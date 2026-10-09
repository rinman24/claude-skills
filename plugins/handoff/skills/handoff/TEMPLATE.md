# Handoff: <session ID or short title> · <unit title>

Start a fresh `claude` session in `<worktree or repo path>` and give it this
file's path.

## Context

<One short paragraph: what the effort is, the branch, and anything about the
environment the next session must know (e.g. "never commit to main; fetch
first and merge `origin/main` if it moved").>

Read first, in order:
1. <the ledger, by path; it is the record and outranks this file>
2. <other artifacts by path or URL, naming the section when a file is long>

## The unit

Ledger items: <IDs, or "none (no ledger)">
Goal: <what "done" looks like>
First action: <the concrete first step>
Estimated work: <optional: tokens or time, against the session budget>

## Where this session left off

<What the ledger can't hold: the current hypothesis, work in flight,
approaches tried and dropped and why, gotchas. Bullets. Write "nothing beyond
the ledger" if that's true.>

## Decisions already made

<Bullets citing ledger decision IDs, ADRs or commits. Don't restate the
detail.>

## Out of scope

<Bullets. Optional.>

## Suggested skills

<Skill names, and when the next session should use each.>

## Wrap-up

<How the next session ends: e.g. "Follow the End steps of the session
protocol in the ledger, then run `/handoff`.">