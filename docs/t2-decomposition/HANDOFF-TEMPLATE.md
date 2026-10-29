# Handoff: <ID> · <unit title>

Copy to `docs/t2-decomposition/handoffs/<ID>-<slug>.md` (local under HD1, not committed) and fill in. Rich starts a fresh `claude` session in
`~/Code/claude-skills` and gives it this file (paste it, or send its path).

## Context

You are working on T2: enforcing Löwy's decomposition across wayfinder,
design-to-board and target repos. To start:

```
git fetch
git worktree add .claude/worktrees/<slug> -b <docs|feat>/t2-<slug> origin/main
```

Enter that worktree. Never commit to main.

Read first, in order:
1. `docs/t2-decomposition/LEDGER.md`: starting decisions, work items, open
   items.
2. `docs/t2-decomposition/LESSONS-LEARNED.md`.
3. <the other files this unit needs, by path and section>

## This session's unit

Ledger item: <ID>
Goal: <one or two lines on what "done" looks like>
Estimated work: ~<N>K tokens (budget under 100K total, hard stop at 120K)

## Decisions already made

<bullets citing ledger IDs (DB-D…, T2-D…) or a research report's Rulings table; don't restate detail>

## Out of scope

<bullets>

## Suggested skills

<e.g. domain-modeling:domain-modeling, adr:adr>

## Wrap-up

Follow the "End" steps of the session protocol in the ledger. Commit, push,
open a PR, write the next handoff, and tell Rich the PR, the handoff path and
what's open in his queue.
