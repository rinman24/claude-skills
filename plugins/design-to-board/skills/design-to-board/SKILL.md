---
name: design-to-board
description: Transcribe a cleared wayfinder design document (docs/design/<map>.md) into increments on squadra's board; it never designs. Validates the document (DESIGN-FORMAT's translator checks 6–15), reads squadra's board, reconciles the two and writes the withdrawals and queues through `squadra board`; `--dry-run` prints the plan and writes nothing. User-invoked only, after wayfinder's Publish says the document is cleared.
argument-hint: <docs/design/<map>.md> [--parent <id>] [--dry-run]
disable-model-invocation: true
---

# design-to-board

Transcribe a cleared design document into increments on squadra's board. The
document is wayfinder's Published Language
([DESIGN-FORMAT.md](../../../wayfinder/skills/wayfinder/DESIGN-FORMAT.md));
this skill reads it and never designs. The work is done by a deterministic
script; you are its Client.

It reads the document strictly and runs checks 6–15, reads squadra's board
with `squadra board origins` (run it in the target repo; squadra finds its own
`squadra.toml`), and reconciles the two into a plan: withdrawals first, then
queues in dependency order. It then writes the plan through `squadra board
withdraw` and `squadra board queue`, stopping at the first write squadra
refuses. With `--dry-run` it prints the plan and writes nothing.

## Run

Pass the user's arguments verbatim:

```bash
python3 -B "${CLAUDE_PLUGIN_ROOT}/scripts/design_to_board.py" $ARGUMENTS
```

Relay the script's output to the user as it is, then stop.

- Exit 0: what it withdrew and queued (or "nothing to write"), ending with
  the suggestion to run `squadra tick --dry-run`; with `--dry-run`, the plan.
  Relay it, including the suggestion; don't run the tick yourself.
- Exit 1: failed, nothing written. Each line is `check · row · reason · fix`.
  Relay every line; the fix says what the user does next: for a document
  defect, revise the map in wayfinder and Publish again; for `--parent`,
  re-run with the parent the line names; for the board, wait for or stop a
  run, transcribe another map first, or repair the board in squadra.
- Exit 2: the arguments were wrong (usage). Relay the usage message.
- Exit 3: stopped partway. squadra refused or failed one write; the report
  names it (`write · step · reason · fix`), the writes done and the writes
  remaining. Relay all of it. The user re-runs design-to-board with the same
  arguments once the fix is done; the re-run finishes the remaining writes.

## Never

- Never supply an argument the user didn't give, including `--parent`.
- Never edit the design document, the map or any other file, even to fix a
  reported failure. The fix belongs to wayfinder, which the user runs.
- Never re-run with changed arguments after a failure. Report and stop; the
  user decides what to run next.
- Never decide, reorder, rename or add an increment. If the document is wrong,
  the report says so.
- Never call `squadra board queue` or `withdraw` yourself, and never set or
  edit an item's tags; the script is the only writer.
