# Handoff: S7 · Finish the wayfinder decisions and lay out W1…

Rich starts a fresh `claude` session in the worktree and pastes this whole file
as the first message.

## Context

You are continuing the wayfinder + domain-modeling port on branch
`feat/wayfinder-domain-modeling` in `rinman24/claude-skills`. Work in the
worktree for that branch at `.claude/worktrees/wayfinder-domain-modeling`.
Run `git worktree list` first; if it isn't there, create it with
`git worktree add .claude/worktrees/wayfinder-domain-modeling feat/wayfinder-domain-modeling`
and enter it with EnterWorktree (`path`). Never commit to main.
The marketplace is `claude-skills`; plugins install as `<plugin>@claude-skills`.

Read first, in order:
1. `docs/wayfinder-port/LEDGER.md`: especially the Wayfinder decisions
   WD1–WD12, the "Open for S7" list under them, and the S6 triage dispositions
2. `docs/wayfinder-port/LESSONS-LEARNED.md` (S6 entries: consult budget,
   absolute paths)
3. Advisor sessions in `/Users/richinman/Code/board-knowledge/sessions/`:
   read the "Named decision" and "Blocking questions" sections of
   `2026-10-06-juval-wayfinder-squadra-split.md`,
   `2026-10-06-eric-wayfinder-squadra-split.md` and
   `2026-10-06-eric-squadra-unit-name.md`; open an "## Answer" only where a
   question needs it

Upstream reference: https://github.com/mattpocock/skills @ `6fd9479`
(`skills/engineering/wayfinder/SKILL.md`, `docs/engineering/wayfinder.md`).
Clone into your scratchpad only if you need the text; S6's outline is in the
ledger. squadra: https://github.com/rinman24/squadra (README describes the
claim rule, `parent_scope_ids`, the runner's seams-then-fan-out). Rich is
renaming squadra's "slice" to "increment" in a separate session (W-SQ).

## This session's unit

Ledger items: W0 (part 2)
Goal: Rich confirms WD1–WD12 as a numbered summary; Q18 is decided after a
Juval consult; the rest of "Open for S7" is decided; W1… are in the ledger
with estimates and sessions (~80K each, with dependencies, `prototype`
blocking whatever needs it); the S8 handoff is written for W1.
Estimated work: ~60K tokens (budget: under 100K total, hard stop at 120K).
At most two advisor consults (lesson S6).

Suggested shape:
1. Load `/grilling`. Round 1 is the numbered WD1–WD12 summary for Rich to
   confirm or correct; include WD3's and WD8's proposed-but-unconfirmed parts
   (operation names Begin/Resolve/Revise/Publish; Eric's Revise additions).
2. **Consult Juval on Q18** (Rich asked for it): call the Agent tool with
   `subagent_type: board-juval`, passing Rich's Q18 instruction and Eric's
   blocking question 1 from `2026-10-06-eric-squadra-unit-name.md` verbatim,
   plus the three session files and the ledger as paths, with no framing of
   your own. Relay the answer verbatim under `## Juval Löwy`, then write
   `board-knowledge/sessions/2026-10-0X-juval-<topic>.md` in the ask-juval
   format (see `~/.claude/skills/ask-juval/SKILL.md`). Don't commit in
   board-knowledge.
3. Grill the rest of "Open for S7": over-charting rules (depend on Q18), board
   rules' new home, translator in scope or not, design document format, local
   board file format, parallel tickets, W-layout.
4. Record decisions in the ledger after Rich confirms the closing summary.

## Decisions already made

- GD1–GD7, MD1–MD13, MD-B1–B5, AD-B1–B4 (ledger). Rich still hasn't commented
  on MD-B or AD-B.
- WD1–WD12 (ledger), recorded in S6 but not yet confirmed as a closing summary.
  Key ones: wayfinder never touches a GitHub/ADO board (WD1); local committed
  board at `.scratch/wayfinder/<map>/`, `Ref` = `scratch:<path>`, which
  supersedes the round-1 GitHub answer (WD2); output is a design document;
  vocabulary per WD10 (`increment`, `design document`, `cleared`; `work` and
  `deliverable` retired); `subsystem` settled with `slice` / `vertical slice`
  rejected (WD12).

## Out of scope for this session

- Building any wayfinder or prototype plugin files.
- Writing the WD12 glossary row (lay it out as a W-item; it goes through
  `/domain-modeling` with Eric, MD6).
- Anything in squadra (Rich drives W-SQ).
- Changing `grilling`, `domain-modeling` or `adr`, unless Rich asks (then it's
  its own W-item).

## Suggested skills

- `grilling:grilling` (decision rounds; it writes nothing, you record after
  Rich confirms)

## Wrap-up

Follow the "End" steps of the session protocol in the ledger, including writing
the next handoff prompt and telling Rich its path.
