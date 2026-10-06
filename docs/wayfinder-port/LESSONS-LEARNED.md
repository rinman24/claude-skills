# Lessons learned

Append-only. One entry per lesson: what happened, and how to apply it next time.
Newest at the bottom.

## S1 · 2026-10-06

- **Matt's skills get their per-repo config from `setup-matt-pocock-skills`.**
  Wayfinder reads "Wayfinding operations" from `docs/agents/issue-tracker.md`;
  other skills read `docs/agents/domain.md`. Apply: when porting a skill, grep
  it for `docs/agents/` and `/setup-matt-pocock-skills` and replace each
  reference with something this repo owns.
- **Upstream docs pages are the best source of known defects.** Each
  `docs/engineering/<skill>.md` has a "Common questions" section listing real
  user-reported failures. Apply: read the docs page, not just `SKILL.md`,
  before designing changes.
- **`EnterWorktree` auto-names the branch `worktree-<name>`.** Apply: rename
  with `git branch -m` straight after creating it.
- **Hook output persisted under `tool-results/` is ephemeral.** The canon-core
  injection file was gone later in the session. Apply: if a rule from the
  session-start hook matters, quote it into the ledger when first seen.
- **`.pipeline/` is not gitignored here**, despite the `handoff` skill saying
  so. Apply: keep durable handoff prompts in `docs/wayfinder-port/handoffs/`;
  don't rely on `.pipeline/` staying out of commits.
- **Budget numbers need reconciling up front.** "Stay under 100K" and "120K
  units" conflict. Apply: 100K target, 120K hard ceiling, ~80K of planned work
  per unit.
- **Plain `git push` fails here (HTTPS origin, no git credential helper).**
  `gh` is logged in with protocol `ssh`, but `origin` is HTTPS. Apply: push with
  `git -c credential.helper= -c credential.helper='!gh auth git-credential' push`.
