# Sandbox run r4 (S14, 2026-10-28): DB-D16 on the live board, plugin 0.3.4

Run by S14 against `rinman24/squadra-sandbox` (local clone `~/Code/squadra-sandbox`,
`squadra.toml` at `8c33d79`: GitHub provider, `claim_scope = "parents"`,
`parent_scope_ids = [1]`; a hand close as completed reads as done). design-to-board:
the installed 0.3.4
(`~/.claude/plugins/cache/claude-skills/design-to-board/0.3.4/scripts/design_to_board.py`,
run with `python3 -B` from the clone). squadra: `~/.local/bin/squadra`.

Documents: `sandbox-r4-r1.md` (map `done4`, r1's chain I1 → I2 → I3, a copy of
`sandbox-r3.md`), `sandbox-r4-r2.md` (revision 2, as wayfinder's Revise would
publish it: I2 `r1, withdrawn r2`; the cascade withdraws I3, which depends on I2;
new row I4 `Greet by nickname`, `vertical (B1)`, `Depends on: I1`, `r2`; I1's
`Kind` stays `foundation → I2`; `changed: [Increments]`) and `sandbox-r4-r3.md`
(r2 with `revision: 3`, nothing else changed).

The case is Juval's DB-D16 acceptance case, which the fake runs as
`test_juval_db_d16_a_delivered_row_withdrawn_lets_its_replacement_queue`; here DONE
is a GitHub issue closed as completed. Unlike the fake's billing map, I3 depends
on I2, so the cascade adds one withdrawal.

## Before

- `claude plugin list`: `design-to-board@claude-skills` 0.3.4, `wayfinder@claude-skills` 0.2.1, user, enabled.
- Issues #1, #2, #8. `origins`: only `SQ5c-live:claim` (#8, withdrawn).
  `squadra tick --dry-run`: `inflight=[] claimable=[] states={}`. Map `done4` not on the board.

## 1. r1, `--parent 1`

| Step | Exit | Output |
|---|---|---|
| dry run | 0 | `dry run for map done4, revision 1, under parent 1: 0 withdrawals, 3 queues. Nothing written.` I1 (none), I2 (`done4:I1`), I3 (`done4:I2`) |
| run | 0 | `queued done4:I1 · item 13 · predecessors: none`; `queued done4:I2 · item 14 · predecessors: 13`; `queued done4:I3 · item 15 · predecessors: 14` |

`origins` after: `done4:I1`–`I3` → #13–#15, parent 1, `queued`, in claim scope.

## 2. I1 and I2 delivered by hand

`gh issue close 13 … --reason completed`, then 14. `origins`: #13 and #14
`done`, #15 `queued`. Tick: `claimable=[15] states={13: 'done', 14: 'done', 15: 'claimable'}`.

## 3–5. r2 withdraws a delivered row; r3 is cosmetic

The note line, in full, is the same wherever it appears below:

```
note · I2 · done4:I2 (item 14) is delivered and its row is withdrawn in r2; withdrawing a row never undoes delivered work · nothing for design-to-board to do; check that any replacement builds on the delivered work, and undo it with a new increment in wayfinder if it's unwanted
```

| Step | Exit | Output |
|---|---|---|
| r2 dry run, no `--parent` | 0 | `dry run for map done4, revision 2, under parent 1: 1 withdrawal, 1 queue. Nothing written.`; `withdraw done4:I3`; `queue done4:I4 · … · predecessors: done4:I1`; the note |
| r2 run | 0 | `transcribed map done4, revision 2, under parent 1: 1 withdrawal, 1 queue.`; `withdrew done4:I3 · item 15`; `queued done4:I4 · item 16 · predecessors: 13`; the note |
| r2 re-run | 0 | `map done4, revision 2, under parent 1: nothing to write; the board already matches the document.`; the note |
| r3 dry run | 0 | `… revision 3, under parent 1: nothing to write; the board already matches the document.` No note |
| r3 run | 0 | the same line, no note |

Before DB-D16, the r2 run failed on `(withdrawn, DONE)` for I2 and I4 never
queued.

## 6. Tick

`squadra tick --dry-run`: `inflight=[] claimable=[16] states={13: 'done', 14: 'done', 16: 'claimable'}`.
I4 (#16) is claimable because its predecessor #13 is done. `squadra start` was not run.

After: `origins` reads `done4:I1` #13 done, `done4:I2` #14 done, `done4:I3`
#15 withdrawn, `done4:I4` #16 queued, all parent 1 and in claim scope. On GitHub
#13 and #14 are closed as completed, #15 as not planned, #16 is open; all four
carry `squadra:committed`. #16's body is the row's `Field: value` lines plus
`<!-- squadra-origin: "done4:I4" -->`. #14 stayed done through every run.

## Verdict

No defect. 0.3.4 on the live board matches DB-D16: the withdrawn delivered row
writes nothing and gets one `note · I2` on the withdrawing revision only, with
exit 0. Its replacement queues on the delivered predecessor, and the cascade's
withdrawal of a still-queued row goes through. Observation, not a defect: r2
leaves B2 with no live vertical row (I3 withdrawn, nothing replaces it).
wayfinder's map check 2 would be the place that catches this. The translator
doesn't run check 2, and the case doesn't depend on it.

## Left on the board

#13–#16 (map `done4`; #16 queued and claimable). Rich decides whether to keep or delete them (DB9's pattern;
`gh issue delete <n> -R rinman24/squadra-sandbox --yes`).
