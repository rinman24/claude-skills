# Handoff: Q1 · Prototype placement, then walk Rich's queue

Rich starts a fresh `claude` session in the worktree and pastes this whole file
as the first message.

## Context

You are continuing the wayfinder + domain-modeling port on branch
`feat/wayfinder-domain-modeling` in `rinman24/claude-skills`. Work in the
worktree for that branch at `.claude/worktrees/wayfinder-domain-modeling`.
Run `git worktree list` first and enter it with EnterWorktree (`path`) if you
aren't in it. Never commit to main. Fetch first, and pull if the branch moved.
The marketplace is `claude-skills`; plugins install as `<plugin>@claude-skills`.
The branch isn't merged, so every plugin loads from this worktree with
`--plugin-dir plugins/<plugin>`, and its skills are `/<plugin>:<skill>`.

Read first, in order:
1. `docs/wayfinder-port/LEDGER.md`: Rich's queue, work items W6–W9, the
   WD-B table (WD-B14, WD-B15)
2. `docs/wayfinder-port/LESSONS-LEARNED.md` (S12: two `--plugin-dir` flags in
   one headless run; "next to what it prototypes" meant the map folder)
3. `plugins/wayfinder/skills/wayfinder/SKILL.md` (the **prototype** bullet
   and "What wayfinder writes") and the Resolution line in `MAP-FORMAT.md`

## This session's unit

Ledger items: W7, then Q1.

Goal, part 1 (W7, do this first): wayfinder tells `prototype` where to put a
prototype, so a pending prototype never sits inside the committed map folder.
- Add a ledger row **WD-B16** after WD-B15: "Pending prototypes live outside
  the map folder", Status `confirmed 2026-10-08 (Rich, after S12)`. Detail:
  with no app in the repo, S12's run put the prototype in
  `.scratch/wayfinder/<map>/`, so committing the map while a verdict was
  pending would commit it too and break MAP-FORMAT's folder contents. Rich
  chose `.scratch/prototypes/<map>/`, named after the ticket. Not gitignored,
  because `prototype` keeps a prototype by committing it to `prototype/<name>`.
- Prototype bullet in `SKILL.md`: when handing over, tell `prototype` to put
  the prototype under `.scratch/prototypes/<map>/`, named after the ticket
  (`<NN>-<slug>.prototype.html` for a single file), unless it has to sit
  inside the app (UI sub-shape A, a switcher on an existing page).
- Mention the location in "What wayfinder writes", and update the runbook's
  Step D 8 expectation.
- Validate (`claude plugin validate .`), then one headless check from the
  worktree root, on a toy map whose first frontier ticket is
  `Kind: prototype` (seed as in S12):
  `claude -p --plugin-dir plugins/wayfinder --plugin-dir plugins/prototype --permission-mode acceptEdits "/wayfinder:wayfinder <map>"`.
  Pass: the prototype lands in `.scratch/prototypes/<map>/`, nothing new is
  in `.scratch/wayfinder/<map>/` except the ticket's `in progress` status,
  and it hands over without picking. Delete the toy map and prototype.
- Commit and push before starting part 2.

Goal, part 2 (Q1): walk Rich through every open item in "Rich's queue", one
at a time, in the ledger's suggested order (confirmations first, then the
interactive checks, then "Elsewhere").
- For each item, say what it is and what Rich needs to do in two or three
  lines. For a confirmation, show the row's interpretation and your
  recommendation.
- For an interactive runbook check, give the exact command to start that
  session (with `--plugin-dir`) and what a pass looks like. Rich runs it in
  another terminal and reports back. Don't run interactive checks yourself.
- Wait for his answer before moving on. If he says "skip", leave the item
  unticked and move on.
- When he rules or reports, update the ledger right away: tick the item,
  record rulings in the table's Status column, and add any defect he finds
  as a new item for S13 under W8. Don't fix defects in this session.

Estimated work: W7 ~15K; Q1 ~30–50K, depending on how many checks Rich runs
(budget: under 100K total, hard stop at 120K). If the budget runs short,
stop at an item boundary; the next queue session picks up from the ledger.

## Decisions already made

- Rich's order: this session, then S13 for what comes up (W8), then the PR
  to main (W9). Ledger, work items.
- Prototype location: `.scratch/prototypes/<map>/` (Rich, after S12; becomes
  WD-B16).
- WD-B1–B13, MD-B1–B5 and AD-B1–B4 are confirmed; WD-B3 is `replaced (W6)`.
  WD-B14 and WD-B15 are unconfirmed and sit in the queue.

## Out of scope for this session

- Fixing anything the queue turns up (W8, S13).
- The PR to main (W9).
- Changes to `plugins/prototype`. If W7 seems to need one, record it and ask
  Rich first.
- `design-to-board` (T1), squadra (W-SQ beyond ticking what Rich reports),
  the map-format Services gap (S10 lessons).

## Suggested skills

None needed. Rich runs the interactive checks with the plugins under test.

## Wrap-up

Follow the "End" steps of the session protocol in the ledger. Write
`handoffs/S13-queue-follow-ups.md` covering W8 (every defect or change Q1
recorded), with W9 as the following unit. If Q1 found nothing to fix, write
the S13 handoff for W9 (the PR to main) instead. Tell Rich its path and what
is still open in his queue.
