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
| G1 | Grilling: outline upstream approach + author's known issues; collect Rich's feedback | S2 | ~40K | done | Decisions GD1–GD7 below |
| G2 | Grilling: build `plugins/grilling` from G1 decisions | S2 | ~35K | done | Validated; headless smoke test passed for round format, fact lookup, no-code. Rich to check clarification + gate interactively (runbook Step D 4 and 6) |
| G3 | Retire the claude.ai-synced `anthropic-skills:grill-me` (old one-at-a-time text) | Rich | n/a | todo | After G2 smoke test passes (GD1); done in claude.ai, not this repo |
| M1 | Domain-modeling: outline upstream approach + author's known issues; collect Rich's feedback | S3 | ~40K | todo | Stop for feedback before M2 |
| M2 | Domain-modeling: build `plugins/domain-modeling` from M1 decisions | S3 | ~35K | todo | Spills to S4 if S3 is past ~70K after M1 |

## Decisions

Grilling (S2, from Rich's answers to the G1 round). Upstream issue IDs (D1–D9,
R1–R4) refer to the S2 outline: D = known defect, R = request the author
rejected.

- **GD1 · Name.** Plugin `grilling`, skill `grilling` (invoked as
  `/grilling`, namespaced `grilling:grilling`). The synced
  `anthropic-skills:grill-me` gets retired once ours is smoke-tested (G3).
- **GD2 · No wrapper.** Ship only the model-invocable core; no `grill-me`-style
  user-invoked wrapper. One-line wrappers fail to load their target (D5).
  Revisit when grill-with-docs is ported.
- **GD3 · Tight question format.** Question body ≤ ~3 lines and says why it
  is being asked now (D6). The `➡️` recommendation answers the question as
  worded ("Yes: …", "Option B: …"), never argues against it (D1).
- **GD4 · Clarification.** The user can ask what a question means instead of
  answering it. The agent re-explains it plainly (with a concrete example),
  doesn't treat that as an answer, and the rest of the round stays open.
  (Rich's addition.)
- **GD5 · No cap, no `AskUserQuestion`.** Same as upstream R1 and R2. For
  oversized scope (D7) the skill proposes splitting before grilling the pieces.
- **GD6 · Hardened gate.** End with a numbered summary of every decision and
  wait for explicit confirmation (D3). Being run by another skill or ticket is
  never permission to answer the user's decisions (D4).
- **GD7 · Grilling never writes code.** Not during the session and not after
  confirmation: no code, no scaffolds or sketches, and grilling itself edits
  no files; fact-finding subagents are read-only. Confirmation ends the skill;
  building is a separate step the user starts. A skill loaded alongside
  grilling (e.g. domain-modeling writing `GLOSSARY.md`) owns its own doc
  writes. (Rich's addition, extending D3.)

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
- From S2 (grilling): GD7 means a wayfinder grilling ticket can never produce
  code, which directly addresses the "agent builds code mid-map" gap; keep
  wayfinder's own wording consistent with it. GD2 (no wrapper) means
  grill-with-docs, if ported, must call the Skill tool for `grilling` and
  `domain-modeling` explicitly and should check both loaded (upstream D5, the
  most-reported bug). Upstream D9 (decisions lost between grilling and
  to-spec) is grill-with-docs' problem; GD6's closing decision summary gives
  it something durable to write down.

## Session log

| Session | Date | Unit | Outcome | Handoff written |
|---------|------|------|---------|-----------------|
| S1 | 2026-10-06 | Orientation + scaffolding | Explained both skills; created branch and tracking files; rebased onto main after PR #1 (handoff plugin removed) and PR #2 (marketplace renamed to `claude-skills`) | `handoffs/S2-grilling.md` |
| S2 | 2026-10-06 | G1, G2 · Grilling | Outlined upstream grilling and its known issues; Rich decided GD1–GD7; built `plugins/grilling` (skill, manifest, upstream MIT LICENSE, marketplace entry, README section, runbook); validated and smoke-tested via `--plugin-dir` | `handoffs/S3-domain-modeling.md` |
