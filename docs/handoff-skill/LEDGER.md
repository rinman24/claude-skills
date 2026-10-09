# handoff skill: ledger

Branch: `feat/handoff-skill`
Worktree: `~/Code/claude-skills/.claude/worktrees/handoff-skill`
Goal: a `handoff` plugin in this marketplace that compacts the current
session into a handoff a fresh agent can pick up, structured by a template
and pointing at the project's ledger.

## Source

The essence of https://github.com/mattpocock/skills/tree/main/skills/productivity/handoff
(read at `0f5e033`). No attribution or upstream tracking (Rich, 2026-10-09).
The upstream skill, in full:

- User-invoked only (`disable-model-invocation: true`); argument hint "What
  will the next session be used for?". With an argument, tailor the
  document to that focus.
- Write a handoff document summarising the current conversation so a fresh
  agent can continue the work.
- Save it to the OS temp directory (`$TMPDIR`, else `/tmp`; `%TEMP%` on
  Windows), not the workspace.
- Include a "Suggested skills" section naming the skills the next agent
  should invoke.
- Don't duplicate what other artifacts hold (specs, plans, ADRs, issues,
  commits, diffs); reference them by path or URL.
- Redact secrets and PII.

## Rich's requirements (2026-10-09)

- Keep a `TEMPLATE.md` that structures what a handoff looks like, and keep
  using a ledger (as `docs/design-to-board/` does on `feat/design-to-board`:
  `LEDGER.md`, `LESSONS-LEARNED.md`, `handoffs/TEMPLATE.md`).
- Temp folder or a `handoffs/` directory are both acceptable, but handoff
  files probably don't belong in version control: noise in the repo. The
  ledger stays committed.
- Ask Juval where the handoff file goes before building (HQ1).

## Repo facts

- Marketplace `claude-skills`; plugins install as `<plugin>@claude-skills`.
- House pattern for a new plugin: `plugins/local-backlog/`
  (`.claude-plugin/plugin.json`, `skills/<name>/SKILL.md`), an entry in
  `.claude-plugin/marketplace.json`, and
  `docs/local-backlog-plugin-install-runbook.md`.
- Validate before committing a manifest change: `claude plugin validate .`
  and `claude plugin validate plugins/<plugin>`.
- Push: `git -c credential.helper= -c credential.helper='!gh auth git-credential' push`.
- `main` is protected: PR, merge `origin/main` into the branch rather than
  rebasing a pushed branch.

## Session budget

Under ~100K tokens per session, hard ceiling 120K, one unit per session. An
advisor consultation costs ~25–30K (answer relayed and recorded verbatim).

## Session protocol

Start: fetch and merge `origin/main` if it moved; read this ledger and
`LESSONS-LEARNED.md`; read the handoff the session log names if it is
present (it is local to the worktree, HD1), else proceed from the ledger;
mark the unit `in progress`.
End: update statuses, decisions, Rich's queue and the session log; append
lessons; commit and push; if work remains, run `/handoff` (template
`HANDOFF-TEMPLATE.md`, file under the ignored `handoffs/`); tell Rich the
handoff path and his queue.

## Status legend

`todo` · `in progress` · `done` · `blocked` · `dropped`

## Rich's queue

- [ ] Review and merge PR #11 (`plugins/handoff`, HD1–HD3).
- [ ] After merging, start H2: fresh `claude` in this worktree; give it only
      "Read `docs/handoff-skill/LEDGER.md` and start the next unit." (that is
      Juval's ledger-only test; the session reads the H2 handoff afterwards).
- [ ] Follow-up, not this effort's work: `feat/design-to-board` commits its
      handoffs under `docs/design-to-board/handoffs/`. Once that branch merges
      `main`, the new root `.gitignore` rule `docs/*/handoffs/` ignores new
      handoffs there. Decide on that branch: adopt HD1 (untrack its handoffs,
      move `handoffs/TEMPLATE.md` to `HANDOFF-TEMPLATE.md`) or `git add -f`.

## Work items

| ID | Item | Unit | Est. | Status | Notes |
|---|---|---|---|---|---|
| H1 | Rule HQ1–HQ3 (Juval on HQ1), then build `plugins/handoff`: SKILL.md, bundled template, manifest, marketplace entry, install runbook; validate, install, PR | H1 | ~70–90K | done | PR #11; installing from the marketplace waits for the merge (H2) |
| H2 | After the H1 PR merges: run Juval's ledger-only test (the session states the unit and first action from the ledger alone, then reads the handoff and notes what it added); `claude plugin marketplace update claude-skills`, install `handoff@claude-skills`, runbook Steps C–D; record lessons; mark the effort done; tell Rich the worktree can go | H2 | ~30–40K | todo | Needs the PR merged |

## Open questions

None open. HQ1–HQ3 were ruled in H1 as HD1–HD3.

## Decisions

| ID | Decision | Status | Detail |
|---|---|---|---|
| HD1 | Handoffs live in a git-ignored `handoffs/` next to the effort's ledger, inside its worktree; `$TMPDIR` only when no ledger exists. The ledger names the handoff but never depends on it: a fresh session must be able to start the next unit from the ledger alone | done (H1) | HQ1. Juval: `~/Code/board-knowledge/sessions/2026-10-09-juval-handoff-file-location.md`. Rich: efforts resume on another machine never or occasionally, so the handoff need not travel with the branch. Root `.gitignore` ignores `docs/*/handoffs/`; templates live outside `handoffs/` |
| HD2 | Template: the skill bundles a default `TEMPLATE.md`; an effort overrides it with `HANDOFF-TEMPLATE.md` next to its ledger | done (H1) | HQ2. One resolution rule in the SKILL.md, beside HD1's location rule |
| HD3 | Ledger: the skill checks that the ledger alone could start the next unit, reports gaps and offers to fix them before writing; its only unasked edit is recording the handoff path in the session log. Other upkeep stays in the effort's End protocol | done (H1) | HQ3 |

## Session log

| Session | Date | Unit | Outcome | Handoff written (local, HD1) |
|---|---|---|---|---|
| H0 | 2026-10-09 | Setup | Branch `feat/handoff-skill` from `main` `205c5f2` (set up from design-to-board's S1); this ledger, lessons, template and H1 handoff | `handoffs/H1-build.md` |
| H1 | 2026-10-09 | H1 | HQ1–HQ3 ruled as HD1–HD3 (Juval on HQ1); `plugins/handoff` built, validated, tried headless (no-ledger path) and on this ledger; PR #11 | `handoffs/H2-install-and-close.md` |
