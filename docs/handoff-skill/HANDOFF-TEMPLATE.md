# Handoff: H<N> · <unit title>

`/handoff` fills this in as `handoffs/H<N>-<slug>.md` (git-ignored, HD1).
Rich starts a fresh `claude` session in the worktree and gives it that path.

## Context

You are working on the `handoff` plugin on branch `feat/handoff-skill`
in `rinman24/claude-skills`, in the worktree
`~/Code/claude-skills/.claude/worktrees/handoff-skill`. Never commit to
main. Fetch first; if `origin/main` moved, merge it in.

Read first, in order:
1. `docs/handoff-skill/LEDGER.md` (status, budget, protocol, open questions)
2. `docs/handoff-skill/LESSONS-LEARNED.md`
3. <any other files this unit needs, by path>

## This session's unit

Ledger items: <IDs>
Goal: <what "done" looks like>
First action: <the concrete first step>
Estimated work: ~<N>K tokens (budget: under 100K total, hard stop at 120K)

## Where this session left off

<What the ledger can't hold: current hypothesis, work in flight, approaches
tried and dropped and why, gotchas. Or "nothing beyond the ledger".>

## Decisions already made

<bullets citing ledger IDs; don't restate detail>

## Out of scope for this session

<bullets>

## Suggested skills

<e.g. grilling:grilling, domain-modeling:domain-modeling>

## Wrap-up

Follow the "End" steps of the session protocol in the ledger, including
running `/handoff` for the next session and telling Rich its path.
