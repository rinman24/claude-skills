# Handoff: S<N> · <unit title>

Copy to `S<N>-<slug>.md`. Paste the whole file as the first prompt of the new
session, or point `/handoff` at it.

## Context

You are continuing the wayfinder + domain-modeling port on branch
`feat/wayfinder-domain-modeling` in `rinman24/claude-skills`. Work in the
existing worktree for that branch (or create one from it); never commit to main.

Read first, in order:
1. `docs/wayfinder-port/LEDGER.md` (status, budget, session protocol)
2. `docs/wayfinder-port/LESSONS-LEARNED.md`
3. <any other files this unit needs, by path>

Upstream reference: https://github.com/mattpocock/skills (clone shallow into
the job temp dir if you need to read it; don't vendor it into the repo).

## This session's unit

Ledger items: <IDs>
Goal: <one or two lines on what "done" looks like>
Estimated work: ~<N>K tokens (budget: under 100K total, hard stop at 120K)

## Decisions already made

<bullets, each linking the ledger item or file that records it; don't restate detail>

## Out of scope for this session

<bullets>

## Suggested skills

<e.g. anthropic-skills:skill-creator, anthropic-skills:grill-me>

## Wrap-up

Follow the "End" steps of the session protocol in the ledger.
