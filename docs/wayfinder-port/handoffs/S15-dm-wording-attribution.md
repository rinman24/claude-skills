# Handoff: S15 · domain-modeling `Wording:` attribution (W8.12)

Rich starts a fresh `claude` session in the worktree and pastes this whole file
as the first message. Start only after the Q5 ledger PR has merged.

## Context

You are continuing the wayfinder + domain-modeling port on branch
`feat/wayfinder-domain-modeling` in `rinman24/claude-skills`. Work in the
worktree for that branch at `.claude/worktrees/wayfinder-domain-modeling`
(EnterWorktree with `path` if you aren't in it). Never commit to main. Fetch
first; if the Q5 PR merged, merge `origin/main` into the branch (don't rebase
a pushed branch).

Read first, in order:
1. `docs/wayfinder-port/LEDGER.md`: W8.9, W8.12, Q5, MD-B6–B8
2. `docs/wayfinder-port/LESSONS-LEARNED.md`, especially S14 and Q5
3. `plugins/domain-modeling/skills/domain-modeling/SKILL.md` step 5 (the
   `Wording:` line) and `BOOTSTRAP.md` steps 4–6
4. `docs/domain-modeling-plugin-install-runbook.md` Step D 3

## This session's unit

Ledger items: W8.12
Goal: the `Wording:` line credits Eric only with the text he actually changed,
and puts his text beside the label where it differed (e.g. "you approved;
Eric's `_Avoid_` and map wording, his text: …; the pointer line Eric approved
unchanged"). The label rule from W8.9 stays. Bump `domain-modeling` to
0.1.2. Validate (`claude plugin validate .` and the plugin), then check
headless with `claude -p --resume` in a `mktemp -d "$TMPDIR/…"` scratch repo
(S14 lessons): a multi-write settle where Eric sharpens one line and approves
another unchanged.
Estimated work: ~15–25K tokens (budget: under 100K total, hard stop at 120K)

## Decisions already made

- W8.9's label rule (`you approved` for any text the user approved, Eric's
  included) holds; W8.12 is only about which text is credited to Eric.
- MD-B6, MD-B7, MD-B8 confirmed.

## Out of scope for this session

- Other plugins, billet, squadra, Rich's interactive re-run (that goes to his
  queue if needed).

## Suggested skills

None.

## Wrap-up

Follow the "End" steps of the session protocol in the ledger. Open a PR,
ready for review, and tell Rich its URL, that he updates the plugin after it
merges, and what's left in his queue.
