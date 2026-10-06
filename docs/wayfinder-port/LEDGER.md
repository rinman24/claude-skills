# Wayfinder + domain-modeling port: ledger

Branch: `feat/wayfinder-domain-modeling`
Goal: our own versions of Matt Pocock's `wayfinder` and `domain-modeling` skills
(https://github.com/mattpocock/skills, MIT) as plugins in this marketplace,
without depending on `setup-matt-pocock-skills`.

## Repo facts

- Marketplace name: `claude-skills` (the `name` field in
  `.claude-plugin/marketplace.json`; renamed from `my-skills` in PR #2). The
  old `my-skills` marketplace is uninstalled on Rich's machine; `claude-skills`
  is installed.
- Install a plugin as `<plugin>@claude-skills`, e.g.
  `claude plugin install grilling@claude-skills --scope user`.
- Refresh an environment after a push: `claude plugin marketplace update claude-skills`.
- Validate before committing a manifest change: `claude plugin validate .`.
- House pattern for a new plugin: `plugins/local-backlog/` plus
  `docs/local-backlog-plugin-install-runbook.md`.

This file is the single source of truth for what is done and what is next.
Every session reads it first and updates it last.

## Session budget

- Target: each session stays under ~100K tokens of context.
- Hard ceiling: 120K. If a session approaches it, stop, update this ledger,
  and write the next handoff prompt rather than finishing the unit.
- Size each unit of work to ~80K of planned work. The remaining ~20K covers
  boot reading (handoff prompt, this ledger, `LESSONS-LEARNED.md`) and wrap-up.
- One unit of work per session. If a unit looks bigger than ~80K, split it
  here before starting.

## How sessions hand off

Handoffs are plain prompt files, committed on this branch in `handoffs/`.
No plugin or hook is involved. To start the next session:

1. Open a terminal in the worktree for `feat/wayfinder-domain-modeling`.
2. Start a fresh `claude` session.
3. Paste the contents of `handoffs/S<N>-<slug>.md` as the first message.

## Session protocol

Start:
1. Read the handoff prompt (it is the first message).
2. Read this ledger and `LESSONS-LEARNED.md`.
3. Mark the unit `in progress` below.

End:
1. Update item statuses and the session log.
2. Append any lessons to `LESSONS-LEARNED.md`.
3. Write the next session's handoff prompt from `handoffs/TEMPLATE.md` as
   `handoffs/S<N+1>-<slug>.md`.
4. Commit and push the branch (see `LESSONS-LEARNED.md` for the push command).
5. Tell Rich the path of the new handoff prompt.

## Status legend

`todo` · `in progress` · `done` · `blocked` · `dropped`

## Work items

<!-- Laid out with Rich in session 1. Columns: id, item, unit (session), est. tokens, status, notes. -->

| ID | Item | Unit | Est. | Status | Notes |
|----|------|------|------|--------|-------|
| L0 | Set up worktree, branch, ledger, lessons, handoff template | S1 | n/a | done | |
| G1 | Grilling: outline upstream approach + author's known issues; collect Rich's feedback | S2 | ~40K | todo | Stop for feedback before G2 |
| G2 | Grilling: build `plugins/grilling` from G1 decisions | S2 | ~35K | todo | Spills to S3 if S2 is past ~70K after G1 |

## Inputs to triage

Raw material from the session 1 read of Matt's repo. Not commitments; each one
becomes a work item, a decision, or `dropped`.

- Replace `setup-matt-pocock-skills` dependencies: tracker "Wayfinding
  operations" and the `domain.md` consumer rules (read GLOSSARY/ADRs first).
- Wayfinder's other skill dependencies: `grilling`, `domain-modeling`,
  `research`, `prototype`; downstream `to-spec`, `to-tickets`, `implement`.
- Tracker choice: GitHub sub-issues + native dependencies vs local markdown
  (`.scratch/`) vs our `local-backlog` (`BACKLOG.local.md`).
- Upstream-known wayfinder gaps: agent builds code mid-map (self-authored
  Notes override); over-charting; agent picks prototype variant itself;
  parallel grilling re-asks; verbose questions; no reopen-decision guidance;
  models skip loading `domain-modeling`.
- Upstream-known domain-modeling gaps: glossary bloats into a spec; no
  tracker lookup for settled terms (upstream #717); ADR format bundled
  (upstream #557); slow brownfield bootstrap.
- Rich's own changes: to be listed.

## Session log

| Session | Date | Unit | Outcome | Handoff written |
|---------|------|------|---------|-----------------|
| S1 | 2026-10-06 | Orientation + scaffolding | Explained both skills; created branch and tracking files; rebased onto main after PR #1 (handoff plugin removed) and PR #2 (marketplace renamed to `claude-skills`) | `handoffs/S2-grilling.md` |
