# Handoff: S10 · Smoke-test `plugins/wayfinder`

Rich starts a fresh `claude` session in the worktree and pastes this whole file
as the first message.

## Context

You are continuing the wayfinder + domain-modeling port on branch
`feat/wayfinder-domain-modeling` in `rinman24/claude-skills`. Work in the
worktree for that branch at `.claude/worktrees/wayfinder-domain-modeling`.
Run `git worktree list` first and enter it with EnterWorktree (`path`) if you
aren't in it. Never commit to main. Fetch first, and pull if the branch moved.
If S11's prototype branch has merged in, note it but don't touch
`plugins/prototype`.
The marketplace is `claude-skills`; plugins install as `<plugin>@claude-skills`.

Read first, in order:
1. `docs/wayfinder-port/LEDGER.md`: W3, W4, WD28, WD-B1–B10
2. `docs/wayfinder-port/LESSONS-LEARNED.md` (S2 and S4: headless smoke tests
   as one bare `claude -p --plugin-dir …` from the worktree root, with
   `--permission-mode acceptEdits` when files must be written; S9: no `cd`)
3. `plugins/wayfinder/skills/wayfinder/SKILL.md`, `MAP-FORMAT.md`,
   `DESIGN-FORMAT.md`
4. `docs/wayfinder-plugin-install-runbook.md` Step D

## This session's unit

Ledger items: W4
Goal: headless checks of runbook Step D 1 (Begin writes a map), 3 (Resolve
takes one ticket) and 5 (Publish writes a cleared design document, or names a
failing check) on a toy map. Fix any skill defect found and re-run the step
that showed it. List Step D 2, 4, 6 and 7 for Rich as interactive checks.
Estimated work: ~40K tokens (budget: under 100K total, hard stop at 120K).

Notes for the runs:
- Headless is one turn, and Begin starts with a grilling round. So give the
  destination, behaviours, increments and first tickets in the prompt, and
  say "these are my answers; write the map". Otherwise Begin stops at its
  questions. That run tests the write path. A run without answers tests that
  it asks first.
- Use a toy destination from this repo's own domain (S4 lesson). For example:
  "a `/handoff` skill that writes the next session's prompt from the ledger".
- `--plugin-dir` takes one path per flag. Load `plugins/wayfinder`,
  `plugins/grilling` and `plugins/domain-modeling`.
- To test Publish without running every ticket, seed a toy map by hand (all
  tickets closed, Fog empty) under `.scratch/wayfinder/<toy>/`. Delete the
  toy map and any `docs/design/` output before committing.

## Decisions already made

- Everything in the ledger through WD28; the build interpretations
  WD-B1–B10 aren't confirmed yet, so if a smoke run shows one is wrong,
  record it and ask Rich.

## Out of scope for this session

- Prototype wiring (W6), `design-to-board` (T1), anything in
  `plugins/prototype` or squadra.
- New glossary terms (they need an Eric consult and Rich).

## Suggested skills

- None needed beyond reading the plugin; `anthropic-skills:skill-creator` if
  a defect needs a structural fix.

## Wrap-up

Follow the "End" steps of the session protocol in the ledger. The next handoff
is `handoffs/S12-prototype-wiring.md` for W6 (W5 merged in PR #3);
write it from the ledger's W6 row and WD-B3, and
tell Rich its path.
