# Handoff: Q2 · Finish walking Rich's queue

Rich starts a fresh `claude` session in the worktree and pastes this whole file
as the first message.

## Context

You are continuing the wayfinder + domain-modeling port on branch
`feat/wayfinder-domain-modeling` in `rinman24/claude-skills`. Work in the
worktree for that branch at `.claude/worktrees/wayfinder-domain-modeling`.
Run `git worktree list` first and enter it with EnterWorktree (`path`) if you
aren't in it. Never commit to main. Fetch first, and pull if the branch moved.
The branch isn't merged, so every plugin loads from this worktree with
`--plugin-dir <worktree>/plugins/<plugin>` (absolute path when Rich runs it
from another repo), and its skills are `/<plugin>:<skill>`.

Read first, in order:
1. `docs/wayfinder-port/LEDGER.md`: Rich's queue, work items Q1, Q2, W8–W8.4
2. `docs/wayfinder-port/LESSONS-LEARNED.md` (Q1: the queue-walk lessons)
3. The runbook Step D of each open interactive check, as you reach it

## This session's unit

Ledger item: Q2 (the rest of Q1's queue walk).
Goal: walk Rich through every open item in "Rich's queue", one at a time, in
this order, same rules as Q1:
1. adr Step D 3–5 (`docs/adr-plugin-install-runbook.md`). Q1 had just given
   Rich step 3 when it stopped: in `~/Code/billet` on a throwaway branch
   `scratch/adr-check`, run the Postgres/DynamoDB decision from step 1.
   billet's house convention: `docs/adr/adr-NNNN-<slug>.md`,
   `# ADR-NNNN: <title>`, sections Status / Context / Decision /
   Consequences / Alternatives considered; latest is 0015, so pass is
   `adr-0016-<slug>.md` in that template with short sections, no new
   directory. Ask Rich whether he already ran it. Step 4 can run in
   `~/Code/scratch/dm-smoke` (no ADRs). Step 5 needs both plugins:
   `--plugin-dir …/plugins/domain-modeling --plugin-dir …/plugins/adr`.
2. wayfinder Step D 8, the verdict half. Rich needs a map with a prototype
   ticket waiting for its verdict: seed a toy map in a scratch repo (Q1 used
   `queue-page`: ticket 01 a UI `Kind: prototype` question, ticket 02 a
   grilling ticket blocked by 01), have Rich run Resolve with
   `--plugin-dir …/plugins/wayfinder --plugin-dir …/plugins/prototype`, then
   give a verdict. Pass per the runbook, plus WD-B16: the prototype sat in
   `.scratch/prototypes/<map>/`, and nothing is left there unless kept on a
   `prototype/<name>` branch.
3. prototype Step D 6: only if a repo with a web UI exists; otherwise Rich
   will likely skip.
4. Elsewhere: G3 (retire `anthropic-skills:grill-me` in claude.ai), W-SQ.

Rules: for each item, two or three lines on what it is and what Rich does;
exact command with `--plugin-dir`; what a pass looks like. Rich runs it in
another terminal and pastes the result. Check written files yourself when
you can. Wait for his answer; "skip" leaves the item unticked. Tick items and
record defects as new W8.<n> rows right away; fix nothing.

Estimated work: ~40–60K. Pasted interactive output is expensive: ask Rich to
paste only the reply that decides the check. Stop at an item boundary if
the context nears ~100K.

## Decisions already made

- Rich's order: Q2, then S13 (W8; `handoffs/S13-queue-follow-ups.md` is
  already written and Q2 adds to it), then the PR to main (W9).
- WD-B14–B16 confirmed (ledger, Decisions table).

## Out of scope for this session

- Fixing W8 items (S13).
- The PR to main (W9), `design-to-board` (T1), squadra beyond ticking W-SQ.

## Suggested skills

None. Rich runs the interactive checks with the plugins under test.

## Wrap-up

Follow the "End" steps of the session protocol in the ledger. Update
`handoffs/S13-queue-follow-ups.md` with any W8 items Q2 added (if none were
added at all, S13 still has W8.1–W8.4). Tell Rich its path and what is
still open in his queue.
