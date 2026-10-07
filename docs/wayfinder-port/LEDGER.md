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
| A1 | ADR: build `plugins/adr` (MD3) | S5 | ~35K | done | Validated; headless smoke test passed for a gate-passing decision (`docs/adr/0001-…` written, one paragraph) and a gate-failing one (nothing written, each gate named). Rich to run runbook Step D 3–5 interactively (house convention, unknown gate, domain-modeling hand-off). Build interpretations AD-B1–B4 below |
| W0 | Wayfinder: lay out work items with Rich from "Inputs to triage" | S6–S7 | ~40K + ~60K | done | WD1–WD26; S7 ran four consults (Juval ×2, Eric ×2) |
| W1 | domain-modeling: rename "slice" → "batch" in MD9 / `BOOTSTRAP.md` (WD20) | S8 | ~10K | todo | Before W2, so Lookup's `slice` redirect never collides with the plugin's prose |
| W2 | Glossary rows via `/domain-modeling` with Eric: `subsystem` (WD12), `map` (WD19), `increment` ruled-in squadra (squadra PR #41 merged), `errand` (WD25) | S8 | ~35K | todo | Blocked by W1. First `GLOSSARY.md` / `GLOSSARY-SETTLED.md` in this repo |
| W3 | Build `plugins/wayfinder`: SKILL.md (Chart: Begin/Resolve/Revise/Publish; WD3–WD9, WD15, WD17, WD19, WD22–WD23), `MAP-FORMAT.md` (WD26), `DESIGN-FORMAT.md` (WD21), manifest, upstream MIT LICENSE, marketplace entry, README section, runbook | S9 | ~80K | todo | Blocked by W2 |
| W4 | Smoke-test wayfinder headless: Begin → Resolve one ticket → Publish on a toy map | S10 | ~40K | todo | Blocked by W3 |
| W5 | Build `plugins/prototype` (WD7: the user picks the variant, never the agent) | S11 | ~60K | todo | No blockers; runs in parallel with S8 on its own branch/worktree (see its handoff) |
| W6 | Wire prototype tickets into wayfinder | S12 | ~25K | todo | Blocked by W3, W5 |
| T1 | `design-to-board` (WD14) | later, not this port | n/a | todo | Blocked by W-SQ and W3; build against `DESIGN-FORMAT.md` and Juval's validation list |
| W-SQ | squadra: rename its unit "slice" → "increment" (WD11) | Rich, in squadra | n/a | in progress | Rename merged (squadra PR #41, 2026-10-07; `Increment` settled in squadra's glossary: Vertical / Foundation, rejects infrastructure increment). Remaining: WD18's squadra requirements (positive-scope claims, `squadra tick --dry-run` contract test) |

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

ADR build interpretations (S5, where MD3 left a detail open; not yet
confirmed by Rich, change in the plugin if he disagrees):

- **AD-B1 · Write or offer.** The skill writes straight away only when the user
  asked for the ADR. When domain-modeling (or any caller, or the model itself)
  raises one, it offers it in one line and writes on the user's yes (same
  principle as GD6: a calling skill is not the user's permission). The gates
  are always the adr skill's call, not the caller's.
- **AD-B2 · Unknown gate → one question.** Upstream says skip if any gate is
  missing; the skill distinguishes "fails" (write nothing, name the gate) from
  "can't tell" (ask that one question).
- **AD-B3 · Convention detection order.** Stated instructions (`CLAUDE.md`,
  `AGENTS.md`, `CONTRIBUTING.md`, `README.md`, `.adr-dir`, `.log4brains.yml`)
  win over existing files; then the repo's template or two most recent ADRs
  set filename, numbering, headings and status vocabulary; an index file gets
  a line; two conflicting conventions → ask. Only with none does the upstream
  `docs/adr/NNNN-slug.md` default apply.
- **AD-B4 · Superseding.** Added to `ADR-FORMAT.md` (upstream only had the
  `superseded by` status value): the new ADR says what it supersedes; the old
  one's `Status` is updated only if it has one; no ADR is deleted.

Wayfinder (S6, from Rich's answers to three rounds; confirmed by Rich in S7
round 1, with Eric's "board" edits applied to WD1/WD2 and WD3, WD8, WD10
amended as marked). Advisor sessions in
`board-knowledge/sessions/`: `2026-10-06-juval-wayfinder-squadra-split.md`,
`2026-10-06-eric-wayfinder-squadra-split.md`,
`2026-10-06-eric-squadra-unit-name.md`. Upstream: mattpocock/skills @ `6fd9479`.

- **WD1 · Swimlanes.** Wayfinder stays out of squadra's swimlane. It clears
  the fog on its map and produces a **design document**. A separate
  translator skill (`design-to-board`, WD14) moves that document onto
  squadra's board (GitHub or ADO), and squadra (`rinman24/squadra`) builds
  from there. Wayfinder never touches a board. (Rich's Q9 clarification;
  replaces his first "no Work mode, squadra implements Work" wording. Wording
  per Eric's "board" ruling, WD19.)
- **WD2 · The map on disk.** Committed markdown under `.scratch/wayfinder/<map>/`:
  `map.md` plus one file per decision ticket. `Settle` gets `scratch:<path>` as
  its `Ref` (MD10). This **supersedes round-1 Q1** (GitHub only, bundled
  `TRACKER-GITHUB.md`), so the `gh:` resolver is moot.
- **WD3 · Wayfinder resolves its own tickets locally (HITL)**: grilling +
  domain-modeling called by name (MD13), one decision ticket per session.
  Operation names (Eric; confirmed S7 Q2): one mode, Chart, with Begin,
  Resolve, Revise and Publish (writes the design document). The word
  "work" appears nowhere in wayfinder (false cognate with squadra).
- **WD4 · Notes override removed.** No map can "carry execution"; wayfinder
  never builds. An `errand` ticket (WD25; was "task") only unblocks a decision.
- **WD5 · Downstream out of scope.** `to-spec`, `to-tickets`, `implement` are
  not ported. `design-to-board` (the translator) is not in this port either (WD14).
- **WD6 · No research plugin.** Research tickets use an inline read-only
  subagent (primary sources, cite every claim); findings go in the ticket's
  resolution, not a `research/<name>` branch.
- **WD7 · Prototype plugin.** `prototype` is ported as its own plugin, a W-item
  after the wayfinder core, and it blocks every W-item that depends on it.
  Until then, prototype tickets follow one inline rule: the user picks the
  variant, never the agent (upstream defect 3).
- **WD8 · Revise.** Only on explicit user instruction: record what changed on
  the closed ticket, open a replacement that links back, rewrite its line in
  Decisions-so-far, flag dependents. Eric's additions (confirmed S7 Q3):
  Reopen settled terms whose `Ref` is the revised ticket (a `Ref`
  scan, not a Lookup); after Publish, edit the design document, mark it
  revised and list the changed sections.
- **WD9 · Over-charting is fought with vertical increments** (Rich's Q8
  intent): wayfinder leads toward vertical increments and may consult Juval on
  decomposition. The concrete rules are open (see below).
- **WD10 · Vocabulary (Eric's revised table, Q13).** `increment`: squadra's
  unit, one board item / claim / branch / PR, done when merged, persists across
  attempts. `vertical`: an attribute of an increment (integrates Client /
  Manager / Engine / ResourceAccess / Resource). `foundation increment`,
  `infrastructure increment`: non-vertical, must say why (a foundation one
  names the increment where it becomes vertical). `service change`, never
  "service task". `decision ticket`: wayfinder only. `design document`:
  wayfinder's output, the Published Language to the translator. `cleared`: the
  hand-off event. Retired everywhere: `work`, `deliverable`. Rich's PR-unit
  idea is his translation of Juval, not Juval's definition.
  **Amended S7 (Q9):** squadra's glossary (settled 2026-10-06, W-SQ) now
  rules: an increment is _Vertical_ (behaviour observable end to end) or
  _Foundation_ (no behaviour of its own; exists so the later increments it
  names can), or neither (its commit type carries the kind). `infrastructure
  increment`, `slice` and `vertical slice` are rejected forms. Wayfinder
  conforms: `infrastructure increment` is dropped from this table, and
  `vertical` is defined by behaviour, not layers. Juval's layer integration is
  his test for whether an increment is vertical, not the definition (Eric).
- **WD11 · squadra rename.** squadra's "slice" becomes "increment" (W-SQ, Rich
  driving it in squadra). Check Scrum's "Increment" before settling it there.
- **WD12 · "Slice" glossary row (Option A).** Settle `subsystem` (Juval's
  unit: up to three Managers with their Engines and ResourceAccess), with
  `slice` and `vertical slice` as rejected forms; context: architecture.
  Grep basis: Righting Software uses "subsystem" 65×, "slice" 14× (5×
  "vertical slice"). To be written via `/domain-modeling` (Eric's order: this
  row now, `increment` only after squadra's rename merges).

Wayfinder (S7, from Rich's answers to three rounds of `/grilling`; each
answer given explicitly; Rich then said "wrap up").
Advisor sessions in `board-knowledge/sessions/`:
`2026-10-06-juval-design-increment-split.md` (Q18),
`2026-10-06-eric-term-board.md` ("board").

- **WD13 · The design document lists the increments (Q18, Juval).**
  Splitting the design into increments is project design, so it belongs in
  wayfinder; `increment` enters wayfinder's language. Per increment, a table
  with: Name + one-line intent · Kind (`vertical`, `foundation` naming the
  increment(s) it enables, or neither, per WD10's amendment) · `Touches:`
  (services, new ones marked) · Depends on (explicit edges, including
  shared-service edges) · Order (critical path first) · Decided by (ticket
  refs). The translator's test is determinism: two independent AFK runs on one
  document give identical increments; anything else is a wayfinder defect.
  Juval withdrew per-service issues: `Touches:` vs sub-issues is a format
  mapping for the translator. His blocking question (does squadra cap one
  increment's size?) was answered by reading squadra: no cap, so "≤ 2 new
  services per increment" stands.
- **WD14 · Translator `design-to-board`: not in this port (Q4, Q13).** A later
  item after W-SQ. Requirements: it is ResourceAccess (transcribes, makes no
  decisions, AFK); publishes only cleared increments; validates and fails
  loudly back to wayfinder (missing kind, undeclared service, two increments
  touching one service with no edge, order contradicting edges, > 2 new
  services); never patches the document; honours `[board].parent_scope_ids`.
  Name chosen by Rich; Eric approved it (fallback `design-to-squadra` only if
  "design-to-board" gets heard as advisor review). Description verb:
  "transcribes a cleared design document into increments on squadra's board;
  it never designs." Context column in glossary rows: `design-to-board`.
- **WD15 · Sequential tickets (Q5).** One decision ticket in progress per map
  at a time, marked in its file; separate maps may run in parallel. Wayfinder
  never says "claim" (squadra's verb, Eric).
- **WD16 · Design document location (Q6).** `docs/design/<map>.md`, outside
  `.scratch/`; it cites tickets as `scratch:` refs. Sections: WD21.
- **WD17 · Over-charting rules (Q8).** (a) every decision ticket carries
  `Unblocks: <increment>`; (b) more than ~6 increments → split the map per
  subsystem; (c) an increment that can't be named in settled terms is fog;
  (d) more than 2 new services in one increment → split into predecessor
  increments; (e) Juval consulted only on (d) or a new component, optional
  (carry on without `board-juval`); (f) increments listed in critical-path
  order.
- **WD18 · Old board rules (Q9).** The `wayfinder:*` exclusion backstop is
  dropped (wayfinder writes nothing to a board). "Publish only cleared
  increments; validate per WD14" are translator requirements. "squadra claims
  by positive scope; `squadra tick --dry-run` contract test" go to W-SQ as
  squadra requirements (Rich: part of W-SQ is already done).
- **WD19 · "Board" (Q11, Eric).** Wayfinder has no board: the "local board" is
  the **map** (`map.md` is the aggregate root, ticket files inside its
  boundary); the skill says positively that wayfinder writes only the map and
  the design document. In claude-skills a bare "board" is squadra's board
  (Conformist; `[board]` keys). Advisors are named by member (`board-juval`),
  "the advisors" for the collective. Glossary: Settle `map` (rejected:
  `local board`, context: wayfinder); nothing about squadra's `board` is
  settled here (translator out of port). Done-test: `rg -n -i '\bboards?\b'
  plugins/ docs/wayfinder-port/` returns only squadra-sense uses, agent ids and
  history.
- **WD20 · "Slice" in domain-modeling (Q12).** MD9 and `BOOTSTRAP.md` say
  "slice" for one module's batch of terms; rename to "batch" in its own W-item,
  before the glossary item (Eric).

S7 round 3 (after Juval and Eric on Q10/Q13: board-knowledge
`sessions/2026-10-07-juval-design-document-contract.md`,
`sessions/2026-10-06-eric-design-document-contract.md`; asked in parallel, neither
saw the other). WD21–WD26 refine WD13 and WD16; where they differ, these win.

- **WD21 · Design document contract (Q14).** Bundled in W3 as `DESIGN-FORMAT.md`
  (the document `design-to-board` is built against). YAML front matter
  `format: wayfinder-design/1`, `map`, `status: cleared | revising`,
  `revision: <N>`, `changed: [...]`. Sections: **Destination** (Eric; not
  "Goal") listing behaviours `B1`, `B2`… (Juval, ~2–3) · **Decisions** (one
  line per current decision with its `scratch:` ref; no errand tickets) ·
  **Services** `Service | Layer | Encapsulates | Introduced in` (only services
  this map changes or creates; `Encapsulates` required for a new one; the only
  place "new" is stated) · **Increments** `ID | Increment | Kind | Touches |
  Depends on | Order | Decided by | Published` (Kind: `vertical (B<n>)`,
  `foundation → I<n>, …`, or blank, per squadra's glossary; `Touches` names
  only; `Depends on` allows `<map>:<ID>`) · **Rules and planning assumptions**
  (rule lines, e.g. WD23, kept apart from resource lines: ≤ 2 concurrent
  runners, one reviewer; a line belongs only if changing it would make Rich
  Revise the map). Juval's split is marked in the spec: contract = front
  matter, Services, Increments, Rules; record = Destination, Decisions; the
  translator never reads the record. Wayfinder checks before `cleared`: every
  behaviour has a vertical increment and vice versa; every `Decided by` ref is
  in Decisions. The document is never a copy of `map.md` (fog and ticket bodies
  stay in the map). Translator validation list: Juval's session, "What the
  translator validates".
- **WD22 · Increment identity (Q15, Juval).** IDs `I1`, `I2`… never renumbered
  or reused. A published row changes only its status (`Published: r1,
  withdrawn r2`); any other change = withdraw + new ID. Withdrawn rows stay.
  The translator only ever creates and withdraws. Revise sets only
  `status: revising`; Publish rewrites the body, sets `cleared`, bumps
  `revision`, fills `changed`. (Refines WD8's "edit in place".)
- **WD23 · Integration rule (Q16).** Strict form: at most 2 **changed**
  services (new or modified) per increment = a count of `Touches`. Replaces
  "≤ 2 new services" in WD13, WD14 and WD17(d). Value lives in the document's
  rule line.
- **WD24 · No Settled terms section (Q17).** Design documents don't drive a
  fleet in another repo yet; if they ever do, `design-to-board` brings it back,
  selecting by terms used in Increments, term + `Ref` only.
- **WD25 · `errand` (Q18b, Eric).** Wayfinder's non-decision ticket kind is
  `errand`, not `task` ("Task" is squadra's child item; `chore` is a commit
  type). Supersedes "task" in WD4.
- **WD26 · Map format (Q19).** Bundled in W3 as `MAP-FORMAT.md`. `map.md`:
  Destination · Increments (same columns as WD21) · Decisions so far · Fog.
  Ticket file: Kind (`grilling | research | prototype | errand`), Status
  (`open | in progress | closed | revised`), `Unblocks:`, Blocked by,
  Resolution. "in progress" is the WD15 mark; no "claim".

Still open: nothing for wayfinder. Rich has still not commented on MD-B1–B5
or AD-B1–B4. squadra side of WD18 (positive-scope claims, `tick --dry-run`
contract test) is with Rich in W-SQ.

## Inputs to triage

Raw material from the session 1 read of Matt's repo. Not commitments; each one
becomes a work item, a decision, or `dropped`.

S6 dispositions:
- `setup-matt-pocock-skills` tracker operations → WD2 (local board, format
  bundled in the plugin); `domain.md` consumer rules → wayfinder's Begin and
  Resolve call domain-modeling (Lookup) and read ADRs; detail in W1.
- Skill dependencies → `grilling`/`domain-modeling` by name (MD13);
  `research` → WD6; `prototype` → WD7; downstream → WD5.
- Tracker choice → WD2 (local committed markdown); `local-backlog` dropped as
  a tracker (no blocking or claims, git-excluded).
- Wayfinder gaps: builds code → WD4 + GD7; over-charting → WD9 (rules open);
  prototype variant → WD7; parallel re-asks → open; verbose questions → GD3;
  reopen guidance → WD8; skips loading domain-modeling → MD13.
- Domain-modeling gaps → decided in MD3, MD5, MD9–MD11.
- Rich's own changes → WD1, WD3, WD9.
- `gh:` resolver → dropped (WD2: wayfinder never touches GitHub);
  `term-settled` backfill → dropped (MD12).

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
| S5 | 2026-10-06 | A1 · ADR build | Built `plugins/adr` (SKILL.md, ADR-FORMAT.md, manifest, upstream MIT LICENSE, marketplace entry, README section, runbook); validated; two headless smoke runs (gate-passing decision → `docs/adr/0001-…`; gate-failing → nothing written, all three gates named). Recorded AD-B1–B4. No change to `plugins/domain-modeling` needed: its ADR section already calls the `adr` skill | `handoffs/S6-wayfinder-layout.md` |
| S6 | 2026-10-06 | W0 · Wayfinder layout (part 1) | Outlined upstream wayfinder and its deps; three grilling rounds; consulted Juval (split, slices), Eric (split, vocabulary) and Eric again (squadra unit name → `increment`). Rich reframed: wayfinder is chart-only on a local committed board and outputs a design document; squadra builds. Recorded WD1–WD12 and triage dispositions; Q18 (Juval) and the W-layout left to S7 at Rich's call (context) | `handoffs/S7-wayfinder-layout-2.md` |
| S7 | 2026-10-06/07 | W0 · Wayfinder layout (part 2) | Rich confirmed WD1–WD12; three grilling rounds decided WD13–WD26 (design document lists increments; `design-to-board` named, out of port; "board" → map; `errand`; design-document and map formats). Four consults: Juval (Q18; Q10), Eric ("board"; Q10 + name). Laid out W1–W6 and T1 | `handoffs/S8-glossary.md`, `handoffs/S11-prototype.md` |
