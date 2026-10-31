#!/usr/bin/env python3
"""AI Coding Gym runner: mock AI-assisted coding interviews.

Commands (add --json for machine-readable output, used by the VS Code extension):
  list                 list problems
  start [problem]      start a session (random problem if omitted)
  status               show current session
  check                run hidden tests for parts revealed so far
  next                 reveal the next part
  finish               final test run, export Claude transcript
  review               ask Claude (claude -p) to grade the session -> review.md
  discard              delete the current session
  clean                delete all sessions except the current one
"""
import argparse
import difflib
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROBLEMS = ROOT / "problems"
SESSIONS = ROOT / "sessions"
CURRENT = SESSIONS / ".current"
CLAUDE_PROJECTS = Path.home() / ".claude" / "projects"

PHASES = [  # (end minute, name)
    (5, "Clarify"),
    (10, "Tests"),
    (30, "Build"),
    (40, "Verify"),
    (45, "Explain"),
]


ASSISTANT_RULES = """# Mock interview: you are the candidate's AI coding assistant

This folder is a timed mock of an AI-assisted coding interview. The candidate is being
evaluated on how they work with you.

- Behave like the AI assistant built into an interview IDE: helpful, accurate, concise.
- Do exactly what the candidate asks, scoped to the request. Don't solve parts of the
  problem they haven't asked about, and don't volunteer the full solution up front.
- Never suggest next steps. Don't end replies with offers or follow-ups ("Want me to...?",
  "Next, you could...", "You might also..."). The candidate decides what happens next.
- Don't volunteer edge cases, bugs, test ideas, optimizations or reviews unless asked.
  Spotting those is what the candidate is being evaluated on. If asked, answer fully.
- After editing code, say in one or two sentences what you changed, then stop.
- Never read or search the `problems/` directory or any `reference.py`: they hold hidden
  tests and future parts. If asked to, refuse and say it would be cheating.
"""

SINGLE_FILE_RULES = """- The problem statement is `problem.md`; the candidate's code goes in `solution.py`.
- Don't run the hidden tests yourself; the candidate does that from VS Code.
"""

CODEBASE_RULES = """- The problem statement is `problem.md`. The code is the existing codebase in this folder:
  the candidate fixes and extends it. `tests/` holds the tests for the parts revealed so far.
- Run the tests only when the candidate asks you to.
"""


SESSION_SETTINGS = {
    "permissions": {"deny": [f"Read(/{PROBLEMS}/**)", f"Edit(/{PROBLEMS}/**)"]},
    # No hints from Claude Code itself: suggested prompts and spinner tips.
    "promptSuggestionEnabled": False,
    "spinnerTipsEnabled": False,
}

# The extension opens each session in its own window: show the code, hide the bookkeeping.
SESSION_VSCODE_SETTINGS = {
    "files.exclude": {
        "**/__pycache__": True,
        "**/.pytest_cache": True,
        ".claude": True,
        ".vscode": True,
        "CLAUDE.md": True,
        "session.json": True,
        "results.json": True,
        "requirements.txt": True,
    },
    # The interpreter running gym.py has pytest; use it for imports and tests in the session.
    "python.defaultInterpreterPath": sys.executable,
}

TEST_MINE = '''"""Your own tests (Tests phase, minutes 5-10). Run: python -m pytest test_mine.py -q"""
import {module}


def test_example():
    pass
'''


def now():
    return datetime.now(timezone.utc)


def parse_ts(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def problem_parts(name):
    return sorted(PROBLEMS.glob(f"{name}/part*.md"))


def is_codebase(name):
    """Codebase problems ship a multi-file starter/ and tests the candidate can see, one file per part."""
    return (PROBLEMS / name / "starter").is_dir()


def part_tests(name, part):
    return sorted((PROBLEMS / name / "tests").glob(f"test_part{part}*.py"))


def reveal_tests(d, name, part):
    """Copy the visible tests of `part` into the session; grading still uses the copies in problems/."""
    for f in part_tests(name, part):
        shutil.copy(f, d / "tests" / f.name)


def list_problems():
    out = []
    for d in sorted(p for p in PROBLEMS.iterdir() if p.is_dir()):
        meta = json.loads((d / "meta.json").read_text())
        out.append({"name": d.name, "title": meta["title"], "parts": len(problem_parts(d.name))})
    return out


def current_dir():
    if not CURRENT.exists():
        return None
    d = SESSIONS / CURRENT.read_text().strip()
    return d if d.exists() else None


def load_session(d):
    return json.loads((d / "session.json").read_text())


def save_session(d, s):
    (d / "session.json").write_text(json.dumps(s, indent=2))


def log(s, event, **kw):
    s["events"].append({"t": now().isoformat(), "event": event, **kw})


def phase(minutes):
    for end, name in PHASES:
        if minutes < end:
            return name
    return "Overtime"


def status_of(d):
    s = load_session(d)
    end = parse_ts(s["finished"]) if s.get("finished") else now()
    elapsed = (end - parse_ts(s["started"])).total_seconds()
    return {
        "session": d.name,
        "dir": str(d),
        "problem": s["problem"],
        "title": s["title"],
        "part": s["part"],
        "parts": s["parts"],
        "started": s["started"],
        "finished": s.get("finished"),
        "elapsed_seconds": int(elapsed),
        "phase": phase(elapsed / 60),
        "problem_file": str(d / "problem.md"),
        "solution_file": str(d / s.get("main", "solution.py")),
    }


def require_session():
    d = current_dir()
    if not d:
        sys.exit("No active session. Run: gym.py start")
    return d


def cmd_start(args):
    names = [p["name"] for p in list_problems()]
    name = args.problem or random.choice(names)
    if name not in names:
        sys.exit(f"Unknown problem {name!r}. Available: {', '.join(names)}")
    meta = json.loads((PROBLEMS / name / "meta.json").read_text())
    d = SESSIONS / f"{now().astimezone():%Y%m%d-%H%M%S}-{name}"
    d.mkdir(parents=True)
    part1 = problem_parts(name)[0].read_text()
    (d / "problem.md").write_text(f"# {meta['title']}\n\n{part1}")
    if is_codebase(name):
        main = meta["open"]
        shutil.copytree(PROBLEMS / name / "starter", d, dirs_exist_ok=True)
        # Test helpers and data files come along now; the test_part files arrive part by part.
        shutil.copytree(PROBLEMS / name / "tests", d / "tests",
                        ignore=shutil.ignore_patterns("test_part*", "__pycache__"))
        reveal_tests(d, name, 1)
        rules = ASSISTANT_RULES + CODEBASE_RULES
    else:
        main = "solution.py"
        (d / main).write_text(f'"""{meta["title"]} - see problem.md"""\n')
        rules = ASSISTANT_RULES + SINGLE_FILE_RULES
    (d / "test_mine.py").write_text(TEST_MINE.format(module=Path(main).stem))
    # Claude Code started in the session folder picks these up: assistant role + no peeking.
    (d / "CLAUDE.md").write_text(rules)
    (d / ".claude").mkdir()
    (d / ".claude" / "settings.json").write_text(json.dumps(SESSION_SETTINGS, indent=2))
    (d / ".vscode").mkdir()
    (d / ".vscode" / "settings.json").write_text(json.dumps(SESSION_VSCODE_SETTINGS, indent=2))
    s = {
        "problem": name,
        "title": meta["title"],
        "part": 1,
        "parts": len(problem_parts(name)),
        "main": main,
        "started": now().isoformat(),
        "events": [],
    }
    log(s, "start")
    save_session(d, s)
    CURRENT.write_text(d.name)
    return status_of(d)


def run_tests(d, upto):
    """Run hidden tests for parts 1..upto against the session's code."""
    name = load_session(d)["problem"]
    tests = [str(f) for i in range(1, upto + 1) for f in part_tests(name, i)]
    with tempfile.TemporaryDirectory() as tmp:
        xml = Path(tmp) / "r.xml"
        env = {**os.environ, "PYTHONPATH": str(d), "PYTHONDONTWRITEBYTECODE": "1"}
        try:
            proc = subprocess.run(
                [sys.executable, "-m", "pytest", "-q", "--tb=no", "-p", "no:cacheprovider",
                 f"--junitxml={xml}", *tests],
                cwd=d, env=env, capture_output=True, text=True, timeout=60,
            )
            output = (proc.stdout + proc.stderr).strip()
        except subprocess.TimeoutExpired:
            output = "tests timed out after 60s (infinite loop?)"
        results = []
        if xml.exists():
            for tc in ET.parse(xml).getroot().iter("testcase"):
                bad = tc.find("failure")
                if bad is None:
                    bad = tc.find("error")
                msg = ""
                if bad is not None:
                    msg = (bad.get("message") or bad.tag).splitlines()[0][:160]
                    # Collection errors (e.g. missing class) hide the reason in the body.
                    details = [l[1:].strip() for l in (bad.text or "").splitlines() if l.startswith("E ")]
                    if msg == "collection failure" and details:
                        msg = details[-1][:160]
                classname = tc.get("classname") or tc.get("name", "")
                m = re.search(r"test_(part\d+)", classname)
                results.append({
                    "part": m.group(1) if m else classname.split(".")[-1],
                    "name": tc.get("name") if tc.get("classname") else "import solution.py",
                    "passed": bad is None and tc.find("skipped") is None,
                    "message": msg,
                })
        if not results:
            results.append({"part": "-", "name": "collection", "passed": False,
                            "message": output.splitlines()[-1][:300] if output else "no tests ran"})
    passed = sum(r["passed"] for r in results)
    return {"passed": passed, "total": len(results), "results": results}


def cmd_check(args):
    d = require_session()
    s = load_session(d)
    r = run_tests(d, s["part"])
    log(s, "check", part=s["part"], passed=r["passed"], total=r["total"])
    save_session(d, s)
    return {**status_of(d), **r}


def cmd_next(args):
    d = require_session()
    s = load_session(d)
    if s["part"] >= s["parts"]:
        return {**status_of(d), "message": "No more parts. Run finish when you're done."}
    s["part"] += 1
    text = problem_parts(s["problem"])[s["part"] - 1].read_text()
    with open(d / "problem.md", "a") as f:
        f.write(f"\n\n---\n\n{text}")
    if is_codebase(s["problem"]):
        reveal_tests(d, s["problem"], s["part"])
    log(s, "next", part=s["part"])
    save_session(d, s)
    return {**status_of(d), "message": f"Part {s['part']} revealed."}


def cmd_status(args):
    return status_of(require_session())


def export_transcript(d, s):
    """Collect Claude Code messages recorded under ai-coding-gym during the session."""
    start = parse_ts(s["started"])
    end = parse_ts(s["finished"])
    root = str(ROOT)
    lines = []
    for f in CLAUDE_PROJECTS.glob("*/*.jsonl"):
        if datetime.fromtimestamp(f.stat().st_mtime, timezone.utc) < start:
            continue
        for raw in f.open():
            try:
                rec = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if rec.get("type") not in ("user", "assistant") or rec.get("isSidechain"):
                continue
            if not str(rec.get("cwd", "")).startswith(root) or "timestamp" not in rec:
                continue
            ts = parse_ts(rec["timestamp"])
            if not (start <= ts <= end):
                continue
            for text in render(rec):
                lines.append((ts, f"**{ts.astimezone():%H:%M:%S} {text}"))
    lines.sort(key=lambda x: x[0])
    body = "\n\n".join(t for _, t in lines) or "_No Claude Code messages found for this session._"
    (d / "transcript.md").write_text(f"# Transcript\n\n{body}\n")
    return len(lines)


def render(rec):
    c = rec["message"].get("content")
    who = "Candidate" if rec["type"] == "user" else "AI"
    if isinstance(c, str):
        yield f"{who}:** {c}"
        return
    for b in c or []:
        t = b.get("type")
        if t == "text":
            yield f"{who}:** {b['text']}"
        elif t == "tool_use":
            yield f"AI tool {b['name']}:** `{json.dumps(b.get('input'))[:400]}`"
        elif t == "tool_result":
            content = b.get("content")
            if isinstance(content, list):
                content = " ".join(x.get("text", "") for x in content if isinstance(x, dict))
            yield f"Tool result:** {str(content)[:300]}"


def cmd_finish(args):
    d = require_session()
    s = load_session(d)
    if not s.get("finished"):
        s["finished"] = now().isoformat()
    r = run_tests(d, s["part"])
    log(s, "finish", part=s["part"], passed=r["passed"], total=r["total"])
    save_session(d, s)
    (d / "results.json").write_text(json.dumps(r, indent=2))
    n = export_transcript(d, s)
    return {**status_of(d), **r, "transcript_messages": n}


REVIEW_PROMPT = """You are a senior engineer grading a candidate's AI-assisted coding interview.
The candidate had an AI coding assistant (Claude Code) available. Below are: the problem
(all parts revealed so far), the candidate's final solution, hidden test results, the
session event log (timestamps of test runs and part reveals), and the transcript of the
candidate's conversation with the AI assistant.

Write a candid review in Markdown with these sections:
1. **Verdict**: Strong hire / Hire / Lean no / No hire, with one sentence why.
2. **Scores (1-5)** for: Problem framing (clarified before prompting?), Prompting
   (specific, scoped requests vs "solve this"), Verification (read/test the AI's output,
   caught its mistakes), Ownership (could explain and justify the code), Code quality,
   Time management (compare event times to the 45-minute plan: 0-5 clarify, 5-10 tests,
   10-30 build, 30-40 verify, 40-45 explain).
3. **Moments that helped**, quoting the transcript.
4. **Moments that hurt**, quoting the transcript.
5. **Code review** of the solution: bugs, complexity, edge cases the tests may not cover.
6. **Three things to do differently next time.**

Be specific and honest; don't inflate.
"""


def cmd_review(args):
    d = require_session()
    s = load_session(d)
    if not s.get("finished"):
        cmd_finish(args)
        s = load_session(d)
    if is_codebase(s["problem"]):
        solution = "## Solution: changes to the starter codebase\n```diff\n" + starter_diff(d, s["problem"]) + "\n```"
    else:
        solution = "## Solution (solution.py)\n```python\n" + (d / "solution.py").read_text() + "\n```"
    parts = [
        REVIEW_PROMPT,
        "## Problem\n" + (d / "problem.md").read_text(),
        solution,
        "## Hidden test results\n```json\n" + (d / "results.json").read_text() + "\n```",
        "## Event log\n```json\n" + json.dumps(s["events"], indent=2) + "\n```",
        (d / "transcript.md").read_text(),
    ]
    # Include any other files the candidate created (e.g. test_mine.py).
    starter = PROBLEMS / s["problem"] / "starter"
    for f in sorted(d.iterdir()):
        if (starter / f.name).exists():
            continue  # already in the diff
        if f.suffix in (".py", ".md", ".txt") and f.name not in ("solution.py", "problem.md", "transcript.md", "review.md", "CLAUDE.md"):
            parts.append(f"## Candidate file {f.name}\n```\n{f.read_text()[:8000]}\n```")
    # The extension passes the claude it found, since VS Code's PATH may not include it.
    claude = os.environ.get("AI_CODING_GYM_CLAUDE") or shutil.which("claude")
    if not claude:
        sys.exit("claude CLI not found on PATH")
    print("Asking Claude for a review...", file=sys.stderr)
    proc = subprocess.run([claude, "-p", "Grade this interview session as instructed in the input."],
                          input="\n\n".join(parts), capture_output=True, text=True, cwd=tempfile.gettempdir())
    if proc.returncode != 0:
        sys.exit(f"claude failed: {proc.stderr.strip()}")
    (d / "review.md").write_text(proc.stdout)
    return {**status_of(d), "review_file": str(d / "review.md")}


def starter_diff(d, name):
    """Unified diff of the session against the starter code and the visible tests it was given."""
    out = []
    for base, sub in ((PROBLEMS / name / "starter", ""), (PROBLEMS / name / "tests", "tests/")):
        for f in sorted(p for p in base.rglob("*") if p.is_file() and "__pycache__" not in p.parts):
            rel = sub + str(f.relative_to(base))
            mine = d / rel
            if not mine.exists():
                continue  # deleted by the candidate, or a part's tests not revealed yet
            out += difflib.unified_diff(f.read_text().splitlines(keepends=True),
                                        mine.read_text().splitlines(keepends=True),
                                        f"starter/{rel}", rel)
    return "".join(out) or "(no changes)"


def cmd_discard(args):
    d = require_session()
    shutil.rmtree(d)
    CURRENT.unlink()
    return {"message": f"Discarded {d.name}."}


def cmd_clean(args):
    keep = current_dir()
    old = [d for d in SESSIONS.glob("*") if d.is_dir() and d != keep] if SESSIONS.exists() else []
    for d in old:
        shutil.rmtree(d)
    return {"deleted": len(old), "message": f"Deleted {len(old)} previous session(s)."}


def fmt(cmd, out):
    if cmd in ("discard", "clean"):
        return out["message"]
    if cmd == "list":
        width = max(len(p["name"]) for p in out)
        return "\n".join(f"{p['name']:<{width}}  {p['title']} ({p['parts']} parts)" for p in out)
    m, sec = divmod(out["elapsed_seconds"], 60)
    lines = [f"{out['title']} - part {out['part']}/{out['parts']} - {m:02d}:{sec:02d} ({out['phase']})",
             f"session: {out['dir']}"]
    if "results" in out:
        for r in out["results"]:
            mark = "PASS" if r["passed"] else "FAIL"
            lines.append(f"  {mark} [{r['part']}] {r['name']}" + (f"  - {r['message']}" if r["message"] else ""))
        lines.append(f"{out['passed']}/{out['total']} passed")
    for k in ("message", "review_file"):
        if k in out:
            lines.append(str(out[k]))
    if "transcript_messages" in out:
        lines.append(f"transcript: {out['transcript_messages']} messages -> {out['dir']}/transcript.md")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    sp = sub.add_parser("start")
    sp.add_argument("problem", nargs="?")
    for c in ("status", "check", "next", "finish", "review", "discard", "clean"):
        sub.add_parser(c)
    args = ap.parse_args()
    handlers = {"list": lambda a: list_problems(), "start": cmd_start, "status": cmd_status,
                "check": cmd_check, "next": cmd_next, "finish": cmd_finish, "review": cmd_review,
                "discard": cmd_discard, "clean": cmd_clean}
    out = handlers[args.cmd](args)
    print(json.dumps(out) if args.json else fmt(args.cmd, out))


if __name__ == "__main__":
    main()
