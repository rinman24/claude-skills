# Handoff: Q3 · Ask Juval whether squadra's claim scope becomes mandatory

Rich starts a fresh `claude` session in the worktree and pastes this whole file
as the first message. Run it before S13: both edit `LEDGER.md`.

## Context

You are continuing the wayfinder + domain-modeling port on branch
`feat/wayfinder-domain-modeling` in `rinman24/claude-skills`. Work in the
worktree for that branch at `.claude/worktrees/wayfinder-domain-modeling`.
Run `git worktree list` first and enter it with EnterWorktree (`path`) if you
aren't in it. Never commit to main. Fetch first, and pull if the branch moved.

Read first, in order:
1. `docs/wayfinder-port/LEDGER.md`: Rich's queue (W-SQ), the W-SQ and T1
   rows, Q2's notes, decisions WD14 and WD18
2. `docs/wayfinder-port/LESSONS-LEARNED.md` (S6/S7: answer an advisor's
   factual blocking question yourself; Q2)

## This session's unit

Ledger item: Q3 (decides how much of W-SQ is left).

W-SQ is the squadra side of WD18: "squadra claims by positive scope;
`squadra tick --dry-run` contract test". Q2 traced both in `~/Code/squadra`
(`main` at `d9d2afa`, PR #41) and found most of it there:

- Scope: `[board].parent_scope_ids` (env `FLEET_PARENT_SCOPE_IDS`, legacy
  `FLEET_EPIC_IDS`) limits claims to children of the listed parents. It is
  opt-in: the default and the scaffold are `[]`, which makes every unblocked
  `queued` item in the project claimable.
- Dry run: `tests/test_supervisor_dry_run.py` checks a dry-run tick mutates
  nothing and reports every would-be action; `tests/test_cli.py` checks
  `tick --dry-run` reaches the tick. Nothing runs the real CLI end to end
  against a board fixture and asserts the claim set.

Rich's question for Juval: should positive scope become mandatory?

Steps:
1. Load the facts into this conversation by reading them, so `/ask-juval`
   can pass them along verbatim (the skill passes "facts from this
   conversation" as they are). Read, with absolute paths and no `cd`:
   - `~/Code/squadra/README.md`: the `[board]` config table and example
     (around lines 90–110), "Scoping" (around 392–396), "Activation (manual,
     opt-in)" (around 436–450)
   - `~/Code/squadra/src/squadra/config.py` `_resolve_parent_scope_ids`
     (around 192–209)
   - `~/Code/squadra/src/squadra/engines.py` `_classify` (around 107–135),
     the claim ladder
   - `~/Code/squadra/src/squadra/scaffold.py` around line 101
     (`parent_scope_ids = []`)
   - `~/Code/squadra/tests/test_supervisor_claim.py` around line 324 (the
     scope test) and the test names in `tests/test_supervisor_dry_run.py`
   - the ledger's WD14, WD18 and T1 text
   Re-check squadra's `main` first (`git -C ~/Code/squadra fetch` and log);
   if it moved past `d9d2afa`, re-read what changed.
2. Ask Rich one factual question before the consult, since Juval will likely
   need it: where does the fleet run today (which host and board), and does
   any live `squadra.toml` there leave `parent_scope_ids` empty? Q2 found no
   `squadra*.toml` under `~/Code` or `~/.config` on his Mac.
3. Tell Rich to type this himself (`ask-juval` sets
   `disable-model-invocation`, so you can't call it):

   ```
   /ask-juval Should squadra make positive claim scope mandatory now? Today `[board].parent_scope_ids` is optional, and empty means every unblocked queued item in the project is claimable. "Mandatory" could be (a) a config-load check that rejects an empty scope unless the operator explicitly opts into the whole project, or (b) a positive per-item tag (e.g. `fleet:ready`) that every writer must set. The alternative is to keep it opt-in until `design-to-board`, the only planned automated writer to the board, is designed. Which, and when?
   ```

   Pass Rich's step 2 answer along as a fact. Add no opinion of your own: the
   advisor answers blind. The skill relays the answer verbatim and writes
   `~/Code/board-knowledge/sessions/<date>-juval-<topic>.md` (not committed).
   If Juval asks a factual blocking question, answer it from squadra or the
   ledger yourself where you can, and continue the same `board-juval` agent
   with SendMessage rather than starting a new one.
4. Put the decision to Rich: Juval's named decision, plus one question per
   choice his answer leaves open (e.g. which shape, (a) or (b); now or at T1;
   whether the CLI-level dry-run contract test pins "no scope, no claims").
   Recommend, don't survey.
5. Record Rich's ruling as a new decision row (`WSQ1`) after WD-B16 in the
   Decisions table, and set W-SQ's remaining scope:
   - **No** (stay opt-in): tick W-SQ in Rich's queue, set the W-SQ row
     `done`, and add a T1 prerequisite: the board `design-to-board` publishes
     to must set `parent_scope_ids`.
   - **Yes (with Juval's mods)**: W-SQ stays `in progress`; write the squadra
     requirement precisely in its row (shape, error text or tag, migration for
     an empty scope, the contract test it adds). The squadra work itself is
     Rich's, in squadra.
   Offer to write Rich's choice into the session file's "Choice" section.

Estimated work: ~20–30K (Juval's verbatim answer is long). Budget: under
100K total, hard stop at 120K.

## Decisions already made

- WD18: wayfinder writes nothing to a board; the positive-scope and dry-run
  contract-test requirements belong to squadra (W-SQ).
- Rich (Q2, 2026-10-08): ask Juval before deciding W-SQ's remaining scope.
- Rich's order after Q3: S13 (`handoffs/S13-queue-follow-ups.md`, W8.1–W8.7),
  then the PR to main (W9).

## Out of scope for this session

- Any change to squadra's code or docs (Rich's, in squadra).
- W8 fixes (S13), the PR to main (W9), `design-to-board` (T1).

## Suggested skills

`/ask-juval` (Rich types it).

## Wrap-up

Follow the "End" steps of the session protocol in the ledger. The next
handoff is the existing `handoffs/S13-queue-follow-ups.md`; don't write a new
one unless Q3 changes S13's scope. Tell Rich its path and what is still open
in his queue.
