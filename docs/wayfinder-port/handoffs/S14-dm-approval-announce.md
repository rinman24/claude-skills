# Handoff: S14 · domain-modeling approval and announcement fixes (W8.8–W8.11)

Rich starts a fresh `claude` session in the worktree and pastes this whole file
as the first message.

## Context

You are continuing the wayfinder + domain-modeling port on branch
`feat/wayfinder-domain-modeling` in `rinman24/claude-skills`. Work in the
worktree for that branch at `.claude/worktrees/wayfinder-domain-modeling`
(EnterWorktree with `path` if you aren't in it). Never commit to main. Fetch
first; if the Q4 ledger PR merged, merge `origin/main` into the branch (don't
rebase a pushed branch). Validate with `claude plugin validate .`.

The five port plugins are installed from the marketplace (user scope, 0.1.0).
Headless checks of the fix use `--plugin-dir plugins/domain-modeling` in a
scratch repo under the job temp dir; the installed plugin only changes after
this unit's PR merges and Rich updates it (his queue).

Read first, in order:
1. `docs/wayfinder-port/LEDGER.md`: W8.8–W8.11, W10, MD-B2, MD-B6, MD-B7
2. `docs/wayfinder-port/LESSONS-LEARNED.md`, especially S13 and Q4
3. `plugins/domain-modeling/skills/domain-modeling/SKILL.md` ("Eric reviews
   every write", "Writing a term" step 5) and `BOOTSTRAP.md` steps 4–6
4. `docs/domain-modeling-plugin-install-runbook.md` Step D 3 and 6

## This session's unit

Ledger items: W10 (W8.8–W8.11).
- W8.8: before asking for a yes, show the exact text of any line to be
  written, including structural lines (a `GLOSSARY-MAP.md` pointer) and
  pointers in other docs.
- W8.9: in a bootstrap's later announcements, a wording the user accepted
  from Eric is `you approved` plus Eric's text, never `Eric approved`.
- W8.10: `BOOTSTRAP.md` step 6's Settle write gets a full
  `📝 Written since last round:` list with a `Wording:` line.
- W8.11 (MD-B7): write only on an explicit yes to the shown draft; any other
  reply gets one line, "Approve … as drafted?", first. Also fix runbook Step
  D 6 so the trim line is given when the batch list is shown (or typed as
  'Other' on its question).
Goal: the four rows are fixed and validated; a headless single-term check
shows the W8.8 pointer text before the yes. The bootstrap fixes can't be
fully checked headless; they go to Rich's queue as a Step D 6 re-run after
the merge and update.
Estimated work: ~20–30K (budget: under 100K total, hard stop at 120K).

## Decisions already made

- MD-B7 (Rich, Q4): only an explicit yes approves a draft.
- MD-B6 still holds: advance acceptance in so many words counts as approval.
- S13 lesson: show the target shape (a sample line) rather than a stronger
  adjective; after tightening a rule, re-read every runbook step against it
  (Step D 1's one-turn write must still pass).

## Out of scope for this session

- Other plugins, and billet itself (its findings are Rich's queue items).
- squadra (SQ1).

## Suggested skills

`anthropic-skills:skill-creator` for the edits if useful; nothing else.

## Wrap-up

Follow the "End" steps of the session protocol in the ledger. Open a PR from
`feat/wayfinder-domain-modeling` to `main`, ready for review, and add to
Rich's queue: merge, `claude plugin marketplace update claude-skills`,
`claude plugin update domain-modeling@claude-skills`, then re-run Step D 3
and 6. Tell Rich the PR URL and what's left in his queue.
