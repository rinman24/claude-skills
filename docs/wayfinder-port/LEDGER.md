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
| M1 | Domain-modeling: outline upstream approach + author's known issues; collect Rich's feedback | S3 | ~40K | done | Decisions MD1–MD13 below; Juval and Eric consulted (board-knowledge `sessions/2026-10-06-juval-settled-term-lookup.md`, `…-eric-settled-term-verbs.md`) |
| M2 | Domain-modeling: build `plugins/domain-modeling` from M1 decisions | S4 | ~60K | done | Validated; headless smoke test passed for Eric consult, refusal on Eric's objection, and both-files write on approval. Rich to run runbook Step D 3–7 interactively (announcement after an answer, drift, Reopen, bootstrap, no-Eric berth). Build interpretations MD-B1–B5 below |
| A1 | ADR: build `plugins/adr` (MD3) | S5 | ~35K | todo | Upstream `ADR-FORMAT.md` gates + format, plus "follow the repo's existing ADR convention"; domain-modeling hands off to it |

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

Domain-modeling (S3, from Rich's answers to the M1 rounds; confirmed). Upstream
issue IDs: K = known defect (K1 glossary bloats into a spec, K2 models skip
loading the skill, K3 no settled-term lookup #717, K4 ADR format bundled #557,
K5 slow brownfield bootstrap, K6 unreviewed glossary treated as truth), R =
request the author rejected (R1 brownfield skill #101, R2 rename GLOSSARY.md,
R3 vague-prompt-to-domain-language skill).

- **MD1 · Name.** Plugin `domain-modeling`, skill `domain-modeling`.
- **MD2 · Locations.** `GLOSSARY.md`, `GLOSSARY-MAP.md` and
  `GLOSSARY-SETTLED.md` at the repo root; upstream names kept (R2).
- **MD3 · ADRs split out (K4).** Separate `adr` plugin (A1): upstream's three
  gates and minimal format, but follow the repo's existing ADR convention if
  one exists. Domain-modeling calls the `adr` skill when a decision looks
  ADR-worthy and the plugin is installed; otherwise it suggests one.
- **MD4 · Inline writes (K6).** A term goes into `GLOSSARY.md` the moment it
  is settled; each write is announced at the top of the next round for review.
  Domain-modeling owns every doc write (GD7).
- **MD5 · Bloat guard (K1).** "Term or spec?" test on every write; past ~40
  terms or ~150 lines, propose a pruning pass with specific cuts. Pruning
  touches `GLOSSARY.md` only, never the settled record.
- **MD6 · Eric on every write.** Consult `board-eric` on every glossary write
  and on every pruning pass. (Rich chose this over contested-terms-only.)
- **MD7 · Reaching Eric.** Call the `board-eric` agent directly (Agent tool,
  `subagent_type: board-eric`); `/ask-eric` and `~/Code/board` stay unchanged
  (`disable-model-invocation: true` is a board Phase 2 decision). If
  `board-eric` is unavailable, refuse the Eric-dependent steps; with MD6 that
  means no glossary writes on a machine or berth without it. Say so plainly.
- **MD8 · No session files.** Eric consults inside domain-modeling write
  nothing to `board-knowledge`; the glossary and settled record are the record.
- **MD9 · Brownfield bootstrap (K5).** Read-only extractor subagents, one per
  top-level module, return candidate terms with `file:line` evidence; Eric
  sees one slice's term list at a time (never raw code), then a final pass over
  the per-slice lists for context boundaries and whether `GLOSSARY-MAP.md` is
  needed. Rich reviews each slice's draft before anything is written. A section
  of the skill, not a separate skill (R1).
- **MD10 · Settled record (K3, Juval).** Lookup is separate from provenance.
  `GLOSSARY-SETTLED.md` columns: `Term | Rejected | Context | Ruling | Status |
  Settled | Ref`. `Ref` is an opaque `scheme:locator` (`gh:`, `scratch:`,
  `backlog:`, `session:`) never followed during lookup; wayfinder passes its
  ticket ref in. Rows are never deleted; status only moves forward. The bloat
  threshold doesn't apply. The "term or spec?" test applies to `Ruling`.
  Enforcement is not reopening: drift is reported and work continues.
- **MD11 · Operations (Eric).** `Settle(term, rejected, context, ruling,
  ref)`; `Lookup(form, context)` (query, no writes) returning `unsettled`,
  `settled-term`, `rejected-form(→ term)`, `distinct-from(other)`, `reopened`
  or `ruled-in(other context)`; `Reopen(form, context, reason, ref)` only on
  explicit user instruction, flipping `settled` → `reopened`, or `withdrawn`
  with a no-replacement flag. A later Settle supersedes a `reopened` row.
  Statuses: `settled | reopened | superseded | withdrawn`. Distinction rulings
  put both terms in `Term` and leave `Rejected` empty. Drift reports never use
  the word "reopen". File header: Eric's rewritten line (board session file).
- **MD12 · No backfill.** No GitHub naming rulings worth importing. The
  `term-settled` backfill and a `gh:` resolver go to "Inputs to triage".
- **MD13 · No grill-with-docs wrapper.** Run `/grilling` and
  `/domain-modeling` by name; wayfinder calls both explicitly (GD2).

Build interpretations (S4, where MD1–MD13 left a detail open; not yet
confirmed by Rich, change in the plugin if he disagrees):

- **MD-B1 · Reopen skips Eric.** Eric reviews every `GLOSSARY.md` /
  `GLOSSARY-MAP.md` write, every `Settle` and every pruning pass. `Reopen`
  adds no language, so it runs without him, including where `board-eric` is
  missing.
- **MD-B2 · Eric advises, Rich decides.** An approval is written straight
  away; a sharper wording or an objection goes back to the user as a question
  before anything is written.
- **MD-B3 · Lookup ignores history.** Lookup matches only `settled` and
  `reopened` rows; a form whose only rows are `withdrawn` or `superseded` is
  `unsettled`. `Settle` never overrides a `settled` row (Reopen first).
- **MD-B4 · Bootstrap settles last.** A row's `Context` can't change, so the
  bootstrap writes `GLOSSARY.md` per approved slice but holds every `Settle`
  until after Eric's final context pass.
- **MD-B5 · Reopen's reason and ref live in the announcement and git
  history.** Rows are immutable apart from `Status`, so they keep their
  original `Settled` and `Ref`. If that loses too much, the fix is a
  `Reopened` column or an event-log format (Eric's Domain Events note).

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
- From S3 (domain-modeling): the domain-modeling gaps above are now decided
  (MD3, MD5, MD9, MD10–11). Wayfinder must pass its ticket ref into
  domain-modeling's `Settle` as the `Ref` (MD10). A `gh:` ref resolver and an
  optional `term-settled` label backfill (MD12) belong with the tracker
  decision; Rich expects GitHub. Upstream K2 (models skip loading
  domain-modeling) is the caller's job: wayfinder calls the Skill tool for
  `grilling` and `domain-modeling` separately and checks both loaded. With MD7,
  wayfinder tickets run in a berth without `board-eric` get no glossary writes.

## Session log

| Session | Date | Unit | Outcome | Handoff written |
|---------|------|------|---------|-----------------|
| S1 | 2026-10-06 | Orientation + scaffolding | Explained both skills; created branch and tracking files; rebased onto main after PR #1 (handoff plugin removed) and PR #2 (marketplace renamed to `claude-skills`) | `handoffs/S2-grilling.md` |
| S2 | 2026-10-06 | G1, G2 · Grilling | Outlined upstream grilling and its known issues; Rich decided GD1–GD7; built `plugins/grilling` (skill, manifest, upstream MIT LICENSE, marketplace entry, README section, runbook); validated and smoke-tested via `--plugin-dir` | `handoffs/S3-domain-modeling.md` |
| S3 | 2026-10-06 | M1 · Domain-modeling decisions | Outlined upstream domain-modeling and its issues (K1–K6, R1–R3); four grilling rounds; consulted Juval (settled-term record) and Eric (its operations); Rich confirmed MD1–MD13. Build (M2) spilled to S4; ADR plugin split out as A1 | `handoffs/S4-domain-modeling-build.md` |
| S4 | 2026-10-06 | M2 · Domain-modeling build | Built `plugins/domain-modeling` (SKILL.md, GLOSSARY-FORMAT.md, SETTLED-FORMAT.md, BOOTSTRAP.md, manifest, upstream MIT LICENSE, marketplace entry, README section, runbook); validated; two headless smoke runs (Eric objection → no write; Eric approval → both files). Recorded build interpretations MD-B1–B5 | `handoffs/S5-adr.md` |
