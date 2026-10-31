import { execFile } from "child_process";
import * as fs from "fs";
import * as path from "path";
import * as vscode from "vscode";

interface Status {
  session: string;
  dir: string;
  problem: string;
  title: string;
  part: number;
  parts: number;
  started: string;
  finished: string | null;
  elapsed_seconds: number;
  phase: string;
  problem_file: string;
  solution_file: string;
}

interface TestResult {
  part: string;
  name: string;
  passed: boolean;
  message: string;
}

interface CheckResult extends Status {
  passed: number;
  total: number;
  results: TestResult[];
  transcript_messages?: number;
}

// Matches PHASES in gym.py: [end minute, name, hint].
const PHASES: [number, string, string][] = [
  [5, "Clarify", "Clarify the problem, list edge cases, pick an approach. No AI yet."],
  [10, "Tests", "Write a few tests of your own."],
  [30, "Build", "Build with the AI in small steps, reviewing each piece."],
  [40, "Verify", "Run the hidden tests, add tricky cases, fix bugs."],
  [45, "Explain", "Explain complexity and trade-offs; expect follow-ups."],
];

let status: Status | undefined;
let statusBar: vscode.StatusBarItem;
let output: vscode.OutputChannel;
let lastPhase = "";
let extensionContext: vscode.ExtensionContext;
let lastCheck: CheckResult | undefined;
let view: GymView;
let treeView: vscode.TreeView<vscode.TreeItem>;

export function activate(context: vscode.ExtensionContext) {
  extensionContext = context;
  output = vscode.window.createOutputChannel("AI Coding Gym");
  statusBar = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
  statusBar.command = "aiCodingGym.menu";
  statusBar.show();
  view = new GymView();
  treeView = vscode.window.createTreeView("aiCodingGym.session", { treeDataProvider: view });
  context.subscriptions.push(treeView);

  const commands: [string, () => Promise<void>][] = [
    ["aiCodingGym.menu", menu],
    ["aiCodingGym.start", start],
    ["aiCodingGym.check", check],
    ["aiCodingGym.next", next],
    ["aiCodingGym.showProblem", showProblem],
    ["aiCodingGym.openClaude", openClaude],
    ["aiCodingGym.finish", finish],
    ["aiCodingGym.review", review],
    ["aiCodingGym.discard", discard],
    ["aiCodingGym.clean", clean],
    ["aiCodingGym.back", goBack],
  ];
  for (const [id, fn] of commands) {
    context.subscriptions.push(vscode.commands.registerCommand(id, () => fn().catch(showError)));
  }
  const timer = setInterval(render, 1000);
  context.subscriptions.push(statusBar, output, { dispose: () => clearInterval(timer) });

  // Resume a session that was running when VS Code closed. In a session's own window,
  // set it up the first time the window opens.
  runMock<Status>(context, ["status"])
    .then(async (s) => {
      status = s;
      lastPhase = phaseOf(elapsedMinutes());
      if (!s.finished && isSessionWindow(s) && !context.workspaceState.get<boolean>("aiCodingGym.setUp")) {
        await context.workspaceState.update("aiCodingGym.setUp", true);
        render();
        await setUpSession(s);
      }
    })
    .catch(() => undefined)
    .finally(render);
}

export function deactivate() {}

// ---- gym.py plumbing ----

function root(context: vscode.ExtensionContext): string {
  const configured = vscode.workspace.getConfiguration("aiCodingGym").get<string>("root");
  const candidates = configured
    ? [configured]
    : [
        // Development: the extension sits inside ai-coding-gym/. Installed: look in the open workspace.
        path.dirname(context.extensionPath),
        // A session window is opened on ai-coding-gym/sessions/<session>.
        ...(vscode.workspace.workspaceFolders ?? []).flatMap((f) =>
          [f.uri.fsPath, path.join(f.uri.fsPath, "ai-coding-gym"), path.resolve(f.uri.fsPath, "..", "..")]),
      ];
  const dir = candidates.find((d) => fs.existsSync(path.join(d, "gym.py")));
  if (!dir) {
    throw new Error(`gym.py not found. Open the ai-coding-gym folder, or set "aiCodingGym.root".`);
  }
  return dir;
}

function python(dir: string): string {
  const configured = vscode.workspace.getConfiguration("aiCodingGym").get<string>("python");
  if (configured) {
    return configured;
  }
  for (const venv of [path.join(dir, ".venv"), path.join(dir, "..", ".venv")]) {
    const exe = path.join(venv, "bin", "python");
    if (fs.existsSync(exe)) {
      return path.resolve(exe);
    }
  }
  return "python3";
}

function runMock<T>(context: vscode.ExtensionContext, args: string[], timeoutMs = 120_000): Promise<T> {
  const dir = root(context);
  return new Promise((resolve, reject) => {
    const claude = findClaude();
    const env = claude ? { ...process.env, AI_CODING_GYM_CLAUDE: claude } : process.env;
    execFile(python(dir), [path.join(dir, "gym.py"), "--json", ...args], { cwd: dir, env, timeout: timeoutMs },
      (err, stdout, stderr) => {
        if (err) {
          reject(new Error(stderr.trim().split("\n").pop() || err.message));
          return;
        }
        try {
          resolve(JSON.parse(stdout) as T);
        } catch {
          reject(new Error(`Unexpected output from gym.py: ${stdout.slice(0, 200)}`));
        }
      });
  });
}

function showError(err: unknown) {
  vscode.window.showErrorMessage(`AI Coding Gym: ${err instanceof Error ? err.message : String(err)}`);
}

function isSessionWindow(s: Status): boolean {
  const folders = vscode.workspace.workspaceFolders ?? [];
  return folders.length === 1 && path.resolve(folders[0].uri.fsPath) === path.resolve(s.dir);
}

function requireSession(): Status {
  if (!status) {
    throw new Error("No active session. Run 'AI Coding Gym: Start'.");
  }
  return status;
}

// ---- timer ----

function elapsedMinutes(): number {
  if (!status) {
    return 0;
  }
  const end = status.finished ? Date.parse(status.finished) : Date.now();
  return (end - Date.parse(status.started)) / 60_000;
}

function phaseOf(minutes: number): string {
  return PHASES.find(([end]) => minutes < end)?.[1] ?? "Overtime";
}

function render() {
  renderStatusBar();
  view.update();
}

function renderStatusBar() {
  if (!status) {
    statusBar.text = "$(mortar-board) AI Coding Gym";
    statusBar.tooltip = "Start a mock AI-assisted coding interview";
    statusBar.backgroundColor = undefined;
    return;
  }
  const minutes = elapsedMinutes();
  const total = Math.floor(minutes * 60);
  const clock = `${String(Math.floor(total / 60)).padStart(2, "0")}:${String(total % 60).padStart(2, "0")}`;
  const phase = phaseOf(minutes);
  const done = status.finished ? " · finished" : "";
  statusBar.text = `$(watch) ${clock} ${phase} · Part ${status.part}/${status.parts}${done}`;
  statusBar.tooltip = new vscode.MarkdownString(
    `**${status.title}**\n\n` +
      PHASES.map(([end, name, hint], i) => {
        const startMin = i === 0 ? 0 : PHASES[i - 1][0];
        const line = `${startMin}–${end} min **${name}**: ${hint}`;
        return name === phase ? `→ ${line}` : line;
      }).join("\n\n") +
      "\n\nClick for actions."
  );
  statusBar.backgroundColor = status.finished
    ? undefined
    : phase === "Overtime"
      ? new vscode.ThemeColor("statusBarItem.errorBackground")
      : phase === "Verify" || phase === "Explain"
        ? new vscode.ThemeColor("statusBarItem.warningBackground")
        : undefined;

  if (!status.finished && phase !== lastPhase) {
    lastPhase = phase;
    const hint = PHASES.find(([, name]) => name === phase)?.[2] ?? "Time's up. Wrap up and explain your solution.";
    vscode.window.showInformationMessage(`AI Coding Gym: ${phase} phase. ${hint}`);
  }
}

// ---- sidebar view (Explorer) ----

interface Action {
  icon: string;
  label: string;
  command: string;
}

// What you can do right now: shared by the menu and the sidebar view.
function actions(): Action[] {
  const items: Action[] = status && !status.finished
    ? [
        { icon: "beaker", label: "Run hidden tests", command: "aiCodingGym.check" },
        { icon: "arrow-right", label: "Next part", command: "aiCodingGym.next" },
        { icon: "book", label: "Show problem", command: "aiCodingGym.showProblem" },
        { icon: "terminal", label: "Open Claude in session", command: "aiCodingGym.openClaude" },
        { icon: "check-all", label: "Finish", command: "aiCodingGym.finish" },
        { icon: "discard", label: "Discard current session", command: "aiCodingGym.discard" },
        { icon: "trash", label: "Delete all previous sessions", command: "aiCodingGym.clean" },
      ]
    : [
        { icon: "play", label: "Start new session", command: "aiCodingGym.start" },
        ...(status
          ? [
              { icon: "comment-discussion", label: "Get Claude review", command: "aiCodingGym.review" },
              { icon: "discard", label: "Discard current session", command: "aiCodingGym.discard" },
            ]
          : []),
        { icon: "trash", label: "Delete all previous sessions", command: "aiCodingGym.clean" },
      ];
  const back = returnFolder();
  if (status && isSessionWindow(status) && back) {
    items.push({ icon: "folder", label: `Back to ${path.basename(back)}`, command: "aiCodingGym.back" });
  }
  return items;
}

function item(label: string, opts: Partial<vscode.TreeItem> & { icon?: string; color?: string } = {}): vscode.TreeItem {
  const { icon, color, ...rest } = opts;
  const it = Object.assign(new vscode.TreeItem(label), rest);
  if (icon) {
    it.iconPath = new vscode.ThemeIcon(icon, color ? new vscode.ThemeColor(color) : undefined);
  }
  return it;
}

class GymView implements vscode.TreeDataProvider<vscode.TreeItem> {
  private changed = new vscode.EventEmitter<vscode.TreeItem | undefined>();
  readonly onDidChangeTreeData = this.changed.event;
  private shown = "";
  private testItems: vscode.TreeItem[] = [];

  // Called every second: the clock goes in the header, the tree is rebuilt only when it changes.
  update() {
    if (treeView) {
      treeView.description = status ? statusBar.text.replace("$(watch) ", "") : "";
    }
    const key = JSON.stringify([status?.session, status?.part, status?.finished, phaseOf(elapsedMinutes()),
      lastCheck?.passed, lastCheck?.total, returnFolder()]);
    if (key !== this.shown) {
      this.shown = key;
      this.changed.fire(undefined);
    }
  }

  getTreeItem(element: vscode.TreeItem): vscode.TreeItem {
    return element;
  }

  getChildren(element?: vscode.TreeItem): vscode.TreeItem[] {
    if (element) {
      return element.id === "tests" ? this.testItems : [];
    }
    const items: vscode.TreeItem[] = [];
    if (status) {
      const phase = phaseOf(elapsedMinutes());
      items.push(item(status.title, {
        description: `part ${status.part}/${status.parts}`,
        icon: "book",
        tooltip: "Show the problem",
        command: { command: "aiCodingGym.showProblem", title: "Show problem" },
      }));
      if (!status.finished) {
        items.push(item(phase, {
          description: PHASES.find(([, name]) => name === phase)?.[2] ?? "Time's up. Wrap up and explain your solution.",
          icon: "watch",
          color: phase === "Overtime" ? "errorForeground" : undefined,
        }));
      }
      if (lastCheck) {
        const allPassed = lastCheck.passed === lastCheck.total;
        this.testItems = lastCheck.results.map((t) => item(t.name, {
          description: t.message ? `${t.part} · ${t.message}` : t.part,
          tooltip: t.message || "passed",
          icon: t.passed ? "pass" : "error",
          color: t.passed ? "testing.iconPassed" : "testing.iconFailed",
        }));
        items.push(item(`Tests: ${lastCheck.passed}/${lastCheck.total} passed`, {
          id: "tests",
          icon: allPassed ? "pass-filled" : "error",
          color: allPassed ? "testing.iconPassed" : "testing.iconFailed",
          collapsibleState: allPassed ? vscode.TreeItemCollapsibleState.Collapsed : vscode.TreeItemCollapsibleState.Expanded,
        }));
      }
    }
    for (const a of actions()) {
      items.push(item(a.label, { icon: a.icon, command: { command: a.command, title: a.label } }));
    }
    return items;
  }
}

// ---- commands ----

async function menu() {
  const items = actions().map((a) => ({ label: `$(${a.icon}) ${a.label}`, command: a.command }));
  const pick = await vscode.window.showQuickPick(items, { placeHolder: "AI Coding Gym" });
  if (pick) {
    await vscode.commands.executeCommand(pick.command);
  }
}

async function start() {
  if (status && !status.finished) {
    const ok = await vscode.window.showWarningMessage(
      `A session (${status.title}) is still running. Abandon it?`, { modal: true }, "Start new");
    if (!ok) {
      return;
    }
  }
  const problems = await runMock<{ name: string; title: string; parts: number }[]>(extensionContext, ["list"]);
  const pick = await vscode.window.showQuickPick(
    [
      { label: "$(question) Random problem", name: "" },
      ...problems.map((p) => ({ label: p.title, description: `${p.parts} parts`, name: p.name })),
    ],
    { placeHolder: "Pick a problem. Parts after the first stay hidden until you reveal them." }
  );
  if (!pick) {
    return;
  }
  status = await runMock<Status>(extensionContext, pick.name ? ["start", pick.name] : ["start"]);
  lastCheck = undefined;
  lastPhase = phaseOf(0);
  render();
  // Switch this window to the session folder, so the explorer shows only its code. The window
  // reloads, and the extension sets up the editors and Claude there (see activate).
  const current = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
  if (current && !path.resolve(current).startsWith(path.join(root(extensionContext), "sessions") + path.sep)) {
    await extensionContext.globalState.update("aiCodingGym.returnTo", current);
  }
  await vscode.commands.executeCommand("vscode.openFolder", vscode.Uri.file(status.dir), { forceNewWindow: false });
}

// The folder that was open before the first session started.
function returnFolder(): string | undefined {
  const dir = extensionContext.globalState.get<string>("aiCodingGym.returnTo");
  return dir && fs.existsSync(dir) ? dir : undefined;
}

async function goBack() {
  const dir = returnFolder();
  if (!dir) {
    throw new Error("No folder to go back to. Use File > Open Folder.");
  }
  await vscode.commands.executeCommand("vscode.openFolder", vscode.Uri.file(dir), { forceNewWindow: false });
}

async function setUpSession(s: Status) {
  // Launch Claude first so a failure opening editors or the preview can't skip it.
  if (vscode.workspace.getConfiguration("aiCodingGym").get<boolean>("launchClaude")) {
    await openClaude().catch(showError);
  }
  // Layout, left to right: test_mine.py | solution.py | problem preview.
  const tests = await vscode.workspace.openTextDocument(path.join(s.dir, "test_mine.py"));
  await vscode.window.showTextDocument(tests, { viewColumn: vscode.ViewColumn.One, preview: false });
  const doc = await vscode.workspace.openTextDocument(s.solution_file);
  await vscode.window.showTextDocument(doc, { viewColumn: vscode.ViewColumn.Two, preview: false });
  // Opens beside the active group (solution.py), so it lands in the third column.
  await showProblem().catch(showError);
  // Put the cursor back in solution.py.
  await vscode.window.showTextDocument(doc, { viewColumn: vscode.ViewColumn.Two, preview: false });
  vscode.window.showInformationMessage(
    `AI Coding Gym session started: ${s.title}. Clarify phase (0–5 min): no AI yet.`);
}

async function showProblem() {
  const s = requireSession();
  // Locked, so it keeps showing the problem when another markdown file becomes active.
  await vscode.commands.executeCommand("markdown.showLockedPreviewToSide", vscode.Uri.file(s.problem_file));
}

async function openClaude() {
  const s = requireSession();
  const existing = vscode.window.terminals.find((t) => t.name === `Claude · ${s.session}`);
  if (existing) {
    existing.show();
    return;
  }
  const claude = findClaude();
  if (!claude) {
    throw new Error('claude CLI not found. Set "aiCodingGym.claudePath" to its full path.');
  }
  // hideFromUser makes the Python extensions skip auto-activation, which would otherwise type
  // `source .../activate` into Claude's prompt. show() still reveals the terminal.
  const term = vscode.window.createTerminal({ name: `Claude · ${s.session}`, cwd: s.dir, hideFromUser: true });
  term.show();
  // Activate the venv too, so `python -m pytest test_mine.py` works in this terminal after Claude exits.
  const activate = path.join(path.dirname(python(root(extensionContext))), "activate");
  // The session's CLAUDE.md doubles as a system prompt, which weighs more than memory files.
  const rules = fs.existsSync(path.join(s.dir, "CLAUDE.md")) ? " --append-system-prompt-file CLAUDE.md" : "";
  const cmd = `"${claude}"${rules}`;
  term.sendText(fs.existsSync(activate) ? `source "${activate}"; ${cmd}` : cmd);
}

// VS Code terminals may not have ~/.local/bin on PATH, so resolve the binary ourselves.
function findClaude(): string | undefined {
  const configured = vscode.workspace.getConfiguration("aiCodingGym").get<string>("claudePath");
  if (configured) {
    return configured;
  }
  const home = process.env.HOME ?? "";
  const dirs = [
    ...(process.env.PATH ?? "").split(path.delimiter),
    path.join(home, ".local", "bin"),
    path.join(home, ".claude", "local"),
    "/usr/local/bin",
  ];
  return dirs.map((d) => path.join(d, "claude")).find((p) => isExecutable(p));
}

function isExecutable(p: string): boolean {
  try {
    fs.accessSync(p, fs.constants.X_OK);
    return true;
  } catch {
    return false;
  }
}

function printResults(title: string, r: CheckResult) {
  output.clear();
  output.appendLine(`${title}: ${r.title}, part ${r.part}/${r.parts}`);
  output.appendLine("");
  for (const t of r.results) {
    output.appendLine(`${t.passed ? "✔ PASS" : "✘ FAIL"}  [${t.part}] ${t.name}${t.message ? `\n          ${t.message}` : ""}`);
  }
  output.appendLine("");
  output.appendLine(`${r.passed}/${r.total} passed`);
  output.show(true);
}

async function check() {
  requireSession();
  await vscode.workspace.saveAll(false);
  const r = await vscode.window.withProgress(
    { location: vscode.ProgressLocation.Notification, title: "Running hidden tests…" },
    () => runMock<CheckResult>(extensionContext, ["check"]));
  status = r;
  lastCheck = r;
  render();
  printResults("Hidden tests", r);
  const msg = `${r.passed}/${r.total} hidden tests passed (part ${r.part}/${r.parts}).`;
  if (r.passed === r.total && r.part < r.parts) {
    const go = await vscode.window.showInformationMessage(`${msg} Reveal the next part?`, "Next part");
    if (go) {
      await next();
    }
  } else if (r.passed === r.total) {
    vscode.window.showInformationMessage(`${msg} All parts done. Finish when you've explained your solution.`);
  } else {
    vscode.window.showWarningMessage(msg);
  }
}

async function next() {
  const s = requireSession();
  if (s.part >= s.parts) {
    vscode.window.showInformationMessage("That was the last part. Finish when you're done.");
    return;
  }
  status = await runMock<Status>(extensionContext, ["next"]);
  lastCheck = undefined;
  render();
  await showProblem();
  // The preview's file watcher can miss the append, so refresh it explicitly.
  await vscode.commands.executeCommand("markdown.preview.refresh");
  vscode.window.showInformationMessage(`Part ${status.part}/${status.parts} revealed. See the problem panel.`);
}

async function finish() {
  const s = requireSession();
  const ok = await vscode.window.showWarningMessage(
    `Finish ${s.title}? The timer stops and the final hidden tests run.`, { modal: true }, "Finish");
  if (!ok) {
    return;
  }
  await vscode.workspace.saveAll(false);
  const r = await vscode.window.withProgress(
    { location: vscode.ProgressLocation.Notification, title: "Final test run…" },
    () => runMock<CheckResult>(extensionContext, ["finish"]));
  status = r;
  lastCheck = r;
  render();
  printResults("Final results", r);
  const go = await vscode.window.showInformationMessage(
    `Finished: ${r.passed}/${r.total} tests, part ${r.part}/${r.parts}. ` +
      `${r.transcript_messages ?? 0} Claude messages captured. Get a review from Claude?`,
    "Get review");
  if (go) {
    await review();
  }
}

async function review() {
  requireSession();
  const r = await vscode.window.withProgress(
    { location: vscode.ProgressLocation.Notification, title: "Claude is reviewing your session (about a minute)…" },
    () => runMock<Status & { review_file: string }>(extensionContext, ["review"], 600_000));
  status = r;
  render();
  await vscode.commands.executeCommand("markdown.showPreview", vscode.Uri.file(r.review_file));
}

async function discard() {
  const s = requireSession();
  const ok = await vscode.window.showWarningMessage(
    `Discard ${s.title}? Its folder (${s.session}) is deleted, including your solution.`, { modal: true }, "Discard");
  if (!ok) {
    return;
  }
  await closeSession(s);
  const r = await runMock<{ message: string }>(extensionContext, ["discard"]);
  if (isSessionWindow(s)) {
    // Its folder is gone: go back to the folder the session was started from.
    if (returnFolder()) {
      await goBack();
    } else {
      await vscode.commands.executeCommand("workbench.action.closeFolder");
    }
    return;
  }
  status = undefined;
  lastCheck = undefined;
  render();
  vscode.window.showInformationMessage(`AI Coding Gym: ${r.message}`);
}

async function clean() {
  const keep = status ? ` The current session (${status.title}) is kept.` : "";
  const ok = await vscode.window.showWarningMessage(
    `Delete all previous sessions, with their solutions, transcripts and reviews?${keep}`, { modal: true }, "Delete");
  if (!ok) {
    return;
  }
  const r = await runMock<{ message: string }>(extensionContext, ["clean"]);
  vscode.window.showInformationMessage(`AI Coding Gym: ${r.message}`);
}

// Close the session's Claude terminal and editors before its folder is deleted.
async function closeSession(s: Status) {
  vscode.window.terminals.find((t) => t.name === `Claude · ${s.session}`)?.dispose();
  const inSession = (uri: vscode.Uri | undefined) => !!uri && uri.fsPath.startsWith(s.dir + path.sep);
  const tabs = vscode.window.tabGroups.all.flatMap((g) => g.tabs).filter((t) => {
    const input = t.input;
    if (input instanceof vscode.TabInputText || input instanceof vscode.TabInputCustom) {
      return inSession(input.uri);
    }
    // The markdown preview is a webview tab with no URI; match it by its title.
    return input instanceof vscode.TabInputWebview && t.label.includes("problem.md");
  });
  await vscode.window.tabGroups.close(tabs);
}
