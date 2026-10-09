# Handoff: S3 · Domain-modeling skill (outline, issues, feedback, then build)

Rich starts a fresh `claude` session in the worktree and pastes this whole file
as the first message.

## Context

You are continuing the wayfinder + domain-modeling port on branch
`feat/wayfinder-domain-modeling` in `rinman24/claude-skills`. Work in the
worktree for that branch at `.claude/worktrees/wayfinder-domain-modeling`.
Run `git worktree list` first; if it isn't there, create it with
`git worktree add .claude/worktrees/wayfinder-domain-modeling feat/wayfinder-domain-modeling`
and enter it with EnterWorktree (`path`). Never commit to main.
The marketplace is `claude-skills`; plugins install as `<plugin>@claude-skills`
(see the ledger's "Repo facts").

Domain-modeling comes next because wayfinder's default ticket type is
"grilling + domain-modeling", and grilling shipped in S2.

Read first, in order:
1. `docs/wayfinder-port/LEDGER.md` (status, budget, session protocol, the
   grilling decisions GD1–GD7, "Inputs to triage")
2. `docs/wayfinder-port/LESSONS-LEARNED.md` (S2 has the `--plugin-dir`
   smoke-test recipe and the guard's limits)
3. `plugins/grilling/` and `docs/grilling-plugin-install-runbook.md` (the
   most recent house example; it credits upstream MIT with a copied LICENSE)

Upstream reference: https://github.com/mattpocock/skills, pinned at commit
`6fd9479`. Shallow-clone it into your job temp dir; don't vendor it into the
repo. Upstream files for this unit:

- `skills/engineering/domain-modeling/SKILL.md`, `GLOSSARY-FORMAT.md`,
  `ADR-FORMAT.md`: the skill and its bundled formats
- `docs/engineering/domain-modeling.md`: human docs; "Common questions" holds
  the author's known issues
- `.agents/invocation.md` ("Passive vs active domain work" section)
- `.out-of-scope/` (grep for glossary, ADR, domain) and `CHANGELOG.md` (grep
  for `domain-modeling`, `GLOSSARY`, `ADR`)
- Grep the skill for `docs/agents/` and `setup-matt-pocock-skills`; each hit
  needs a replacement this repo owns (ledger: Goal, S1 lesson)

## This session's unit

Ledger items: M1, M2
Goal: `plugins/domain-modeling` built from Rich's M1 decisions, validated and
smoke-tested via `--plugin-dir`.
Estimated work: ~75K tokens (budget: under 100K total, hard stop at 120K)

Same shape as S2, and do not skip the stop in step 3.

1. **Outline Matt's approach** briefly: what counts as active vs passive domain
   work, what goes in `GLOSSARY.md` / `GLOSSARY-MAP.md`, the ADR gates, and how
   it runs alongside grilling.
2. **List the author's issues**, one line each with a source path, split into
   "known defect" and "request the author rejected". The ledger's triage list
   already names some: glossary bloats into a spec, no tracker lookup for
   settled terms (#717), ADR format bundled (#557), slow brownfield bootstrap.
3. **Stop and ask Rich**, in grilling round format, before writing any skill
   file. Questions worth raising, without deciding them:
   - Name: plain `domain-modeling`, or something else?
   - Where the docs live in this repo's projects, and whether ADRs use the
     bundled format or one Rich already uses (the injected
     `architecture-closed` canon may matter here).
   - How it fits GD7: grilling writes no files, so domain-modeling owns every
     doc write when the two run together.
   - Whether to port `grill-with-docs` as a thin wrapper now (GD2 deferred it)
     or leave it to wayfinder.
   Record Rich's answers as decisions (MD1…) in the ledger before building.
4. **Build it** only after Rich has responded, and only if the session is
   under ~70K at that point; otherwise wrap up and write an S4 handoff for the
   build. Match `plugins/grilling`: manifest, SKILL.md plus any format files,
   upstream LICENSE copy, a marketplace entry, a README section, and
   `docs/domain-modeling-plugin-install-runbook.md`. Run
   `claude plugin validate .` and a headless smoke test.

## Decisions already made

- Grilling decisions GD1–GD7 (ledger: Decisions). GD7 (grilling never writes
  code or edits files) is the one that touches this unit.
- No dependency on `setup-matt-pocock-skills` (ledger: Goal).
- One plugin per skill; marketplace name `claude-skills`.
- Handoffs are plain prompt files (ledger: How sessions hand off).

## Out of scope for this session

- wayfinder, research, prototype, to-spec, to-tickets (note anything that
  affects them in the ledger's "Inputs to triage").
- Changing `plugins/grilling`, unless Rich's interactive smoke test (G2 notes)
  found a defect.

## Suggested skills

- `grilling:grilling` (for the step 3 round, if installed)

## Wrap-up

Follow the "End" steps of the session protocol in the ledger, including writing
the next handoff prompt and telling Rich its path.
