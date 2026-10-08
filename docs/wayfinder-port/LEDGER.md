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
2. Update [Rich's queue](#richs-queue): tick what he did this session, add
   anything new left for him, and record his rulings in the build
   interpretation tables.
3. Append any lessons to `LESSONS-LEARNED.md`.
4. Write the next session's handoff prompt from `handoffs/TEMPLATE.md` as
   `handoffs/S<N+1>-<slug>.md`.
5. Commit and push the branch (see `LESSONS-LEARNED.md` for the push command).
6. Tell Rich the path of the new handoff prompt and what's still open in his
   queue.

## Status legend

`todo` · `in progress` · `done` · `blocked` · `dropped`

## Rich's queue

Everything waiting on Rich, in one place. Sessions tick items when he does
them and add new ones at End. Suggested order: the wayfinder interactive
checks before S12 edits the skill, then the confirmations, then the rest.

Confirm or overrule (reply e.g. "confirm all except WD-B7"; the session
records it in the table's Status column):
- [x] WD-B1–B13 ([table](#decisions), after WD28): all confirmed 2026-10-08
- [x] MD-B1–B5 ([table](#decisions), after MD13): all confirmed 2026-10-08
- [x] AD-B1–B4 ([table](#decisions), after MD-B): all confirmed 2026-10-08

Interactive checks (each runbook's Step D; under `--plugin-dir` type
`/<plugin>:<skill>`):
- [x] wayfinder Step D 4, 6, 7 (Rich, 2026-10-08, in
      `~/Code/scratch/wayfinder-smoke`; D 6 found the WD-B13 gap, fixed)
- [ ] grilling Step D 4, 6 (`docs/grilling-plugin-install-runbook.md`)
- [ ] domain-modeling Step D 3–7 (`docs/domain-modeling-plugin-install-runbook.md`)
- [ ] adr Step D 3–5 (`docs/adr-plugin-install-runbook.md`)
- [ ] prototype Step D 6 (`docs/prototype-plugin-install-runbook.md`), once a
      repo with a web UI exists

Elsewhere:
- [ ] G3: retire `anthropic-skills:grill-me` in claude.ai
- [ ] W-SQ: squadra side of WD18 (positive-scope claims, `squadra tick
      --dry-run` contract test)
- [x] Start S12: paste `handoffs/S12-prototype-wiring.md` into a fresh session

Added in S12:
- [ ] Confirm or overrule WD-B14–B15 ([table](#decisions), after WD-B13)
- [ ] wayfinder Step D 8, the verdict half (`docs/wayfinder-plugin-install-runbook.md`):
      give a verdict on a waiting prototype ticket; check the Resolution, the
      `closed` status, one Decisions line and no prototype file left behind
- [x] Prototype location: Rich chose `.scratch/prototypes/<map>/`
      (2026-10-08); W7 makes the change and adds WD-B16
- [ ] Start Q1: paste `handoffs/Q1-rich-queue.md` into a fresh session

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
| W1 | domain-modeling: rename "slice" → "batch" in MD9 / `BOOTSTRAP.md` (WD20) | S8 | ~10K | done | `BOOTSTRAP.md` (11 lines) and MD9; `rg -n -i slice plugins/domain-modeling` clean. Before W2, so Lookup's `slice` redirect never collides with the plugin's prose |
| W2 | Glossary rows via `/domain-modeling` with Eric: `subsystem` (WD12), `map` (WD19), `increment` ruled-in squadra (squadra PR #41 merged), `errand` (WD25) | S8 | ~35K | done | Layout per WD27: `GLOSSARY-SETTLED.md` + `GLOSSARY-MAP.md` at root, `plugins/wayfinder/GLOSSARY.md`; all four rows in Wayfinder. WD19 done-test clean (remaining hits: squadra sense, `board-*` ids, `~/Code/board` project, history, and Map's `_Avoid_: local board`) |
| W3 | Build `plugins/wayfinder`: SKILL.md (Chart: Begin/Resolve/Revise/Publish; WD3–WD9, WD15, WD17, WD19, WD22–WD23), `MAP-FORMAT.md` (WD26), `DESIGN-FORMAT.md` (WD21), manifest, upstream MIT LICENSE, marketplace entry, README section, runbook | S9 | ~80K | done | Validated (`claude plugin validate .` and the plugin). Four glossary rows first (WD28). Build interpretations WD-B1–B10 below. Not smoke-tested (W4) |
| W4 | Smoke-test wayfinder headless: Begin → Resolve one ticket → Publish on a toy map | S10 | ~40K | done | Headless passes: Step D 1 (Begin with answers given up front wrote `map.md` and two tickets, resolved nothing), 3 (Resolve took the first frontier ticket, a research one, with one subagent and cited sources; closed it, added one Decisions line, graduated fog into a new ticket, stopped), 5 (Publish wrote a cleared `docs/design/<map>.md` on a hand-seeded map; on a failing copy it named checks 1 and 3 and wrote nothing). Defect fixed: check 4 failed every map whose names had no `GLOSSARY-SETTLED.md` row (WD-B11, unconfirmed). Rich's interactive Step D 2 grilled small ideas before saying no map was needed; fixed with a size check before grilling (WD-B12, unconfirmed) and re-run headless on both of his ideas plus a large one. Rich ran Step D 4, 6, 7 interactively (2026-10-08): all passed; D 6 showed Revise leaving `Decided by` on the revised ticket, fixed as WD-B13 (unconfirmed) and re-run headless. All of Step D now verified |
| W5 | Build `plugins/prototype` (WD7: the user picks the variant, never the agent) | S11 | ~60K | done | Built on `feat/prototype-plugin` (PR #3, merged). Validated; headless smoke test passed for UI variants in a repo with no app (sub-shape C, hand-over, no pick), the logic demo (hand-over, no ruling) and a settled design (refused, nothing written). Rich verified runbook Step D 1–5 and 7 interactively in `~/Code/squadra` on a scratch branch (2026-10-07); Step D 6 (sub-shape A, existing page) deferred until a repo with a web UI exists. Decisions from one S11 grilling round (Rich: "all recommended"): PD1 the verdict is always the user's: the skill hands over and waits, headless or called by another skill; PD2 one logic model by default, competing models on tabs only when the question names alternatives; PD3 it ends at recording the verdict, never folds into the real code; PD4 the prototype is kept on a never-merged `prototype/<name>` branch only on the user's yes; PD5 UI sub-shape C, one self-contained HTML file when the repo has no app; PD6 model-invocable (so W6 can call it), with a question check that turns away settled designs and whole-app demos |
| W6 | Wire prototype tickets into wayfinder | S12 | ~25K | done | Replaced WD-B3: a prototype ticket now calls the `prototype` skill, the user gives the verdict, and the Resolution links the prototype (`SKILL.md` prototype bullet, "What wayfinder writes", Resolve step 2; `MAP-FORMAT.md` Resolution; runbook Step D 8; README). Validated. Headless Step D 8 hand-over passed on a toy map: `prototype` loaded, three UI variants in one HTML file, said what it noticed without picking, ticket left `in progress`, no Resolution, no Decisions line. The verdict half of Step D 8 needs a second turn (Rich). Build interpretations WD-B14–B15 |
| W7 | Wayfinder tells `prototype` to put a pending prototype under `.scratch/prototypes/<map>/`, not the map folder (WD-B16) | Q1 | ~15K | done | Rich's choice after S12's headless run put it in `.scratch/wayfinder/<map>/`. `SKILL.md` prototype bullet and "What wayfinder writes", runbook Step D 8. Validated. Headless Resolve on a toy map (UI question, no app): prototype landed at `.scratch/prototypes/queue-page/01-queue-layout.prototype.html`; in the map folder only the ticket's `in progress` changed; handed over without picking. Toy map and prototype deleted. `plugins/prototype` unchanged |
| Q1 | Walk Rich through his queue, one item at a time | Q1 | ~30–50K | in progress | Rich's order (2026-10-08): Q1, then S13 (W8), then the PR to main (W9). Records rulings and defects; fixes nothing |
| W8 | Fix what Q1 turns up | S13 | tbd | todo | Q1 adds items here. If Q1 finds nothing, S13 does W9 instead |
| W9 | PR `feat/wayfinder-domain-modeling` → main, then install the port's plugins from the marketplace | after S13 | ~10K | todo | No PR yet; 30 commits ahead of main at S12 |
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
  sees one batch's term list at a time (never raw code), then a final pass over
  the per-batch lists for context boundaries and whether `GLOSSARY-MAP.md` is
  needed. Rich reviews each batch's draft before anything is written. A section
  of the skill, not a separate skill (R1). ("Slice" renamed to "batch" in S8,
  WD20/W1.)
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

Build interpretations (S4, where MD1–MD13 left a detail open; change in the
plugin if Rich disagrees). Status: `unconfirmed`, `confirmed <date>`,
`overruled <date>: <what instead>`, or `record only` (nothing to decide).

| ID | Interpretation | Status | Detail |
|----|----------------|--------|--------|
| MD-B1 | Reopen skips Eric | confirmed 2026-10-08 | Eric reviews every `GLOSSARY.md` / `GLOSSARY-MAP.md` write, every `Settle` and every pruning pass. `Reopen` adds no language, so it runs without him, including where `board-eric` is missing |
| MD-B2 | Eric advises, Rich decides | confirmed 2026-10-08 | An approval is written straight away; a sharper wording or an objection goes back to the user as a question before anything is written |
| MD-B3 | Lookup ignores history | confirmed 2026-10-08 | Lookup matches only `settled` and `reopened` rows; a form whose only rows are `withdrawn` or `superseded` is `unsettled`. `Settle` never overrides a `settled` row (Reopen first) |
| MD-B4 | Bootstrap settles last | confirmed 2026-10-08 | A row's `Context` can't change, so the bootstrap writes `GLOSSARY.md` per approved batch but holds every `Settle` until after Eric's final context pass |
| MD-B5 | Reopen's reason and ref live in the announcement and git history | confirmed 2026-10-08 | Rows are immutable apart from `Status`, so they keep their original `Settled` and `Ref`. If that loses too much, the fix is a `Reopened` column or an event-log format (Eric's Domain Events note) |

ADR build interpretations (S5, where MD3 left a detail open; change in the
plugin if Rich disagrees). Status values as for MD-B.

| ID | Interpretation | Status | Detail |
|----|----------------|--------|--------|
| AD-B1 | Write or offer | confirmed 2026-10-08 | The skill writes straight away only when the user asked for the ADR. When domain-modeling (or any caller, or the model itself) raises one, it offers it in one line and writes on the user's yes (same principle as GD6: a calling skill is not the user's permission). The gates are always the adr skill's call, not the caller's |
| AD-B2 | Unknown gate → one question | confirmed 2026-10-08 | Upstream says skip if any gate is missing; the skill distinguishes "fails" (write nothing, name the gate) from "can't tell" (ask that one question) |
| AD-B3 | Convention detection order | confirmed 2026-10-08 | Stated instructions (`CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, `README.md`, `.adr-dir`, `.log4brains.yml`) win over existing files; then the repo's template or two most recent ADRs set filename, numbering, headings and status vocabulary; an index file gets a line; two conflicting conventions → ask. Only with none does the upstream `docs/adr/NNNN-slug.md` default apply |
| AD-B4 | Superseding | confirmed 2026-10-08 | Added to `ADR-FORMAT.md` (upstream only had the `superseded by` status value): the new ADR says what it supersedes; the old one's `Status` is updated only if it has one; no ADR is deleted |

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
  **Amended S8 (WD27):** context is Wayfinder, not architecture.

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

S8 (W2, Eric reviewed every write; Rich accepted all of Eric's revisions):

- **WD27 · Glossary layout and contexts (Eric, revising his WD12/S7 rulings).**
  All four first terms are settled in the **Wayfinder** context, because
  wayfinder speaks them (WD17, WD21, WD26). A row in another context would
  only be `ruled-in`, which is not enforced. Files:
  - `GLOSSARY-SETTLED.md` and `GLOSSARY-MAP.md` at the root.
  - `plugins/wayfinder/GLOSSARY.md` headed `# Wayfinder`, created ahead of W3.
  - No root `GLOSSARY.md`: each plugin is its own context.

  squadra fleet is not copied in as rows. It appears in `GLOSSARY-MAP.md` as
  "Wayfinder → squadra fleet: Conformist on Increment", linked to squadra's
  glossary. A copied row would go stale if squadra reopened the term.

  Rows written on 2026-10-07:

  | Term | Rejected | Ref |
  |---|---|---|
  | Subsystem | Slice, Vertical slice | `session:2026-10-06-eric-squadra-unit-name` |
  | Map | Local board | `session:2026-10-06-eric-term-board` |
  | Errand | Task, Chore | `session:2026-10-06-eric-design-document-contract` |
  | Increment | Infrastructure increment | `session:2026-10-06-eric-design-document-contract` |

  Eric's acceptance test is that Lookup in Wayfinder returns exactly one
  enforced answer for `slice`, `vertical slice`, `infrastructure increment`,
  `local board`, `task` and `increment`. It passes.

  Wording changes made under WD3 and WD14:
  - Errand's definition says "manual step", not "work".
  - The map's Relationships line says `design-to-board` "(not yet built) will
    read". Change it to "reads" when T1 ships.
  - Eric chose not to rule on "non-decision ticket": whether a research ticket
    counts as a decision ticket stays with W3.

  `ruled-in` across several foreign contexts needs no format change until a
  second owned context settles an overlapping form. The fix then is that
  `ruled-in` lists every matching context.

S9 (W3; one Eric consult, Rich accepted every recommendation):

- **WD28 · Four more Wayfinder terms (Eric, Rich).** `Ticket` (rejects issue,
  story, card), `Decision ticket` (any kind except errand, research included;
  rejects work item), `Design document` (rejects spec, plan, deliverable),
  `Cleared` (the design document's state in which `design-to-board` may read
  it; opposite: revising; rejects done, ready, final, approved). Eric objected
  to Cleared as both state and event, so it is a state now. Publishing a
  cleared document is the hand-off, which amends WD10's "hand-off event".
  Eric cut storage details from the definitions. The `GLOSSARY.md` opening
  line no longer says "clears the fog", because "clear" now belongs only to
  the design document; the skill says fog "graduates". `Decision ticket`'s
  row doesn't reject `Task`, because `Task` is already rejected for Errand
  and a second row would break the one-answer Lookup test. Its `_Avoid_`
  line still lists task. The Lookup test passes for 13 forms. `Ref`:
  `session:2026-10-07`.

Build interpretations (S9–S10, where WD1–WD28 left a detail open; change in
the plugin if Rich disagrees). Status values as for MD-B.

| ID | Interpretation | Status | Detail |
|----|----------------|--------|--------|
| WD-B1 | Out of scope lives under Destination | confirmed 2026-10-08 | WD26 lists four map sections, so upstream's separate Out of scope section became an `Out of scope:` list in Destination (scope is the destination's business) |
| WD-B2 | No research exception | confirmed 2026-10-08 | Upstream fired research subagents at charting and exempted research from one-per-session; WD15 is applied strictly: Begin resolves nothing, and research tickets go one at a time |
| WD-B3 | Prototype before W6 | replaced (W6) | Variants were shown in the conversation, not written as files (wayfinder wrote only the map and the design document); the user picked. Confirmed 2026-10-08; replaced in S12: a prototype ticket now calls the `prototype` skill (WD-B14, WD-B15) |
| WD-B4 | Errands are checklists | confirmed 2026-10-08 | Wayfinder hands the user a checklist and may run read-only commands; it doesn't perform the manual step itself |
| WD-B5 | Errands in the map | confirmed 2026-10-08 | An errand's `Unblocks:` names a ticket, not an increment. Errands get a `(errand)` line in Decisions so far, never in the design document |
| WD-B6 | WD22 immutability starts at first Publish | confirmed 2026-10-08 | Unpublished increment rows may be edited freely; a published row only changes its `Published` cell |
| WD-B7 | Revise's Reopen | confirmed 2026-10-08 | The user's Revise instruction counts as the explicit instruction MD11 needs, so Revise has domain-modeling reopen rows whose `Ref` is the revised ticket (WD8). The reason is the user's revision |
| WD-B8 | `scratch:` refs | confirmed 2026-10-08 | `scratch:wayfinder/<map>/<file>`, the path under `.scratch/`. Ticket files are `NN-<slug>.md`, numbers never reused |
| WD-B9 | Publish runs the translator's checks too | confirmed 2026-10-08 | `DESIGN-FORMAT.md` lists 13 checks: WD21's two, WD17's naming and size rules, and Juval's validation list. Juval's `Created by` is spelled `Introduced in` (WD21). `changed` lists section names |
| WD-B10 | Upstream base | confirmed 2026-10-08 (record only) | Adapted from mattpocock/skills @ `f3fc563` (newer than S6's `6fd9479`). The wayfinder changes since then are the label, real-id, no-PR and resolve-by-type fixes, and the port already covers each one |
| WD-B11 | Check 4 means "no rejected form", in the destination's context (S10) | confirmed 2026-10-08 | As built, Publish read WD17(c)'s "named in settled terms" as "every term has a `GLOSSARY-SETTLED.md` row" and refused a clean toy map, since that file records only contested rulings and nothing in Resolve settles increment names. It also couldn't tell which context to look in ("work item" is rejected in Wayfinder, but the map was about the port ledger). `DESIGN-FORMAT.md` check 4 now runs `Lookup` on the terms in increment names and behaviours in the context whose `GLOSSARY-MAP.md` description covers the destination. Only a `rejected-form` hit fails, a term with no row passes, and no covering context means no row applies. Charting-time "can't be named in settled terms is fog" (SKILL.md, MAP-FORMAT) is unchanged: there it is the agent's judgment, not a gate |
| WD-B12 | Begin checks the size before grilling (S10) | confirmed 2026-10-08 | Rich's interactive Step D 2 (a Python dataclass; `echo "Hello World"`) got a full grilling round before "no map needed", because Begin's only size check sat in step 2, after the destination round. Begin now has a step 0: if the idea as stated plainly fits in one session, say a map isn't needed and ask how to proceed, without loading grilling or writing anything; when in doubt, go on, and step 2 still catches the rest. Headless re-runs: both small ideas stop at once; a large idea (`/ledger-lint`) still grills |
| WD-B13 | Revise repoints `Decided by`, and its replacement is a decision ticket (S10) | confirmed 2026-10-08 | Rich's Step D 6 on a real map left I1 and I3's `Decided by` on the revised ticket, which would fail Publish check 3 (the design document shows a revised ticket only through its replacement). Revise step 3 now repoints `Decided by` in unpublished rows; a published row is listed as a dependent and the next Publish withdraws and replaces it. A headless re-run then made the replacement an errand inside `Decided by`, so step 2 now says the replacement is a decision ticket, with an errand ahead of it (`Unblocks:` the replacement) if a manual step comes first. Re-run on a copy of Rich's map: both hold |
| WD-B14 | A prototype ticket waits for its verdict in `in progress` (S12) | unconfirmed | WD7 and PD1 make the user's verdict the only way to close it, and WD15 allows one ticket per session. So the ticket stays `in progress` until the user rules, even across sessions, and blocks other tickets on the map as any `in progress` ticket does. Naming it in Resolve resumes it by handing the existing prototype over again |
| WD-B15 | Wayfinder writes the prototype Resolution; a turned-away question goes back to the user (S12) | unconfirmed | Wayfinder asks `prototype` to return the verdict to it rather than write the ticket, so the ticket has one writer. The Resolution gives the question, the user's verdict in their own words and a link (`prototype/<name>` branch and path, or "not kept"). If `prototype`'s question check refuses (settled, whole application, grillable), wayfinder says the ticket may be mis-kinded and asks; it never changes `Kind` itself (Kind is read, never inferred) |
| WD-B16 | Pending prototypes live outside the map folder (Q1, W7) | confirmed 2026-10-08 (Rich, after S12) | With no app in the repo, S12's run put the prototype in `.scratch/wayfinder/<map>/`, so committing the map while a verdict was pending would commit it too and break MAP-FORMAT's folder contents. Rich chose `.scratch/prototypes/<map>/`, named after the ticket (`<NN>-<slug>.prototype.html` for a single file). Not gitignored, because `prototype` keeps a prototype by committing it to `prototype/<name>`. Wayfinder's prototype bullet tells `prototype` the location when it hands over; `plugins/prototype` is unchanged. Exception: a UI prototype that has to sit inside the app. The handoff named only sub-shape A (switcher on an existing page); W7 also exempts sub-shape B (a throwaway route), since a route has to follow the app's routing |

Still open: everything Rich owes is in [Rich's queue](#richs-queue).

## Inputs to triage

Raw material from the session 1 read of Matt's repo. Not commitments; each one
becomes a work item, a decision, or `dropped`.

S6 dispositions:
- `setup-matt-pocock-skills` tracker operations → WD2 (the map on disk, format
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
| S8 | 2026-10-07 | W1, W2 · Batch rename + first glossary rows | W1: "slice" → "batch" in `BOOTSTRAP.md` and MD9. W2: two Eric consults; Eric moved all four terms into the Wayfinder context, objected to a squadra copy row, sharpened three wordings and two description lines; Rich accepted all (WD27). Wrote `GLOSSARY-SETTLED.md`, `GLOSSARY-MAP.md`, `plugins/wayfinder/GLOSSARY.md`; Lookup test and WD19 done-test pass; fixed two stale "board" uses in port docs | `handoffs/S9-wayfinder-build.md` |
| S9 | 2026-10-07 | W3 · Wayfinder build | One batched Eric consult (Ticket, Decision ticket, Design document approved with sharper wording; Cleared objected as event → state; GLOSSARY.md intro line) and Rich accepted all (WD28). Built `plugins/wayfinder` (SKILL.md, MAP-FORMAT.md, DESIGN-FORMAT.md, manifest, upstream MIT LICENSE, marketplace entry, README section, runbook); validated; recorded WD-B1–B10. Fixed a leftover "slice" in the domain-modeling runbook (WD20) | `handoffs/S10-wayfinder-smoke.md` |
| S11 | 2026-10-07 | W5 · Prototype build (parallel with S8, branch `feat/prototype-plugin`) | One grilling round on upstream vs WD7 (PD1–PD6 in W5's notes); built `plugins/prototype` (SKILL.md, LOGIC.md, UI.md, manifest, upstream MIT LICENSE, marketplace entry, README section, runbook); validated; three headless smoke runs passed. Draft PR into `feat/wayfinder-domain-modeling` | None (W6 waits for W3; S10 writes S12's handoff once W5 merges) |
| S10 | 2026-10-07 | W4 · Wayfinder smoke | Five headless runs plus one re-run: Begin with answers (map written), Begin without answers (asked first, wrote nothing), Resolve (one research ticket closed), Publish fail (checks named, nothing written), Publish pass (refused on check 4, fixed as WD-B11, re-run wrote a cleared document). Toy maps and `docs/design/` output deleted. Fixed `TEMPLATE.md`'s retired `grill-me` example | `handoffs/S12-prototype-wiring.md` |
| S12 | 2026-10-08 | W6 · Prototype wiring | Wayfinder's prototype tickets now call the `prototype` skill (WD-B3 → `replaced (W6)`; WD-B14–B15 unconfirmed). Updated `SKILL.md`, `MAP-FORMAT.md`, runbook (Step D 8), README. Validated; one headless Resolve on a toy map handed over without picking or closing. Toy map and prototype deleted. Port units done; afterwards Rich set the order Q1 (W7 + his queue) → S13 (W8) → PR to main (W9) | `handoffs/Q1-rich-queue.md` |
