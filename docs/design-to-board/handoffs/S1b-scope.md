# Handoff: S1b · Scope design-to-board, continued (DB1)

Rich starts a fresh `claude` session in
`~/Code/claude-skills/.claude/worktrees/design-to-board` and gives it this
file.

## Context

You are working on `design-to-board` (T1) on branch `feat/design-to-board`
in `rinman24/claude-skills`, in the worktree
`~/Code/claude-skills/.claude/worktrees/design-to-board`. Never commit to
main. Fetch first; if `origin/main` moved, merge it in.

S1 ruled DBQ1 as DB-D1: board writes live in squadra behind
`queue_increment` / `withdraw_increment` / `increments_by_origin` and a new
`Lifecycle.WITHDRAWN`; design-to-board calls squadra's CLI and owns
validation, the Origin format `<map>:<ID>` and the translation table.
Most of the build is squadra work (Rich's queue, A–D); design-to-board's
own build is Juval's E (reader, validation, dry run), F (reconcile and
ordered queueing against squadra's fake provider) and its half of G.

Read first, in order:
1. `docs/design-to-board/LEDGER.md`: DB-D1 in Decisions, the annotated
   DBQ2–DBQ8, Rich's queue, work items (DB-W is new)
2. `docs/design-to-board/LESSONS-LEARNED.md` (S1 entries)
3. Only if a question needs it: `~/Code/board-knowledge/sessions/2026-10-09-juval-design-to-board-write-path.md`
   ("Sequencing", "Blocking questions") and
   `~/Code/board-knowledge/sessions/2026-10-09-eric-design-to-board-vocabulary.md`
   ("`Lifecycle.WITHDRAWN`", "Key becomes Origin", "Blocking questions").
   Grep the sections; don't read them whole.
4. `plugins/wayfinder/skills/wayfinder/DESIGN-FORMAT.md` (checks 6–13).
   squadra read-only, `~/Code/squadra` on `main`, only if a question needs it.

## This session's unit

Ledger items: DB1 (finish)
Goal: DBQ2–DBQ8 each ruled by Rich (or `dropped`) and recorded as DB-D2,
DB-D3, … in the ledger; the design-to-board build split into work items
DB2, DB3, … of ~80K or less, each with a one-line goal and its decisions,
ordered against squadra's A–D (F needs squadra C; G needs D); DB-W placed
before the validation unit; `handoffs/S2-<slug>.md` written for the first
build unit. Nothing is built.
Estimated work: ~40–60K tokens (budget: under 100K total, hard stop at 120K)

Order: DBQ3 first (it carries Juval's and Eric's blocking Q2s: withdrawing
an ACTIVE item, and a withdrawn row whose increment is DONE), then DBQ7
(Eric's blocking Q1: QUEUED vs held decides whether the verb stays
`queue_increment`), then DBQ2, DBQ4 (confirm what DB-D1 already answers),
DBQ5, DBQ6, DBQ8. One question at a time, each with your recommendation.
DBQ3, DBQ7, DBQ2 and DBQ4 unblock squadra's SQ2 (the verb contract), which
runs in parallel in squadra (`~/Code/squadra` `docs/board-writes/LEDGER.md`,
read-only from here): as soon as those four are recorded, commit and push,
and tell Rich SQ2 can start.
No advisor consultation is planned; if one becomes necessary, Rich types
the command, and budget ~30K for it (S1 lesson).

## Decisions already made

- DB-D1 (S1): write path, verbs, Origin, WITHDRAWN, cascade in wayfinder,
  sequencing A → B → C → E → F → D → G, GitHub first.
- WD13, WD14, WD21–WD23, WSQ1 in `docs/wayfinder-port/LEDGER.md`; don't
  reopen them unless Rich does. If Rich answers "yes" to Eric's blocking Q2
  (DONE rows withdrawn through a foundation's `Kind` cell), that reopens
  WD22: say so and let Rich decide.

## Out of scope for this session

- Building or prototyping anything; changes in squadra, wayfinder or
  domain-modeling (record them as work items or Rich's queue items).
- squadra activities A–D: Rich's, in squadra.

## Suggested skills

grilling:grilling (one question at a time).

## Wrap-up

Follow the "End" steps of the session protocol in the ledger: decisions and
work items recorded, DB1 `done`, Rich's queue updated, lessons appended,
`S2` handoff written, committed and pushed. Tell Rich the S2 handoff path
and what's in his queue.
