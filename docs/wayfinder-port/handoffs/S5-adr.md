# Handoff: S5 · Build `plugins/adr`

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

Read first, in order:
1. `docs/wayfinder-port/LEDGER.md` (status, budget, session protocol, MD3,
   and MD-B1–B5 if Rich has comments on them)
2. `docs/wayfinder-port/LESSONS-LEARNED.md` (S2 and S4: the `--plugin-dir`
   smoke-test recipe, `--permission-mode acceptEdits` for writes)
3. `plugins/grilling/` and `plugins/domain-modeling/` (house examples; the
   latter's "Decisions that need an ADR" section is the caller of this skill)
4. `docs/domain-modeling-plugin-install-runbook.md` (runbook shape)

Upstream reference: https://github.com/mattpocock/skills, pinned at commit
`6fd9479`. Clone it into your session scratchpad; don't vendor it into the
repo. Files for this unit: `skills/engineering/domain-modeling/ADR-FORMAT.md`
(adapt) and `LICENSE` (copy). Also skim upstream's
`docs/engineering/domain-modeling.md` "Common questions" for ADR issues
(upstream #557 split ADRs out).

## This session's unit

Ledger items: A1
Goal: `plugins/adr` built from MD3, validated with `claude plugin validate .`,
and smoke-tested headless via `--plugin-dir`.
Estimated work: ~35K tokens (budget: under 100K total, hard stop at 120K)

Deliverables (match `plugins/domain-modeling`):
- `.claude-plugin/plugin.json`, upstream `LICENSE` copy.
- `skills/adr/SKILL.md`: upstream's three gates (hard to reverse, surprising
  without context, a real trade-off; skip the ADR if any is missing),
  upstream's minimal format, and "follow the repo's existing ADR convention
  if one exists" (detect location, numbering and template before writing).
  Model-invocable, so domain-modeling can call it via the Skill tool.
- `ADR-FORMAT.md` adapted from upstream if SKILL.md would otherwise grow.
- Marketplace entry, README section, `docs/adr-plugin-install-runbook.md`.

Smoke test: one bare
`claude -p --plugin-dir plugins/adr --permission-mode acceptEdits "…"` from
the worktree root (no `cd`, pipes or redirects). Check one case that passes
the gates (an ADR is written in the default location) and, if budget allows,
one that fails a gate (no ADR, and it says which gate). Run `git status`
afterwards and remove the test files before committing.

## Decisions already made

- MD3 (ledger): separate `adr` plugin; upstream gates and format; follow the
  repo's existing convention; domain-modeling calls it when installed.
- GD7: grilling writes nothing; the skill that owns a doc writes it.
- No dependency on `setup-matt-pocock-skills`; one plugin per skill.
- Unlike domain-modeling, MD6 (Eric on every write) does not cover ADRs; don't
  add an advisor call unless Rich asks.

## Out of scope for this session

- Wayfinder, grill-with-docs (MD13), the tracker choice and `gh:` resolver.
- Changing `plugins/domain-modeling` beyond what the `adr` hand-off needs
  (MD-B1–B5 changes wait for Rich's comments).

## Suggested skills

- `anthropic-skills:skill-creator` (only if useful for structuring SKILL.md)

## Wrap-up

Follow the "End" steps of the session protocol in the ledger, including writing
the next handoff prompt and telling Rich its path. Wayfinder has no work items
yet: the next unit is laying them out with Rich from "Inputs to triage".
