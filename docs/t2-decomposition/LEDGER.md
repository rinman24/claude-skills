# T2 · Löwy's decomposition across wayfinder, design-to-board and target repos: ledger

Goal: enforce the decomposition design-to-board's DB-D18–DB-D23 rule.
- Wayfinder decides the structure.
- design-to-board verifies the plan.
- Target-repo CI verifies the build with the import-direction check.
- A conformance check compares a delivered map with its design document.
- squadra stays naive.

This is T2 from the wayfinder port. Its row in `docs/wayfinder-port/LEDGER.md`
holds the history up to S0. This ledger is the source of truth from S0 on;
the port row only points here.

Branches: each session branches from `origin/main` as `docs/t2-<unit>` or
`feat/t2-<unit>`, in a new worktree under `.claude/worktrees/`. It ends with a
PR to main, as T2c-R, T2c-R2 and T2c-J did. This ledger lives on main.

## Starting decisions

Cite these by ID; don't copy them here.

- design-to-board `docs/design-to-board/LEDGER.md`:
  - DB-D18: where the decomposition is enforced;
  - DB-D19: `Calls`, the composition rules, contract operations and type pairs;
  - DB-D20: an Engine may call ResourceAccess;
  - DB-D21: build by layers, in pulses with milestones;
  - DB-D22: the import-direction check enforces declared edges through a
    per-service allow-list, with no baseline from the code graph;
  - DB-D23: T2c builds the sandbox skeleton and proves the conformance check
    on fixtures; sandbox r5; advisory until calibrated.
- Tool rulings: `research/T2C-TOOL-RESEARCH.md` and
  `research/T2C-STATE-OF-THE-ART.md`, their "Rulings" tables.
  - The service layout (the former "layer map", T2-D3) is target-owned.
  - gswa-backend is an example only.
  - import-linter is the CI tool.
  - The conformance check is built on grimp and griffe.
  - The tool has its own public repo with semver tags.
  - Output starts as plain text.
- Names: `~/Code/board-knowledge/sessions/2026-10-28-eric-decomposition-vocabulary.md`,
  Choice: proving path, conformance check, surplus, shortfall. Its follow-up,
  `2026-10-28-eric-decomposition-vocabulary-followup.md`, was adopted as
  written at T2-E ([T2-D2–T2-D6](#decisions)). The terms are settled in
  `docs/service-decomposition/GLOSSARY.md`, the Wayfinder glossary and
  `GLOSSARY-SETTLED.md`.
- [T2-D1](#decisions): protecting the rule sources.

## Repo facts

- **Target repo:** `rinman24/squadra-sandbox`.
  - Private, default branch `main`, cloned at `~/Code/squadra-sandbox`.
  - As of 2026-10-28 it holds only `README.md` and `squadra.toml`, with no
    rulesets and no CI.
  - Board history is in `docs/design-to-board/LEDGER.md`, Repo facts.
- **gswa-backend:** an example only. Read it if useful; never edit it or run
  anything against it.
- **plumb:** the tool. It holds the config generator, the config check and
  the conformance check (T2-D3). The repo `rinman24/plumb` is free but not
  created yet; T2c-2 creates it, public, with semver tags.
- **squadra:** `rinman24/squadra`, public. Its side of T2 is its N39.
- **Board sessions:** `~/Code/board-knowledge/sessions/`.
  - Juval, 2026-10-28: `where-enforce-service-decomposition`,
    `engine-calls-resourceaccess`, `layers-vs-dependencies-agents`,
    `ci-strictness-sandbox-sequencing`.
  - Juval, 2026-10-09: `services-layer-enforcement`.
  - Eric, 2026-10-28: `decomposition-vocabulary`.

## Session budget

Same as the port: under ~100K tokens per session, hard ceiling 120K, ~80K
of planned work per unit, one unit per session. Near the ceiling, stop,
update this ledger and write the next handoff.

## How sessions hand off

Handoffs are prompt files in `handoffs/`. Under HD1 they stay out of git
(`.gitignore`: `docs/*/handoffs/`): each lives in the worktree of the session
that wrote it, and that session tells Rich the absolute path. Write them from
`HANDOFF-TEMPLATE.md`, which is tracked. To start a session, open a terminal
in `~/Code/claude-skills`, start `claude`, and give it the handoff (paste it,
or send its path). The handoff says which branch and worktree to create.

## Session protocol

Start:
1. Read the handoff prompt.
2. `git fetch`; branch from `origin/main` in a new worktree.
3. Read this ledger and `LESSONS-LEARNED.md`.
4. Mark the unit `in progress` in [Work items](#work-items).

End:
1. Update item statuses and the session log.
2. Update [Rich's queue](#richs-queue), and record his rulings in
   [Decisions](#decisions).
3. Append lessons to `LESSONS-LEARNED.md`.
4. Write the next handoff from `HANDOFF-TEMPLATE.md` into `handoffs/` (local, HD1).
5. Commit, push with
   `git -c credential.helper= -c credential.helper='!gh auth git-credential' push`,
   and open a PR. If main moved, merge `origin/main` into the branch; never
   rebase or force-push.
6. Tell Rich the PR, the handoff path and what's open in his queue.

## Status legend

`todo` · `in progress` · `done` · `blocked` · `dropped`

## Rich's queue

- [ ] Start T2a, wayfinder's DESIGN-FORMAT and the Publish step
  (`/Users/richinman/Code/claude-skills/.claude/worktrees/t2-e/docs/t2-decomposition/handoffs/T2a-design-format.md`).
  It is on the critical path, and T2b and T2c-2 wait on it.
- [ ] `/ask-juval` on the four project-design items under [Open items](#open-items):
  same-pulse edges, milestones against check 5, Query→Result at the Manager,
  and use case as B<n>. This doesn't block T2a, which marks them pending, but
  T2b's pulse checks need same-pulse edges and check 5 settled.
- [ ] Start T2c-1, the sandbox skeleton (`/Users/richinman/Code/claude-skills/.claude/worktrees/t2-s0/docs/t2-decomposition/handoffs/T2c-1-sandbox-skeleton.md`).
  It can run in parallel with T2-E.
- [ ] Before sandbox r5, the bookkeeping carried from design-to-board S16:
  1. Add `[fleet] name` to `~/Code/squadra-sandbox/squadra.toml`, and commit
     it on the sandbox's `main`.
  2. Reinstall squadra at `main`.
  3. Run `squadra init --check --provider github` there.

## Work items

| ID | Item | Depends on | Est. | Status | Notes |
|---|---|---|---|---|---|
| S0 | Set up T2: this ledger, lessons, template, handoffs for T2-E and T2c-1; rule question 6 (T2-D1) | — | ~35K | done | |
| T2-E | `/ask-eric` follow-up, then settle terms with the domain-modeling skill | — | ~60K | done | T2-D2–T2-D6. Created the Service decomposition glossary; added three Wayfinder terms, six GLOSSARY-MAP lines and 21 settled rows |
| T2a | Wayfinder: DESIGN-FORMAT and the Publish step. Covers the `Calls` column and Services' declaring and referenced rows (T2-D4), contract operations and type pairs, DB-D20 and DB-D21 Rules lines, and the gap rulings (T2-D6) | T2-E | ~80K | todo | Splits if the gaps add more than ~20K |
| T2b | design-to-board: composition-rule checks; `Depends on` derived from call edges; T2-D4's four `Calls` checks; operation-count warnings; pulse and milestone ordering | T2a | ~80K | todo | |
| T2c-1 | Sandbox skeleton (DB-D23) and T2-D1 | — | ~70K | todo | Handoff written. Hand-written import-linter config until T2c-2's generator replaces it |
| T2c-2 | Create plumb's repo (`rinman24/plumb`). Build the config generator (`plumb config`): a per-service allow-list from each service's latest declaration, plus a rules-only tier (DB-D22). Build the config check (`plumb config --check`, T2-D2) and its separate CI job, and replace T2c-1's hand-written config | T2-E (name), T2a (format), T2c-1 | ~80K | todo | Includes the composite Action and the Azure step from T2C-STATE-OF-THE-ART §3 |
| T2c-3 | Conformance check in plumb (`plumb conformance`), proved on seeded fixtures: a known surplus edge, a shortfall, an undeclared operation and a missing module against a hand-written document; it must report exactly those (DB-D23) | T2c-2 | ~80K | todo | JSON is the record and Markdown is rendered from it, with three outcomes per surface: `match`, `surplus`, `shortfall` (T2-D2) |
| T2-r5 | Sandbox r5: the first map squadra builds, delivered through merges, then checked. Advisory until a run has zero check defects (DB-D23) | T2a, T2b, T2c-3, squadra delivering through merges, `[fleet] name`, the sandbox's glossary seeded (T2-D6) | ~80K | todo | If squadra can't yet deliver through merges, that gap goes on squadra's ledger and T2c still closes on its fixtures |

## Open items

- **T2-D1 and identity.** If squadra opens PRs as `rinman24`, GitHub won't
  let Rich approve his own PR. A required code-owner review with no bypass
  would then block every agent PR that touches a protected path. T2c-1 checks
  which identity squadra uses and what the account's plan allows. Rulesets and
  enforced CODEOWNERS on a private repo need GitHub Pro or above; the S0 token
  couldn't read the plan. It brings any conflict to Rich rather than adding a
  bypass.
- **For Juval (project design, from T2-E).** Eric noted these and left
  them unruled:
  - **Same-pulse edges.** A queued call into a new Manager, or a Utility
    calling a new Utility, needs a `Depends on` inside one pulse, which
    DB-D21 forbids. One of the two has to give.
  - **Milestones against check 5.** A pulse milestone is an increment, so by
    definition it counts toward "about 6 live increments". Whether to exclude
    milestones is a planning rule. Check 5 must say which applies.
  - **Query→Result at the Manager.** Confirm Löwy has no conflicting kind for
    a read at the Manager (T2-D6).
  - **Use case as behaviour B<n>.** If B<n> isn't a use case in Löwy's sense,
    drop the term and shrink the check to "Clients call only Managers"
    (T2-D6).

  T2a writes DB-D21 as ruled and the T2-D6 defaults. It marks these four as
  pending rather than deciding them.

## Decisions

| ID | Decision | Status | Source |
|---|---|---|---|
| T2-D1 | The rule sources in each target repo are protected. These are the layer map, `docs/design/` and the generated import-linter config, plus any exemptions file. Rich is their CODEOWNER. A ruleset on `main` requires the import-direction check as a status check and code-owner review for those paths. No bypass actors: no Copilot coding agent and no squadra bot identity. Large organisations route boundary changes to a human owner (T2C-STATE-OF-THE-ART §1) | ruled 2026-10-28 (Rich, T2 S0) | T2c-R2 question 6, as recommended. DB-D23's "advisory until calibrated" governs whether the edge gate blocks; T2-D1 governs who may change the rules |
| T2-D2 | Three checks, each defined by when it runs and what it can report, never by what it reads. The **import-direction check** runs on every PR and reports forbidden imports. The **config check** runs on every PR and reports a stale config; this was called the "drift check", a name now rejected because drift means code departing from the design. The **conformance check** runs once per delivered map and reports a **match**, **surplus** or **shortfall** on each of its three surfaces. These are also the JSON outcome values, and "conforms" in T2C-STATE-OF-THE-ART's Rulings now reads as match | ruled 2026-10-29 (Rich, T2-E) | Eric, `~/Code/board-knowledge/sessions/2026-10-28-eric-decomposition-vocabulary-followup.md`, adopted as written. T2c-R2 question 7, with framing (a) as the definition. Framing (b), that only the generator reads documents, is a fact about how plumb is built and goes in plumb's design notes. Surplus and shortfall are triaged as a document, squadra or check defect (DB-D23), which replaces "the defect goes to wayfinder" |
| T2-D3 | Names. The tool is **plumb** (`rinman24/plumb`), with three commands: `plumb config` generates the config, `plumb config --check` is the config check, and `plumb conformance` is the conformance check. The layer map is the **service layout**: the target-owned file that places each service at its repo path, names the composition root and records each exemption with its reason. One import-linter entry is an **import rule**. import-linter's own words (contract, layers, forbidden, protected) stay inside the generated config. The design document is authoritative for the layer of any service it declares. The service layout's layer applies only to rules-only services, and the config check fails if the two disagree | ruled 2026-10-29 (Rich, T2-E) | Eric, `~/Code/board-knowledge/sessions/2026-10-28-eric-decomposition-vocabulary-followup.md`, adopted as written. T2c-R2 question 8. Eric's naming test: "map" is settled in Wayfinder, and "contract" already means a service's public operations. The name was free, per Rich on 2026-10-29. Name metaphors (line, bob, true) never enter the glossary. T2-D1's "layer map" refers to the service layout |
| T2-D4 | `Calls` and absence. A `Calls` cell holds one of three things. `none` means the service is declared to call nothing. A list of names, such as `B, C (queued)`, is the complete set it calls, never the change. A blank cell means not declared, and it is legal only on a referenced service's row. A **declaring row** is for a service the map creates (`Introduced in`) or changes (named in a `Touches`). Its `Calls` cell is that service's **declaration**. A **referenced service** is one the map neither creates nor changes, listed only because a declaring row calls it. It has a Layer, and its `Encapsulates`, `Introduced in` and `Calls` are blank. It is never a declaration. Services becomes "the services this map creates, changes or calls", and the 2-service rule still counts `Touches` only. Publish runs four checks: every callee has a Services row, every row has a Layer, a declaring row's `Calls` isn't blank, and a referenced row's `Calls` is blank. DB-D22's "lists it" reads as "declares it" | ruled 2026-10-29 (Rich, T2-E) | Eric, `~/Code/board-knowledge/sessions/2026-10-28-eric-decomposition-vocabulary-followup.md`, adopted as written. DB-D22's two format consequences, which turn out to be one problem. A referenced row counted as a listing would put B into the edge-enforced tier with an empty allow-list. For T2a (format) and T2b (design-to-board checks) |
| T2-D5 | The **Service decomposition** context covers Löwy's Method as applied in target repos: layers, contracts, type pairs, call edges and the three checks. Its glossary is `docs/service-decomposition/GLOSSARY.md`, which check 4's `Lookup` resolves against. Context map: Wayfinder → Service decomposition and design-to-board → Service decomposition are Conformist. plumb → Service decomposition is Conformist, and plumb coins no terms. Wayfinder → plumb is Published Language. plumb → import-linter is an Anticorruption Layer: plumb's config generator is the only place the translation happens. Pulse, pulse milestone and proving path are Wayfinder terms | ruled 2026-10-29 (Rich, T2-E) | Eric, `~/Code/board-knowledge/sessions/2026-10-28-eric-decomposition-vocabulary-followup.md`, adopted as written. The term table as amended, with Layer and Composition rule added. Eric's review changed his "Conformist" for import-linter to Anticorruption Layer and reversed the plumb arrow to match the map's convention; Rich approved both. GLOSSARY-SETTLED gained 21 rows. Proving path rejects Spike and Pilot, and Vertical slice stays rejected under Subsystem. Type-pair words stay qualified in design-to-board code (`TypePair.FACTS_TO_PLAN`), never a bare `Plan`. The translation notes on Command and Spec are in the glossary |
| T2-D6 | Gap rulings, for T2a and T2b. (1) Use case: Löwy's term. In a design document it is a behaviour B<n>, and "one Manager per use case" is checked only in review. (2) Query→Result is a fourth type-pair kind, at the Manager only. A ResourceAccess read stays Spec→Rows. (3) A ResourceAccess write returns Rows when the caller needs what was stored, and nothing otherwise. A bare identity is a legal ResourceAccess input. (4) Increments get a `Pulse` column. (5) An edge is introduced conservatively: every increment touching A depends on B's `Introduced in`. (6) The naming questions plus the Engine question are DB-D19's "business verbs, not CRUD" test. The CRUD-verb lint is a warning, and check 4's `Lookup` extends to operation and Engine names. (7) The sandbox's glossary is seeded before r5. Eric's blocking question 2 and the gswa renames drop | ruled 2026-10-29 (Rich, T2-E) | Eric, `~/Code/board-knowledge/sessions/2026-10-28-eric-decomposition-vocabulary-followup.md`, adopted as written. Same-pulse edges, milestones against check 5, and Juval's confirmations of (1) and (2) are under Open items, for Juval. Operation-count thresholds, the pulse order, the "<Layer> complete: …" milestone names and the proving-path Rules line come from Eric's first session and go into DESIGN-FORMAT at T2a |

## Session log

Sessions before S0 (T2c-R, T2c-R2, T2c-J) are logged in
`docs/wayfinder-port/LEDGER.md`.

| Session | Date | Unit | Outcome | Handoff written |
|---|---|---|---|---|
| S0 | 2026-10-28 | S0 · set up T2 (branch `docs/t2-s0`) | Created this ledger, `LESSONS-LEARNED.md`, `HANDOFF-TEMPLATE.md`, and handoffs for T2-E and T2c-1 (local under HD1, in the `t2-s0` worktree). Units T2a–T2-r5 sized from DB-D18–DB-D23 and the T2c rulings. Rich ruled question 6 (T2-D1). The port ledger's T2 row now points here | `/Users/richinman/Code/claude-skills/.claude/worktrees/t2-s0/docs/t2-decomposition/handoffs/T2-E-eric-followup.md`, `/Users/richinman/Code/claude-skills/.claude/worktrees/t2-s0/docs/t2-decomposition/handoffs/T2c-1-sandbox-skeleton.md` |
| T2-E | 2026-10-29 | T2-E · `/ask-eric` follow-up and settled terms (branch `docs/t2-e-eric`) | Eric's follow-up session (`2026-10-28-eric-decomposition-vocabulary-followup.md`) was adopted as written, and the tool is named plumb. Rulings T2-D2–T2-D6. domain-modeling, with Eric's review, created `docs/service-decomposition/GLOSSARY.md` (29 terms) and added Pulse, Pulse milestone and Proving path to Wayfinder's glossary, six GLOSSARY-MAP lines and 21 GLOSSARY-SETTLED rows. `<tool>` replaced by plumb. Four project-design items went to Open items for Juval | `/Users/richinman/Code/claude-skills/.claude/worktrees/t2-e/docs/t2-decomposition/handoffs/T2a-design-format.md` |
