# Handoff: S13 · Fix what the queue walk turned up

Rich starts a fresh `claude` session in the worktree and pastes this whole file
as the first message. Start it only after Q2 has finished the queue walk; Q2
may have added W8 items to the ledger and to this file.

## Context

You are continuing the wayfinder + domain-modeling port on branch
`feat/wayfinder-domain-modeling` in `rinman24/claude-skills`. Work in the
worktree for that branch at `.claude/worktrees/wayfinder-domain-modeling`
(EnterWorktree with `path` if you aren't in it). Never commit to main. Fetch
first, and pull if the branch moved. Validate with `claude plugin validate .`.

Read first, in order:
1. `docs/wayfinder-port/LEDGER.md`: W8 and every W8.<n> row
2. `docs/wayfinder-port/LESSONS-LEARNED.md`
3. `plugins/domain-modeling/skills/domain-modeling/SKILL.md` ("Eric reviews
   every write", the no-Eric line) and `BOOTSTRAP.md`
4. `docs/domain-modeling-plugin-install-runbook.md` Step D

## This session's unit

Ledger items: W8.1–W8.4, plus any W8.<n> Q2 added.
- W8.1: runbook Step D 2 expects the objection from Claude's own challenge
  or from Eric.
- W8.2: any change to an Eric-reviewed wording (Eric's sharpening, or Claude
  diverging from his verdict) goes to the user as a question before it is
  written; the announcement says who approved each wording. In `SKILL.md`
  and `BOOTSTRAP.md` step 4 (Q1's billet bootstrap broke this three times).
- W8.3: `BOOTSTRAP.md` step 1 batches per top-level module, or per
  subsystem when the top-level directories are layers.
- W8.4: the no-Eric refusal doesn't offer a manual write that skips Eric.

Goal: each item fixed, validated, and checked headless where a one-turn
check exists (W8.4: run step 7's prompt with `board-eric` unavailable;
W8.2 is a second-turn behaviour, so add or sharpen a runbook step for Rich).
Estimated work: ~20–30K (budget: under 100K total, hard stop at 120K).

## Decisions already made

- Each W8 row's notes record Rich's call to log it (Q1, 2026-10-08).
- MD-B2 (Eric advises, Rich decides) is the rule W8.2 enforces; it is
  confirmed, not reopened.

## Out of scope for this session

- The PR to main (W9): the next unit.
- New features; anything not listed as a W8 row.

## Suggested skills

None.

## Wrap-up

Follow the "End" steps of the session protocol in the ledger. Write
`handoffs/W9-pr-to-main.md` for the PR to main and marketplace install, and
tell Rich its path and anything left in his queue (e.g. re-running a
runbook step a fix touched).
