# Handoff: S9 · Build `plugins/wayfinder`

Rich starts a fresh `claude` session in the worktree and pastes this whole file
as the first message. S11 (W5, prototype) may be running in parallel on its own
branch; don't touch `plugins/prototype` or its ledger row.

## Context

You are continuing the wayfinder + domain-modeling port on branch
`feat/wayfinder-domain-modeling` in `rinman24/claude-skills`. Work in the
worktree for that branch at `.claude/worktrees/wayfinder-domain-modeling`.
Run `git worktree list` first; enter it with EnterWorktree (`path`) if you
aren't in it. Never commit to main. Fetch first: if S11's PR has merged into
this branch, pull it before editing the ledger.
The marketplace is `claude-skills`; plugins install as `<plugin>@claude-skills`.

Read first, in order:
1. `docs/wayfinder-port/LEDGER.md`: W3, WD1–WD27 (WD27 is new: glossary layout)
2. `docs/wayfinder-port/LESSONS-LEARNED.md` (S2: `--plugin-dir` smoke tests;
   S7/S8: no `cd` outside the worktree; consult budgeting)
3. `plugins/wayfinder/GLOSSARY.md`, `GLOSSARY-MAP.md`, `GLOSSARY-SETTLED.md`
   (the skill's prose must use these terms: Map, Errand, Subsystem, Increment)
4. House pattern: `plugins/domain-modeling/` (manifest, LICENSE, skill layout)
   and `docs/local-backlog-plugin-install-runbook.md`
5. Upstream wayfinder at https://github.com/mattpocock/skills (shallow clone
   into the job temp dir; don't vendor it)

## This session's unit

Ledger items: W3
Goal: `plugins/wayfinder` exists and validates. That means:
- `SKILL.md`: Chart with Begin / Resolve / Revise / Publish, per WD3–WD9,
  WD15, WD17, WD19, WD22–WD23. It says positively that wayfinder writes only
  the map and the design document.
- `MAP-FORMAT.md` (WD26) and `DESIGN-FORMAT.md` (WD21).
- `.claude-plugin/plugin.json`, the upstream MIT `LICENSE`, the marketplace
  entry and a README section.
- A runbook.

Finish with `claude plugin validate .`. The smoke test is W4 (S10), not this
session.
Estimated work: ~80K tokens (budget: under 100K total, hard stop at 120K). This
is tight, so if the build looks bigger, split W3 in the ledger (e.g. formats
first, SKILL.md second) before starting, and write the handoff for the rest.

## Decisions already made

- WD1–WD26 (ledger, confirmed by Rich in S7); WD27 (S8): glossary contexts and
  layout, `plugins/wayfinder/GLOSSARY.md` already exists, so keep it.
- Vocabulary: WD3 (no "work"), WD10 (amended), WD19 (map, no board), WD25
  (`errand`), and the settled rows in `GLOSSARY-SETTLED.md`.
- Wayfinder calls domain-modeling for Lookup and Settle (MD11); Settle gets
  `scratch:<path>` as its `Ref` (WD2).
- MD6/MD-B2: any new glossary term (WD10's `design document`,
  `decision ticket`, `cleared`, plus research vs decision ticket, which Eric
  left to W3) goes through `board-eric` and Rich before it is written. Budget
  ~10K per consult; batch the terms into one consult.

## Out of scope for this session

- Smoke testing (W4, S10); prototype wiring (W6); `design-to-board` (T1).
- Anything in `plugins/prototype` (W5, S11) or squadra.

## Suggested skills

- `anthropic-skills:skill-creator` (skill structure)
- `domain-modeling:domain-modeling` (only if new terms get settled)

## Wrap-up

Follow the "End" steps of the session protocol in the ledger. The next handoff
is `handoffs/S10-wayfinder-smoke.md` for W4; tell Rich its path.
