---
name: design-to-board
description: Transcribe a cleared wayfinder design document (docs/design/<map>.md) into increments on squadra's board; it never designs. This version reads the document and runs DESIGN-FORMAT's translator checks 6–15, and writes nothing. User-invoked only, after wayfinder's Publish says the document is cleared.
argument-hint: <docs/design/<map>.md>
disable-model-invocation: true
---

# design-to-board

Transcribe a cleared design document into increments on squadra's board. The
document is wayfinder's Published Language
([DESIGN-FORMAT.md](../../../wayfinder/skills/wayfinder/DESIGN-FORMAT.md));
this skill reads it and never designs. The work is done by a deterministic
script; you are its Client.

This version validates only: it reads the document strictly and runs checks
6–15. On a valid document it says so and writes nothing. The board steps
(plan, dry run, queueing and withdrawing through squadra) come later.

## Run

Pass the user's arguments verbatim:

```bash
python3 -B "${CLAUDE_PLUGIN_ROOT}/scripts/design_to_board.py" $ARGUMENTS
```

Relay the script's output to the user as it is, then stop.

- Exit 0: the document is valid. Say so; nothing was written.
- Exit 1: failed, nothing written. Each line is `check · row · reason · fix`.
  Relay every line; the fix says what the user does next (for a document
  defect, revise the map in wayfinder and Publish again).
- Exit 2: the arguments were wrong (usage). Relay the usage message.

## Never

- Never supply an argument the user didn't give, including `--parent`.
- Never edit the design document, the map or any other file, even to fix a
  reported failure. The fix belongs to wayfinder, which the user runs.
- Never re-run with changed arguments after a failure. Report and stop; the
  user decides what to run next.
- Never decide, reorder, rename or add an increment. If the document is wrong,
  the report says so.
