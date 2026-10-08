# Handoff: S12 · Wire prototype tickets into wayfinder

Rich starts a fresh `claude` session in the worktree and pastes this whole file
as the first message.

## Context

You are continuing the wayfinder + domain-modeling port on branch
`feat/wayfinder-domain-modeling` in `rinman24/claude-skills`. Work in the
worktree for that branch at `.claude/worktrees/wayfinder-domain-modeling`.
Run `git worktree list` first and enter it with EnterWorktree (`path`) if you
aren't in it. Never commit to main. Fetch first, and pull if the branch moved.
The marketplace is `claude-skills`; plugins install as `<plugin>@claude-skills`.

Read first, in order:
1. `docs/wayfinder-port/LEDGER.md`: Rich's queue, W5 (its notes hold
   PD1–PD6), W6, WD7, the WD-B table
2. `docs/wayfinder-port/LESSONS-LEARNED.md` (S10 and S11: namespaced
   `/<plugin>:<skill>` under `--plugin-dir`, parallel headless runs, no `cd`)
3. `plugins/wayfinder/skills/wayfinder/SKILL.md` (the **prototype** bullet
   under "Ticket kinds", and "What wayfinder writes") and `MAP-FORMAT.md`
   (Resolution: assets are linked, never pasted)
4. `plugins/prototype/skills/prototype/SKILL.md`; skim `LOGIC.md` and `UI.md`

## This session's unit

Ledger items: W6
Goal: a wayfinder prototype ticket is resolved by calling the `prototype`
skill (Skill tool) instead of showing variants inline (WD-B3 replaced). The
user still picks (WD7, PD1). The Resolution links the prototype and records
the user's verdict. Update the prototype bullet, "What wayfinder writes" (the
prototype plugin writes its own files, so wayfinder no longer writes "exactly
two things"), the runbook and WD-B3's ledger entry. Headless check: Resolve on a toy map
whose first frontier ticket is `Kind: prototype` loads the prototype skill
and hands over without picking or closing the ticket.
Estimated work: ~25K tokens (budget: under 100K total, hard stop at 120K)

## Decisions already made

- WD7 and PD1–PD6 (ledger, W5 row): the verdict is always the user's; the
  prototype skill hands over and waits, even when another skill calls it;
  it's model-invocable for this purpose (PD6).
- WD-B3 is the interim behaviour this unit replaces.
- Check the WD-B table's Status column (ledger, after WD28) for Rich's
  rulings. Apply any overrule he has recorded; otherwise don't change them
  beyond WD-B3. When W6 lands, set WD-B3's Status to `replaced (W6)`.

## Out of scope for this session

- `design-to-board` (T1), squadra (W-SQ), new glossary terms.
- Changes to `plugins/prototype` beyond what wiring strictly needs; if one
  is needed, record it and ask Rich first.
- The map-format Services gap noted in S10's lessons (record only).

## Suggested skills

- `anthropic-skills:skill-creator` if the wiring needs a structural change.

## Wrap-up

Follow the "End" steps of the session protocol in the ledger. The next unit
is T1 (`design-to-board`), out of this port; if nothing else is `todo`,
say the port is finished instead of writing a handoff, and read out what is
still open in the ledger's "Rich's queue".
