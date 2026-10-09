# Handoff: SQ1 · squadra: mandatory claim scope (W-SQ, WSQ1)

Rich starts a fresh `claude` session in `~/Code/squadra` and pastes this whole
file as the first message.

## Context

This unit is squadra code, not the claude-skills port. The requirement was
ruled in the port's Q3 session and lives in the claude-skills ledger. Work in
`rinman24/squadra`, starting from `main` (`d9d2afa` at W9, 2026-10-09; fetch
and check whether it moved). Create a worktree on a new branch
`feat/mandatory-claim-scope`, and never commit to main. Follow squadra's own
`CLAUDE.md` and the engineering rules its hooks inject (closed architecture,
vertical slice, testing conventions). If they conflict with this file, they
win, and you tell Rich.

The squadra checkout may have two untracked `*.prototype.html` files at its
root, left over from prototype checks. The Q4 session clears them with Rich.
Leave them alone and keep them out of your commits.

Read first, in order:
1. squadra's `CLAUDE.md`, `GLOSSARY.md` and `README.md`
2. The W-SQ row in
   `~/Code/claude-skills/docs/wayfinder-port/LEDGER.md` (Rich pulled `main`
   with the port on 2026-10-09). Its "Remaining (WSQ1, Q3)" list, items
   (1)–(5), is the spec. Also read WSQ1 and WD14/WD18 in the Decisions section
3. Juval's session file
   `~/Code/board-knowledge/sessions/2026-10-08-juval-mandatory-claim-scope.md`
4. The code the spec cites: `config.py:192` (`[board].parent_scope_ids`),
   `config.py:198` (`FLEET_EPIC_IDS`, `FLEET_PARENT_SCOPE_IDS`),
   `supervisor.py:486` (`_predecessors_done`, which today reports an
   out-of-scope item as `BLOCKED`), `_classify`, `LifecycleFacts`,
   `test_supervisor_claim.py:324`, `test_supervisor_dry_run.py` and
   `test_cli.py:178`. Line numbers are as of `d9d2afa`.

Read files outside squadra by absolute path, with no `cd` (claude-skills
lessons S6, S7, S9).

## This session's unit

Ledger items: W-SQ (WSQ1 items 1–5).
Goal: a ready-for-review squadra PR that makes positive claim scope mandatory
and fail-closed:
1. `[board].claim_scope` is required and is `"parents"` or `"whole-board"`.
   Loading fails with `ConfigError` if it is missing, if `"parents"` has no
   `parent_scope_ids`, or if `"whole-board"` has ids.
2. `squadra init` writes `claim_scope` with no value, so the first load fails
   naming both options.
3. Drop the env vars and the unit file's `Environment=FLEET_PARENT_SCOPE_IDS=`
   line, or render it from the validated declaration.
4. `in_claim_scope` in `LifecycleFacts`, and a terminal `OUT_OF_SCOPE` state
   in `_classify` before the queued step, gated on the queued bucket only. An
   item that is in flight and gets reparented out of scope still finalizes or
   reaps.
5. An end-to-end `squadra tick --dry-run` contract test, plus the three
   load-error tests.

Write the tests first (squadra's testing conventions). No migration: no live
config exists.
Estimated work: ~60–80K (budget: under 100K total, hard stop at 120K). If it
runs long, split after items 1–3 (config and init, with their tests) and
hand items 4–5 (the lifecycle state and the contract test) to SQ2.

## Decisions already made

- WSQ1 (Rich, Q3, 2026-10-08, after Juval): scope is mandatory now in form
  (a), a fail-closed config check. Not form (b), and it doesn't wait for
  `design-to-board`.
- Nothing outside squadra sets `FLEET_EPIC_IDS` or `FLEET_PARENT_SCOPE_IDS`
  (grep of `~/Code`, Q3).
- Deferred to the GitHub adapter unit: the adapter answering
  `in_claim_scope(item_id)` (the supervisor stops reading parent links),
  renaming `seams.ado`, `[[boards]]` with `claim_scope` per entry, and a fleet
  name that `tag_prefix` derives from.

## Out of scope for this session

- The squadra GitHub adapter and everything deferred to it (above).
- `design-to-board` (T1) and any claude-skills plugin or runbook change.
- The claude-skills ledger: don't edit it from squadra. Report the PR URL;
  the next claude-skills session records W-SQ.

## Suggested skills

`grilling:grilling` only if the spec leaves a real gap; ask Rich before
guessing.

## Wrap-up

Run squadra's full test suite and linters, open the PR ready for review
(base `main`), and tell Rich the PR URL, what passed, and anything the spec
didn't cover. If you split, write
`~/Code/claude-skills/docs/wayfinder-port/handoffs/SQ2-…` content into your
final message for Rich to commit, rather than writing outside squadra.
