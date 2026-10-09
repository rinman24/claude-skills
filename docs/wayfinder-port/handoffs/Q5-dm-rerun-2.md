# Handoff: Q5 · domain-modeling Step D 3 and 6 re-run (after S14)

Rich starts a fresh `claude` session in the worktree and pastes this whole file
as the first message. Start only after S14's PR
(https://github.com/rinman24/claude-skills/pull/7) has merged and Rich has run
`claude plugin marketplace update claude-skills` and
`claude plugin update domain-modeling@claude-skills`.

## Context

You are continuing the wayfinder + domain-modeling port on branch
`feat/wayfinder-domain-modeling` in `rinman24/claude-skills`. Work in the
worktree for that branch at `.claude/worktrees/wayfinder-domain-modeling`
(EnterWorktree with `path` if you aren't in it). Never commit to main. Fetch
first; if PR #7 merged, merge `origin/main` into the branch (don't rebase a
pushed branch).

Read first, in order:
1. `docs/wayfinder-port/LEDGER.md`: W8.8–W8.11, W10, MD-B6–B8
2. `docs/wayfinder-port/LESSONS-LEARNED.md`, especially Q4 and S14
3. `docs/domain-modeling-plugin-install-runbook.md` Step D 1, 3 and 6

## This session's unit

Ledger items: Q5 (Rich's queue: the post-S14 Step D 3 and 6 re-run).
First check `claude plugin list` shows `domain-modeling@claude-skills` at
0.1.1. Then walk Rich through Step D 2–3 in `~/Code/scratch/dm-smoke` and
Step D 6 in `~/Code/billet` on a throwaway branch (one batch is enough). Rich
runs them interactively in another terminal and pastes the replies; you check
them against the runbook and record pass or fail. What to look for:
- Step D 3 (W8.8): any proposed line, such as a `GLOSSARY-MAP.md` pointer, is
  shown word for word before the yes.
- Step D 6 (W8.9–W8.11): trim the batch list when it is shown (or under
  "Other"). A reply that isn't a yes gets `Approve … as drafted?`. "Run the
  final pass and Settle" gets a draft of the edits and rows, not a write.
  Settle's announcement is one 📝 list ending with a `Wording:` line, and
  text taken from Eric reads `you approved`, never `Eric approved`.
Goal: pass or fail for each check, recorded in the ledger; new defects logged
as W8.12+. Records results and fixes nothing.
Estimated work: ~25–40K (budget: under 100K total, hard stop at 120K).

## Decisions already made

- MD-B6, MD-B7, MD-B8 confirmed. The plugin is already updated to 0.1.1;
  just confirm `claude plugin list` shows it.
- The billet findings already in Rich's queue are his; don't re-log them.

## Out of scope for this session

- Fixing anything found (that's a new S-session), other plugins, squadra.

## Suggested skills

None.

## Wrap-up

Follow the "End" steps of the session protocol in the ledger. Before dropping
billet's throwaway branch, copy any finding about billet into Rich's queue.
Open a PR for the ledger changes, ready for review, and tell Rich its URL and
what's left in his queue.
