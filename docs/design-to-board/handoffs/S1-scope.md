# Handoff: S1 · Scope design-to-board (DB1)

Rich starts a fresh `claude` session in
`~/Code/claude-skills/.claude/worktrees/design-to-board` and gives it this
file.

## Context

You are starting `design-to-board` (T1 from the wayfinder port) on branch
`feat/design-to-board` in `rinman24/claude-skills`. Work in this worktree;
never commit to main. Fetch first; if `origin/main` moved, merge it in.

`design-to-board` transcribes a cleared wayfinder design document into
increments on squadra's board; it never designs (WD14). Wayfinder's Publish
step hands a document to it; squadra claims and builds what it creates.

Read first, in order:
1. `docs/design-to-board/LEDGER.md`: repo facts, work items, open questions
   DBQ1–DBQ8
2. `docs/design-to-board/LESSONS-LEARNED.md`
3. `docs/wayfinder-port/LEDGER.md`, decisions only: WD1, WD10, WD13, WD14,
   WD18, WD19, WD21–WD24, WD27, WD-B9 and WSQ1 (grep the IDs; don't read the
   whole file)
4. `plugins/wayfinder/skills/wayfinder/DESIGN-FORMAT.md` and the Publish
   step in `plugins/wayfinder/skills/wayfinder/SKILL.md`
5. Juval's list: `~/Code/board-knowledge/sessions/2026-10-07-juval-design-document-contract.md`,
   "What the translator validates"
6. squadra, read-only, only as far as DBQ1 and DBQ4 need: its README "Claim
   scope" section, `src/squadra/board.py` (`BoardAccess`, `PROVIDERS`) and
   `docs/design/board-provider-seam.md`. Use `~/Code/squadra` if `main`
   includes PR #42, else the `mandatory-claim-scope` worktree under it.
   Never write in squadra.

## This session's unit

Ledger items: DB1
Goal: every open question DBQ1–DBQ8 is a decision Rich has ruled (or
`dropped`), recorded in the ledger's Decisions table as DB-D1, DB-D2, …;
the build is split into work items DB2, DB3, … of ~80K or less, each with a
one-line goal and its decisions; and `handoffs/S2-<slug>.md` is written for
the first build unit. Nothing is built.
Estimated work: ~50–70K tokens (budget: under 100K total, hard stop at 120K)

Order: DBQ1 first; it decides DBQ2–DBQ4. Put each question to Rich with
your recommendation (one question at a time). DBQ1 is structural (where the
board's ResourceAccess lives, and whether squadra grows create/link
operations): offer Rich `/ask-juval` with the question written out for him
to paste after typing the command; he types the command himself. If a new
term needs settling (e.g. what "withdraw" names on a board), use
domain-modeling, which calls Eric.

## Decisions already made

- WD14: name, ResourceAccess role, validate-and-fail-loudly, never patch the
  document, honour claim scope. WD22: it only creates and withdraws.
  WD13: determinism is the test. WD21: it never reads the record.
  WD23: ≤ 2 changed services per increment. WSQ1: claim scope is mandatory
  in squadra; it must never set `tag_prefix` tags.
- All in `docs/wayfinder-port/LEDGER.md`; don't reopen them unless Rich does.

## Out of scope for this session

- Building or prototyping the skill, changes in squadra, wayfinder or
  domain-modeling (note any needed change as a work item instead).
- The squadra GitHub adapter itself (Rich's, in squadra), unless DBQ1 makes
  part of it a dependency: then it is a queue item for Rich.

## Suggested skills

grilling:grilling (Rich's rulings, one question at a time),
domain-modeling:domain-modeling (only if a term needs settling), and
`/ask-juval` typed by Rich for DBQ1.

## Wrap-up

Follow the "End" steps of the session protocol in the ledger: decisions and
work items recorded, Rich's queue updated, lessons appended, `S2` handoff
written, committed and pushed. Tell Rich the S2 handoff path and what's in
his queue.
