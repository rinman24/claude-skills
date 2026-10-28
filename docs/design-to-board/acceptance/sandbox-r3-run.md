# Sandbox run r3 (S11, 2026-10-28): plugin 0.3.3 on the live board

Run by S11 against `rinman24/squadra-sandbox` (local clone `~/Code/squadra-sandbox`,
`squadra.toml` at `8c33d79`: GitHub provider, `claim_scope = "parents"`,
`parent_scope_ids = [1]`). design-to-board: the installed 0.3.3
(`~/.claude/plugins/cache/claude-skills/design-to-board/0.3.3/scripts/design_to_board.py`,
run with `python3 -B` from the clone). squadra: `~/.local/bin/squadra`.

Documents: `sandbox-r3.md` (map `live3`, r1's chain I1 → I2 → I3),
`sandbox-r3-partial-r1.md` (map `partial3`, r1's chain, the revision a crashed
first run was transcribing) and `sandbox-r3-partial-r2.md` (revision 2: I1's
title revised, I2 also depends on `ghost:I1`, a map never transcribed). The
DB10 probe's document is r1 with `map: outscope3`, not kept.

## Before

- `squadra board partial-items --requests-file -` with `[]`: `{"partial_items": []}`, exit 0.
- `claude plugin list`: `design-to-board@claude-skills` 0.3.3, user, enabled.
- Issues #1, #2, #8. `origins`: only `SQ5c-live:claim` (#8, withdrawn).
  `squadra tick --dry-run`: `inflight=[] claimable=[] states={}`.

## 1. Fresh map `live3`, `--parent 1`

| Step | Exit | Output |
|---|---|---|
| dry run | 0 | `dry run for map live3, revision 1, under parent 1: 0 withdrawals, 3 queues. Nothing written.` I1 (none), I2 (`live3:I1`), I3 (`live3:I2`) |
| run | 0 | `queued live3:I1 · item 9 · predecessors: none`; `queued live3:I2 · item 10 · predecessors: 9`; `queued live3:I3 · item 11 · predecessors: 10` |
| re-run | 0 | `nothing to write; the board already matches the document.` |
| re-run, no `--parent` | 0 | same (the map's parent read from the board) |
| `squadra tick --dry-run` | 0 | `inflight=[] claimable=[9] states={9: 'claimable', 10: 'blocked', 11: 'blocked'}` |

`origins` after: `live3:I1`–`I3` → #9–#11, parent 1, `queued`, in claim scope.
Each issue carries `<!-- squadra-origin: "live3:I<n>" -->` in its body, the
`squadra:committed` label and Status Todo on project 1.

## 2. DB10 probe: map `outscope3`, first run, `--parent 2`

| Step | Exit | Output |
|---|---|---|
| dry run | 1 | `failed, nothing written (1 failure …)`; `--parent · map outscope3 · --parent 2 is outside squadra's claim scope · re-run with a --parent inside squadra's claim scope, or widen [board].claim_scope in squadra` |
| run (extra) | 1 | same line; the checks run before any write |

Issues after: unchanged (`[11, 10, 9, 8, 2, 1]`).

## 3. DB12 on a hand-made partial item (Rich agreed, S11)

On GitHub a partial item is an Origin-bearing issue without the adapter's
commit marker (squadra ledger N20, ruling 1); the marker is the
`squadra:committed` label. Hand-made as the state a crash after the adapter's
first write leaves: issue **#12**, title `Greeting store: greetings can be saved and read`,
body exactly `partial3:I1`'s revision-1 body plus
`<!-- squadra-origin: "partial3:I1" -->`; no label, no parent link, not on the project.

- `origins`: exit 0, stderr `item 12 is partial, carrying origin "partial3:I1": a create that did not finish; it is not in the output`.
- `partial-items` with revision 2's I1 request: `queue: refuses`, `disagrees_on: ["title", "body"]` (the parent link is missing, not disagreeing).

| Step | Exit | Output |
|---|---|---|
| r2 dry run, before #12 existed | 1 | one line: `board · I2 · depends on ghost:I1, which is missing from the board · transcribe map ghost first, then re-run design-to-board` |
| r2 dry run | 1 | `failed, nothing written (2 failures …)`: the `ghost:I1` line, and `board · I1 · partial3:I1 is on partial item 12, and squadra would refuse its queue: origin 'partial3:I1' is on partial item 12, which disagrees with this request: title '…can be saved and read' != '…are saved, read and dated'; body differs · repair the partial item by hand in squadra, then re-run design-to-board` |
| r2 run | 1 | the same two lines |
| r1 dry run (unrevised) | 0 | `3 queues`; `queue partial3:I1 · …` (squadra's queue would finish #12) |

After: issues `[12, 11, 10, 9, 8, 2, 1]`; #12 still no label, no project;
tick unchanged (`claimable=[9] states={9: 'claimable', 10: 'blocked', 11: 'blocked'}`).

## Verdict

No defect. 0.3.3 on the live board matches DB5's acceptance (step 1), DB10
(step 2) and DB12 (step 3: both failures in one run, exit 1, nothing
written). Observation, not a defect: the dry-run plan prints the same
`queue` line whether the queue creates an item or finishes a partial one.

## Left on the board

#9–#11 (map `live3`, queued, #9 claimable) and #12 (partial, `partial3:I1`).
Keep or delete is Rich's call (DB9's pattern; `gh issue delete <n> -R rinman24/squadra-sandbox --yes`).
While #12 stays, `origins` prints its stderr line on every read.
