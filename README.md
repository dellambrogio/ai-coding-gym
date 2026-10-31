# AI Coding Gym

Timed practice for AI-assisted coding interviews: staged problems, hidden tests and a review from Claude at the end.

- `gym.py`: runner (Python; runs the hidden tests with pytest)
- `problems/`: 33 problems in two formats. Don't open these before practicing.
  - single file (19): 3 parts, you write `solution.py` from scratch, hidden tests, `reference.py`
  - codebase (14): an existing multi-file project in `starter/` to fix and extend over 3-4 parts. Part 1 is usually a bug to find. Each part's tests are copied into the session's `tests/` when the part is revealed. Grading always runs the original copies, so editing them doesn't help. `reference/` holds the solved files.
- `sessions/`: one folder per attempt (`problem.md`, `solution.py` or the starter code, `test_mine.py`, `results.json`, `transcript.md`, `review.md`)
- `vscode-extension/`: VS Code front end (TypeScript)

## Shortcuts (`just`)

Run from `ai-coding-gym/`:

| Command | What it does |
|---|---|
| `just setup` | create `.venv` with pytest (first time only) |
| `just install` | install deps if needed, compile, package and install the extension |
| `just dev` | open VS Code with the extension loaded from source, no install |
| `just compile` / `just package` / `just uninstall` | the individual steps |
| `just start [problem]` | start a session from the terminal (random if no problem given) |
| `just check` / `just next` / `just status` / `just finish` / `just review` | session commands, same as the extension |
| `just list` | list problems |
| `just discard` / `just clean` | delete the current session / all sessions except the current one |
| `just verify [problem...]` | check the hidden tests pass against each reference solution (after editing a problem) |

The sections below show what these do step by step.

## Compile the extension

```sh
cd ai-coding-gym/vscode-extension
npm install          # first time only
npm run compile      # TypeScript in src/ → JavaScript in out/
```

## Install it

```sh
npm run package                                      # builds ai-coding-gym-0.1.0.vsix
code --install-extension ai-coding-gym-0.1.0.vsix
```

Then reload any open VS Code windows: **Ctrl+Shift+P**, then **Developer: Reload Window**.

- After changing the code: run `npm run compile && npm run package` and install again with the same command.
- Uninstall: `code --uninstall-extension local.ai-coding-gym`
- To try changes without installing: open `vscode-extension/` in VS Code and press **F5**. A second window opens with the extension loaded.

## Use it

1. Open the `ai-coding-gym` folder in VS Code (`code ai-coding-gym`). The extension finds `gym.py` there. For any other folder, set it once in VS Code settings:
   ```json
   "aiCodingGym.root": "/path/to/ai-coding-gym"
   ```
2. Click **🎓 AI Coding Gym** at the bottom right of the status bar, then **Start new session**, and pick a problem or **Random problem**.
3. The window switches to the session's own folder (it reloads). **Back to …** in the menu returns to the folder you started from. The explorer shows only the code (`.py` files, `tests/`) and `problem.md`; the session's `.vscode/settings.json` hides the rest. `test_mine.py`, `solution.py` (or the starter's main file) and the problem open side by side, the timer starts, and Claude Code launches in a terminal inside the session folder. That folder's `CLAUDE.md` tells Claude to act as the interview assistant, and its settings block reading `problems/`.
4. While you work:
   - The status bar timer follows the 45-minute plan: Clarify, Tests, Build, Verify, Explain. It turns yellow for the last two phases and red in overtime.
   - The **AI Coding Gym** section in the Explorer, below the files, shows the clock, the part, the last test results and the actions. Its title bar has buttons for the tests, the next part and the menu.
   - **Ctrl+Alt+T** runs the hidden tests for every part revealed so far. When they all pass, you're offered the next part.
   - Clicking the timer shows the menu: hidden tests, next part, show problem, reopen Claude, finish, discard the current session, delete all previous sessions.
   - Run your own tests from the session folder with `python -m pytest test_mine.py -q`. In codebase problems, `python -m pytest tests -q` runs the visible tests.
5. When you're done, click **Finish**. This stops the timer, runs the final tests and exports your Claude conversation to `transcript.md`.
6. Then click **Get review**. This runs `claude -p` on the problem, your code, the test results, the event times and the transcript, and writes `review.md` (takes about a minute).

## Tests: yours vs. the AI's

You decide what to test: list the cases yourself first (Tests phase, minutes 5–10). Then let the AI write the test code, read every assertion it writes, and ask it what you missed. Avoid "write tests for my solution" after the code exists: those tests just confirm whatever the code does, bugs included.

The CLI works without the extension: `python gym.py start|check|next|status|finish|review|discard|clean`.
