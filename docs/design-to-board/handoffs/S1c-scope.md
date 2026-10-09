# Handoff: S1c · Scope design-to-board, finished (DB1)

Rich starts a fresh `claude` session in
`~/Code/claude-skills/.claude/worktrees/design-to-board` and gives it this
file.

## Context

You are working on `design-to-board` (T1) on branch `feat/design-to-board`
in `rinman24/claude-skills`, in the worktree
`~/Code/claude-skills/.claude/worktrees/design-to-board`. Never commit to
main. Fetch first; if `origin/main` moved, merge it in.

S1 ruled the write path (DB-D1). S1b ruled withdrawal (DB-D2), QUEUED
landing (DB-D3), the Origin mapping and squadra's frozen verb contract
(DB-D4, after `/ask-juval`) and the parent and config rules (DB-D5). SQ2
(the verb contract) is unblocked and may be running in squadra in parallel.
Three questions remain: DBQ5, DBQ6 and DBQ8. Rich wants them put to
advisors before he rules. Each already has an S1b starting position in the
ledger.

Read first, in order:
1. `docs/design-to-board/LEDGER.md`: Decisions DB-D1–DB-D5, the open
   questions DBQ5, DBQ6, DBQ8 (with their S1b starting positions), work
   items (DB-W), Rich's queue
2. `docs/design-to-board/LESSONS-LEARNED.md` (S1 and S1b entries)
3. Only if a question needs it: `~/Code/board-knowledge/sessions/2026-10-09-juval-parent-and-lookup-scope.md`
   ("The contract to freeze in SQ2", "The test that discriminates"); grep,
   don't read whole. `plugins/wayfinder/skills/wayfinder/DESIGN-FORMAT.md`
   (checks 6–13). squadra read-only, `~/Code/squadra` on `main`.

## This session's unit

Ledger items: DB1 (finish)
Goal: DBQ5, DBQ6, DBQ8 ruled by Rich after the two consultations below and
recorded as DB-D6, DB-D7, …; the design-to-board build split into work items
DB2, DB3, … of ~80K or less, each with a one-line goal and its decisions,
ordered against squadra's SQ1–SQ5 (F needs SQ4, the CLI and rules; G needs
SQ5, the GitHub adapter); DB-W placed before the validation unit;
`handoffs/S2-<slug>.md` written for the first build unit. Nothing is built.
Estimated work: ~80K tokens (two consultations ~60K, rulings and split
~20K; budget under 100K total, hard stop at 120K)

Order:
1. At the start, ask Rich to type both consultations. You can't run
   `/ask-*` yourself. Paste-ready, below. Relay each answer verbatim per
   the ask skill. If the guard blocks the session-file write to
   `~/Code/board-knowledge/sessions/`, use a quoted shell heredoc
   (Rich OK'd this in S1b).
2. Rule DBQ5, DBQ8 (Juval's), then DBQ6 (Eric's), one question at a time,
   each with your recommendation updated by the advisor.
3. Split the build, then wrap up. If the consultations run long, stop after
   the rulings and leave the split for S1d rather than going past 120K.

`/ask-juval`:

```
/ask-juval design-to-board S1c, two questions before the build split (squadra's contract is frozen in DB-D4: queue_increment / withdraw_increment / increments_by_origin(), board-wide, A1–A3; DB-D2 refuses ACTIVE and DONE withdrawals; DB-D5 --parent on a map's first run).
(1) DBQ5: what does "fails loudly back to wayfinder" (WD14, WD18) mean concretely? Proposal: all-or-nothing. Every check (DESIGN-FORMAT 6–14, plus the board checks: DB-D2 refusals, missing/withdrawn/out-of-scope predecessor Origins, a map under more than one parent, a missing or conflicting --parent) runs before any write; every failure is collected; on any failure nothing is written, exit non-zero, one line per failure (check, row, reason, fix = "Revise the map in wayfinder"; design-to-board never patches the document). Writes go withdrawals first, then queues in dependency order; a crash mid-run recovers by re-running (A3 idempotency). Is all-or-nothing right given that board state can change between the check and the write (a tick claims an item in between)?
(2) DBQ8: WD13 says two AFK runs on one document give identical increments. Proposal: the translation is a deterministic script the skill calls; the model only invokes it and relays the report. Test: two runs from one document against the same starting state of squadra's fake provider, asserting identical squadra calls and an identical final board; a golden file for the dry-run plan; your 7 discriminating cases; ties broken by Order, then ID; titles and bodies from row fields only. Is that the right seam, and is it the right test?
```

`/ask-eric`:

```
/ask-eric design-to-board S1c, DBQ6. WD14 (docs/wayfinder-port/LEDGER.md) says the translator fails on "missing kind", but DESIGN-FORMAT (plugins/wayfinder/skills/wayfinder/DESIGN-FORMAT.md, Increments) and WD10 allow a blank Kind: Kind is `vertical (B<n>)`, `foundation → I<n>, …`, or blank, "as squadra's glossary defines them". Proposal: DESIGN-FORMAT holds; a blank Kind is a plain increment; only a non-blank Kind outside those two forms fails; WD14 is reworded to "unknown kind" (in DB-W, with WD14's stale "> 2 new services"). Does a blank Kind name a real concept in squadra's language (and if so, what is it called), or is it absence? And is "unknown kind" the right failure name in design-to-board's report?
```

## Decisions already made

- DB-D1–DB-D5 in the ledger. Don't reopen them unless Rich does.
- WD13, WD14, WD21–WD23, WSQ1 in `docs/wayfinder-port/LEDGER.md`; DBQ6 may
  reword WD14 (wording only, via DB-W). Don't reopen the others unless
  Rich does.

## Out of scope for this session

- Building or prototyping anything; changes in squadra, wayfinder or
  domain-modeling (record them as work items or Rich's queue items).
- squadra SQ1–SQ5: Rich's, in squadra.

## Suggested skills

grilling:grilling (one question at a time). `/ask-juval`, `/ask-eric` (Rich
types them).

## Wrap-up

Follow the "End" steps of the session protocol in the ledger: decisions and
work items recorded, DB1 `done`, Rich's queue updated, lessons appended,
`S2` handoff written, committed and pushed. Tell Rich the S2 handoff path
and what's in his queue.
