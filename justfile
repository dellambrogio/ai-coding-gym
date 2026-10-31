python := justfile_directory() / ".venv/bin/python"
ext := justfile_directory() / "vscode-extension"
gym := python + " " + justfile_directory() / "gym.py"

# List recipes
default:
    @just --list

# --- setup ---

# Create .venv with pytest
setup:
    python3 -m venv {{justfile_directory()}}/.venv && {{python}} -m pip install -q pytest

# --- extension ---

# Compile the TypeScript extension
compile:
    cd {{ext}} && ([ -d node_modules ] || npm install) && npm run -s compile

# Build the .vsix package
package: compile
    cd {{ext}} && npm run -s package

# Install the extension into VS Code (reload windows afterwards)
install: package
    code --install-extension {{ext}}/ai-coding-gym-0.1.0.vsix --force

# Uninstall the extension
uninstall:
    code --uninstall-extension local.ai-coding-gym

# Open VS Code with the extension loaded from source (no install)
dev: compile
    code --new-window --extensionDevelopmentPath={{ext}} {{justfile_directory()}}

# --- sessions (CLI, same as the extension) ---

# List problems
list:
    {{gym}} list

# Start a session (random problem if none given)
start problem="":
    {{gym}} start {{problem}}

# Start a practice session: no clock, every prompt to Claude graded in coaching.md
practice problem="":
    {{gym}} start {{problem}} --practice

# Show the current session
status:
    {{gym}} status

# Run the hidden tests for revealed parts
check:
    {{gym}} check

# Reveal the next part
next:
    {{gym}} next

# Stop the timer, run the final tests, export the transcript
finish:
    {{gym}} finish

# Ask Claude to review the session
review:
    {{gym}} review

# Delete the current session
discard:
    {{gym}} discard

# Delete all sessions except the current one
clean:
    {{gym}} clean

# --- maintenance ---

# Check every problem's hidden tests pass against its reference (or just the ones named)
verify *problems:
    #!/usr/bin/env bash
    set -euo pipefail
    cd {{justfile_directory()}}/problems
    names="{{problems}}"
    fail=0
    for p in ${names:-*}; do
        tmp=$(mktemp -d)
        if [ -d "$p/starter" ]; then
            # Codebase problem: reference/ holds the starter files that change.
            cp -r "$p/starter/." "$p/reference/." "$tmp/"
        else
            cp "$p/reference.py" "$tmp/solution.py"
        fi
        if out=$(cd "$tmp" && PYTHONPATH="$tmp" PYTHONDONTWRITEBYTECODE=1 {{python}} -m pytest -q -p no:cacheprovider \
                "$OLDPWD/$p"/tests/test_part*.py 2>&1); then
            echo "ok    $p: $(echo "$out" | tail -1)"
        else
            echo "FAIL  $p"; echo "$out" | grep -E "^(FAILED|ERROR|E )" | head -10; fail=1
        fi
        rm -rf "$tmp"
    done
    exit $fail
