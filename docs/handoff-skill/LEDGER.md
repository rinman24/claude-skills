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

Start: read the handoff; fetch and merge `origin/main` if it moved; read
this ledger and `LESSONS-LEARNED.md`; mark the unit `in progress`.
End: update statuses, decisions, Rich's queue and the session log; append
lessons; write the next handoff from `handoffs/TEMPLATE.md` if work
remains; commit and push; tell Rich the handoff path and his queue.

## Status legend

`todo` · `in progress` · `done` · `blocked` · `dropped`

## Rich's queue

- [ ] Start H1: fresh `claude` in this worktree, give it
      `docs/handoff-skill/handoffs/H1-build.md`. It will ask you to type
      `/ask-juval` with a prepared question.

## Work items

| ID | Item | Unit | Est. | Status | Notes |
|---|---|---|---|---|---|
| H1 | Rule HQ1–HQ3 (Juval on HQ1), then build `plugins/handoff`: SKILL.md, bundled template, manifest, marketplace entry, install runbook; validate, install, PR | H1 | ~70–90K | todo | Handoff `handoffs/H1-build.md` |

## Open questions

| ID | Question | Notes |
|---|---|---|
| HQ1 | Where does the handoff file go: OS temp dir, a git-ignored `handoffs/` in the repo, or committed `handoffs/`? | Juval. Rich leans away from version control. A temp file is lost on reboot and invisible to a teammate; a git-ignored dir survives locally; committed handoffs are what design-to-board does today |
| HQ2 | Template: bundle a default `TEMPLATE.md` in the skill, use the project's `handoffs/TEMPLATE.md` when one exists, or both? | Rich wants the template structure kept |
| HQ3 | Ledger: does the skill only reference a ledger it finds (upstream "don't duplicate"), or also update it (session log, next handoff path)? | design-to-board's protocol has the session update the ledger before handing off |

## Decisions

| ID | Decision | Status | Detail |
|---|---|---|---|

## Session log

| Session | Date | Unit | Outcome | Handoff written |
|---|---|---|---|---|
| H0 | 2026-10-09 | Setup | Branch `feat/handoff-skill` from `main` `205c5f2` (set up from design-to-board's S1); this ledger, lessons, template and H1 handoff | `handoffs/H1-build.md` |
