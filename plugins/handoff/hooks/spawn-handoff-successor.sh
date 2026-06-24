#!/usr/bin/env bash
# Stop hook for the handoff plugin — the SOLE spawner.
#
# Spawns a fresh Claude Code session in a new lower tmux pane to continue work
# with a clean context window.
#
# Coordination with the skill (exactly-once, no model in the spawn path):
#   - The handoff skill's only side effects are writing .pipeline/<slug>/handoff.md
#     and dropping a one-shot marker file at .pipeline/.spawn-successor. It does
#     NOT spawn anything itself.
#   - This hook fires at turn end (Stop). If the marker is present, it spawns the
#     successor and removes the marker. Because the skill never spawns, there is
#     no way to double-spawn, and the spawn never depends on the model.

set -u

# The Stop event JSON arrives on stdin.
INPUT="$(cat)"

# Resolve the project directory: prefer the event's cwd, then CLAUDE_PROJECT_DIR,
# then the current directory.
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$PWD}"

if command -v jq >/dev/null 2>&1; then
  # Loop guard: if this Stop was itself triggered by a hook-driven continuation,
  # do nothing. Prevents the hook re-firing on its own output.
  if [ "$(printf '%s' "$INPUT" | jq -r '.stop_hook_active // false')" = "true" ]; then
    exit 0
  fi
  event_cwd="$(printf '%s' "$INPUT" | jq -r '.cwd // empty')"
  [ -n "$event_cwd" ] && PROJECT_DIR="$event_cwd"
fi

# The skill drops this marker when it runs. No marker => not a handoff => exit.
SIGNAL="${PROJECT_DIR}/.pipeline/.spawn-successor"
[ -f "$SIGNAL" ] || exit 0

# A successor only makes sense inside tmux (there must be a pane to split).
if [ -z "${TMUX:-}" ] || ! command -v tmux >/dev/null 2>&1; then
  # Can't spawn here. Leave the marker so a human can act, and exit cleanly.
  exit 0
fi

# Find the most recently modified handoff.md WITHOUT GNU-only `find -printf`.
# Portable across GNU/Linux and BSD/macOS:
#   - `-maxdepth` exists on both GNU and BSD find.
#   - We pick the newest with the [ -nt ] (newer-than) test instead of
#     `-printf` (GNU-only) or `stat` (whose format flags differ: GNU uses
#     `stat -c '%Y'`, BSD/macOS uses `stat -f '%m'`).
#   - Reading line-by-line with `IFS= read -r` preserves paths containing
#     spaces (the while loop runs in the current shell via the here-doc, so
#     handoff_file survives the loop — unlike `find | while`).
handoff_file=""
while IFS= read -r candidate; do
  [ -n "$candidate" ] || continue
  if [ -z "$handoff_file" ] || [ "$candidate" -nt "$handoff_file" ]; then
    handoff_file="$candidate"
  fi
done <<EOF
$(find "${PROJECT_DIR}/.pipeline" -maxdepth 2 -name handoff.md 2>/dev/null)
EOF

[ -n "$handoff_file" ] || exit 0

# Seed prompt for the successor session.
seed="Read ${handoff_file} and continue the work it describes. It is a handoff document from a previous session whose context window was getting full."

# Spawn a fresh Claude session in a lower pane (60% height) rooted at the
# project. tmux 3.3a uses -l 60% (the deprecated -p 60 was removed).
# printf %q shell-escapes the seed so it survives tmux's sh -c re-parse.
if tmux split-window -v -l 60% -c "$PROJECT_DIR" \
     "claude --dangerously-skip-permissions $(printf '%q' "$seed")"; then
  # One-shot: consume the marker only after a successful spawn, so a failed
  # spawn leaves the marker in place rather than silently losing the handoff.
  rm -f "$SIGNAL"
fi

exit 0
