# T2c tool research: conformance check and import-direction check

Session T2c-R, 2026-10-28. Research only; Rich rules the tool and the owner.
Inputs: port ledger row T2, design-to-board DB-D18–DB-D21, Juval's
2026-10-28 sessions (`where-enforce-service-decomposition`,
`engine-calls-resourceaccess`) and 2026-10-09 (`services-layer-enforcement`),
`DESIGN-FORMAT.md`, gswa-backend at `8a14d9c`. Eric's decomposition
vocabulary session had not landed, so the names here (`Calls`, reconciliation
diff, layer map, reconciler) are provisional.

Spike artifacts (configs, scripts, raw output) are in [`t2c-spike/`](t2c-spike/).

## Rulings after this report (Rich, 2026-10-28)

| Question (section 6) | Ruling |
|---|---|
| 1, 2 · Tool and home | Not ruled. A second research pass with subagents looks at state-of-the-art practice at GitHub scale: `docs/wayfinder-port/handoffs/T2c-R2-state-of-the-art.md` |
| 3 · Service to code mapping | **A layer map in the target repo** (Juval, 2026-10-09) |
| 4 · Classification (gswa) | **No changes to gswa-backend**; it was an example only. The spike's gswa findings are illustrations, not work items |
| 5 · CI strictness; 7 · sandbox sequencing | One `/ask-juval` session: `docs/wayfinder-port/handoffs/T2c-J-juval-ci-strictness-sandbox.md` |
| 8 · Names | Folded into Eric's vocabulary work. Eric's 2026-10-28 session landed after this report. Rich's Choice there renamed the diff to **conformance check**, with surplus and shortfall as its findings; this report now uses those names. "reconciler" is a rejected form (it collides with Reconcile) and stays a placeholder until Eric names the tool and the layer map. Eric's term table, which is still unruled, proposes that the import-direction check "reads code only, never the design document". That bears on question 5. Once Eric answers, settle the terms with the domain-modeling skill |

## 1. Recommendation

| Half | Recommended tool | Why |
|---|---|---|
| CI import-direction check | **import-linter 2.15**, its config generated from the design documents plus a target-owned layer map | The most expressive tool that is configured rather than coded: `layers` (with `|` independent and `:` open siblings), `protected`, `forbidden`, `independence`, wildcards, and `ignore_imports` for the queued Manager→Manager edge. It catches indirect chains. BSD-2, released since 2019, maintained by grimp's author, and its graph is Rust-backed. Caught every real violation in the gswa spike |
| Conformance check: modules and edges | **grimp 3.18** (the graph under import-linter) through a ~20-line script | Gives module-level edges with file and line, as data. Builds gswa (173 modules) in 7 ms. Because it is the same graph the CI gate uses, the diff and the gate cannot disagree about what an edge is |
| Conformance check: contract operations | **griffelib 2.4.x** (griffe) through a ~30-line extractor that writes our own JSON schema | Static, so gswa isn't imported and the `Settings()` side effect is avoided. Resolves each parameter and return type to its full dotted path. Recovered every operation and type pair on gswa's contracts |

**Does one tool cover both halves?** No off-the-shelf tool does. Nothing on
the market diffs contract operations against a document, and only Tach
reports declared-but-unbuilt edges. The coherent answer is a single small
package, the reconciler (working name), with one Manager and two use cases:

- `reconciler diff --map <map>` (half 1): reads the design document, uses
  grimp for modules and edges and griffe for operations, and writes the
  diff.
- `reconciler config [--check]` (half 2's generator): writes the
  import-linter contracts from the union of `docs/design/*.md` plus the
  layer map. `--check` regenerates and fails on any difference.

CI then runs plain `lint-imports`. Both halves read one graph (grimp) and one
rule source (the document plus the layer map). That is Juval's "the same
diff" made literal.

**Runner-up: Tach 0.35.3.** It is Rust end to end. Its per-module
`depends_on` maps one-to-one onto a `Calls` cell. With `exact = true` it
reports both surplus and unbuilt edges, which is the edge half of the diff
almost for free. It loses on health: Gauge abandoned it in mid-2025, and
since 2025-11 it has been revived under `tach-org` by one maintainer. It
also loses on output: its JSON carries surplus edges only, and unused
dependencies appear in text only. It would be the pick if bus factor
mattered less than a one-file config.

## 2. Candidates

Checked 2026-10-28 against PyPI JSON, the GitHub API and each repo's docs.
"Commits" counts commits since 2026-04-28.

| Tool | Repo | Latest release | Maintenance | Licence / lang | Rule expressiveness for DB-D19/D20 | JSON out | Verdict |
|---|---|---|---|---|---|---|---|
| import-linter | github.com/seddonym/import-linter | 2.15, 2026-09-04 | 32 commits; not archived; 74 open issues; ships a pre-commit hook | BSD-2 / Python on grimp (Rust) | High. Layers with independent or open siblings, `containers`, `protected` (allow-list importers), `forbidden`, `independence`, `*`/`**` wildcards (whole segments only), `ignore_imports`, indirect-chain detection, `broken_contract_guidance` | No (text only) | **CI pick** |
| grimp | github.com/python-grimp/grimp | 3.18, 2026-10-26 | 41 commits; wheels for 3.15 and free-threaded builds | BSD-2 / Rust core | Not a rule engine: graph queries (`find_matching_direct_imports`, `get_import_details`, chains) | Via its API | **Edge-dump pick** |
| Tach | github.com/tach-org/tach (formerly gauge-sh) | 0.35.3, 2026-10-06 | 34 commits; revived 2025-11 by one maintainer (issue #791); pre-commit mirror stale since 2025-04 | MIT / Rust | High. Layers (needs `layers_explicit_depends_on = true` or skip-layer imports pass), per-module `depends_on`, `utility`, `visibility`, `interfaces`, `exact` (unused deps) | Yes for violations; `tach map` gives file edges | Runner-up |
| ruff `analyze graph` | github.com/astral-sh/ruff | 0.17.3, 2026-10-27 | Very active | MIT / Rust | None: graph only | File-level edges, no line numbers (#20737), misses implicit `__init__` edges (#13482) | Still "experimental"; fallback edge dump |
| deply | github.com/Vashkatsi/deply | 1.3.0, 2026-10-23 | 66 commits | BSD-3 / Python | Deny-only regex layers, so a poor fit for an allow-list `Calls` | JSON, SARIF, Mermaid; baseline | No |
| pytestarch | github.com/zyskarch/pytestarch | 5.1.0, 2026-10-24 | 40 commits | Apache-2.0 / Python | Fluent rules written in pytest code | Via pytest | No: rules are code, so hard to generate |
| ArchUnitPython | github.com/LukasNiessen/ArchUnitPython | 1.8.1, 2026-10-06 | 100 commits; created 2026-04 | MIT / Python | Fluent rules in code | Via pytest | Watch; same objection |
| ruff TID251 / flake8-tidy-imports | astral-sh/ruff; adamchainz/flake8-tidy-imports | 0.17.3 / 4.12.0 (2025-09-08) | Active / slow | MIT | A project-wide banned list only, with no per-source scope | Ruff JSON | No |
| pydeps | github.com/thebjorn/pydeps | 3.0.9, 2026-10-01 | 35 commits | BSD-2 / Python | Visualisation only | `--deps-output` | No |
| stratalint | PyPI only; its repo link returns 404 | 0.20.0, 2026-07-18 | Unverifiable, self-described pre-release | Apache-2.0 / Rust | n/a | n/a | No |

Contract-surface candidates:

| Tool | Release | Maintenance | Licence / lang | Operation + input type + output type per contract | Verdict |
|---|---|---|---|---|---|
| griffe / griffelib (github.com/mkdocstrings/griffe) | 2.4.1, 2026-10-22 | 10 releases in 2026; split into `griffelib` and `griffecli` at 2.0 | ISC / Python | Excellent through the API (full type paths via `canonical_path`). `griffe dump` JSON follows its internal model with no versioned schema, so it is an input, not the thing diffed | **Pick** |
| stdlib `ast` / libcst | stdlib / 1.9.0, 2026-07-29 | n/a / Meta, active | MIT / Python + Rust | Good, but you write cross-module name resolution yourself (~150–300 lines) | Only if zero dependencies is a hard rule |
| pyright / basedpyright | 1.1.414 / 1.40.2 | Active | MIT / TypeScript | `--outputjson` gives diagnostics only; `--verifytypes` gives symbol lists, not signatures | Optional "fully annotated" gate |
| mypy stubgen | 2.4.1, 2026-10-28 | Active | MIT / Python | Writes `.pyi` text, which must be parsed again | No |
| Runtime `inspect` / `get_type_hints` | stdlib | n/a | n/a | Precise, but imports gswa (settings and env side effects) and needs a full install | No |
| aexpy, surface, oneport-apidiff | 2024 / 2019 / 2026-10 | Stale / dead / new | n/a | API break-diff between versions, not code vs document | No |

## 3. Spike on gswa

Run against a scratch copy of gswa-backend (`8a14d9c`). The copy has been
deleted, and gswa-backend itself was not touched.

**Prerequisite found.** grimp (so import-linter) and griffe both silently skip
folders without `__init__.py`. gswa has 11, including `utility`, `config`,
`access/outbox` (which holds a `contracts.py`), `authn/ports` and
`authz/engines/strategy`. import-linter fails on `gswa.utility` with "module
does not exist". ruff saw them. The spike added the files in the scratch
copy. In a target repo, ruff's `INP001` (implicit namespace package) rule
enforces this for both tools at no cost.

### import-linter 2.15: [`importlinter.toml`](t2c-spike/importlinter.toml), [output](t2c-spike/lint-imports-output.txt)

Five contracts:
- closed `layers` (Client > Manager > Engine > ResourceAccess > Utility, with
  independent siblings in the service layers and open siblings among
  utilities);
- Clients-call-Managers-only (`forbidden`, composition root ignored);
- no Engine→Engine (`independence`);
- no ResourceAccess→ResourceAccess on implementation modules
  (`independence`);
- closed subsystems (`independence` across `accounts`, `authn`, `authz`).

Run time is well under a second. Result: 2 kept, 3 broken, 7 violating module
pairs:

| Caught | Kind | Real? |
|---|---|---|
| `config.static_config → access.external.email.params` | Utility imports ResourceAccess (up) | Yes |
| `access.role_scope → access.role`, `→ access.scope`; `access.user_invite → access.user` | RA→RA, but only on contract DTOs (`RoleRow`, `UserRow`) | Depends on a ruling: is sharing Row types between RA contracts legal? |
| `workers.outbox_runner → access.external.email…`, `workers.outbox_dispatcher → access.outbox…` | Client→RA | Depends on whether workers are Clients or a Manager-hosting process |
| `accounts.manager → authn.engines.password_policy_engine`, `→ authn.ports`, `→ authn.domain` | Cross-subsystem bypass (Manager reaches another subsystem's Engine) | Yes, unless the document's `Calls` declares it |

Missed or out of reach:
- **Composition root.** `gswa/api/dependencies/**` imports Engines and Access
  directly to wire Managers. The spike exempted it, which suppressed 42
  imports. Real Client→Engine calls hiding there would pass too.
- **Unlisted packages are unconstrained by `layers`.** Subsystem `contracts`,
  `domain` and `ports` (and `access.models`, `access.relational`) aren't
  listed. Only the closed-subsystems contract caught `accounts → authn.ports`.
- **Semantics.** Whether `user_query_engine` sequences work like a Manager
  (Juval's DB-D20 flag) is invisible to any import tool: Engine→RA is legal.
- **Expressiveness limits.** Wildcards replace whole segments only, so
  `gswa.access.*.*_access` is rejected and the generator must enumerate
  implementation modules. The `layers` list takes no wildcards.

### grimp 3.18: [`grimp_edges.py`](t2c-spike/grimp_edges.py), [output](t2c-spike/grimp-edges-output.txt)

It built the graph in 7 ms and produced 14 service-to-service edges, each with
an example `module->module:line`. Examples: `AccountManager -> AuthnEngines`,
`AccountsEngines -> UserAccess`, `RoleScopeAccess -> RoleAccess`. This is the
built side of the edge diff.

### Tach 0.35.3: [`tach.toml`](t2c-spike/tach.toml), [output](t2c-spike/tach-check-output.txt)

One `[[modules]]` per service, with `depends_on` playing the role of a
hypothetical `Calls` cell, and `exact = true`. It ran in 0.23 s and produced
36 JSON diagnostics across 13 module pairs. It caught the same real findings
as import-linter. The Utility→RA case was reported as a `LayerViolation`;
the composition root's 14 imports from `api` surfaced because no exemption was
configured. With `exact`, it also listed declared edges that were never
built: `api` doesn't import the authn or authz Managers, `authz.manager`
doesn't import `authz.engines` or `access.role`. That is the "missing" side
of the diff. It **missed** `accounts.manager → authn.ports/domain`, because
packages that aren't declared modules are unchecked.

### griffe 2.4.1 (agent B): [`griffe_contract_surface.py`](t2c-spike/griffe_contract_surface.py)

Static load of 137 modules in about 22 ms. Every operation came back with its
input and output types resolved, for example:

```
UserAccess.create async (spec: gswa.access.user.contracts.CreateUserSpec) -> gswa.access.user.contracts.UserRow
AccountAdminManager.create_account async (command: …create_user.CreateUserCommand) -> …CreateUserResult
InviteTokenEngine.create sync (*, facts: …domain.invite_token.CreateInviteFacts) -> InviteTokenPlan
```

Departures from the strict type pairs that the diff would flag:
- `UserAccess.get_users_with_latest_activation(*, query: UserListAccessQuery)`
  takes a Query, not a Spec.
- Primitive inputs such as `get_by_id(user_id: int)`.
- Engine helpers on plain types (`hash_token(str) -> str`).
- `LoginPlan` is a union alias that must be expanded.

Contracts are plain concrete classes, not Protocols, and carry no marker.
`AccountAdminManager` lives in `account_manager.py`, and that module also
defines `AccountAdminManagerAccess`. So the document has to name each
contract class, and naming conventions can only find undeclared extras.

## 4. Generating the config from the design document

The document stays the single source for services, layers and edges. The
target repo stays the single source for where they live, as Juval ruled on
2026-10-09 ("the service-to-path map is target-repo knowledge").

1. **Inputs.**
   - The union of `docs/design/*.md` that are `cleared`. Each document lists
     only the services its map touches (`DESIGN-FORMAT.md` line 61), so no
     single document is the whole system.
   - A target-owned layer map (e.g. `[tool.reconciler]` in `pyproject.toml`)
     that maps each service name to a package and contract class. It also
     names the composition root and the non-service shared packages
     (contracts, domain, ports, models, relational base), and carries
     services that predate wayfinder: all of gswa today.
2. **Emit.**
   - One `layers` contract: the layer order with independent siblings, the
     enumerated service packages, and open siblings for Utilities.
   - One `protected` contract per layer: Engines importable only by
     Managers; RA only by Managers and Engines (DB-D20); Managers only by
     Clients and the composition root.
   - `independence` contracts for Engine↔Engine and RA↔RA implementation
     modules.
   - Per service, a `forbidden` contract listing every same-or-lower service
     not in its `Calls` cell. This turns the CI gate from "legal layer pair"
     into "declared edge".
   - One `ignore_imports` line per queued Manager→Manager edge, scoped to the
     callee's message contract module. If that contract lives outside
     `manager/`, `layers` already passes it.
   - `broken_contract_guidance` pointing at the design document.
3. **Write.** Write into a marked, generated `[tool.importlinter]` block, or
   a separate `.importlinter.toml` so hand edits are obvious. Commit it.
4. **Drift guard.** CI runs `reconciler config --check` (regenerate and
   compare), then `lint-imports`. Changing an edge means changing the
   document, then regenerating.
5. **Fixtures.** Per Juval 2026-10-09 (line 92), ship one bad-import fixture
   per forbidden edge kind and assert that `lint-imports` fails on it. gswa's
   `tests/meta/test_canon_adoption.py` is the pattern.

The diff (half 1) reads the same inputs, so "declared" means the same thing in
both halves.

**Its JSON output**, `genshift.reconciliation/v1`, has three sections:
- **modules:** surplus and missing services;
- **edges:** surplus and missing, each with `file:line`;
- **operations:** missing, undeclared, type mismatch, role violation (e.g. an
  RA input that isn't a Spec), and undeclared contract.

Each surplus class names the DESIGN-FORMAT column that would have prevented
it, which is Juval's test. The acceptance session renders it as a
"Reconciliation" table in `acceptance/sandbox-rN-run.md`.

## 5. Owner (recommendation; Rich rules)

| Half | Recommended owner | Reasons | Rejected |
|---|---|---|---|
| Conformance check | **A standalone uv-installable package, the reconciler**, with one Manager, Engines for composition rules and the diff, and Access for the design document, source tree (grimp, griffe) and layer map. The sandbox acceptance session runs it once per map | Keeps DB-D18 intact: design-to-board verifies the plan, never the build. Keeps squadra naive (N39). It is its own volatility (repo layout, language tooling), changing on a different axis from design-to-board (DESIGN-FORMAT, board) | design-to-board would need a new `BuiltRepoAccess` reading code, which breaks "never the build". squadra would parse Services, Layer and `Calls`, which breaks N39. wayfinder writes only the map and the document |
| CI import check | **Target-repo CI** runs `lint-imports` against config the reconciler generates, and the repo owns the layer map. In gswa: a step after `ruff check` in `azure-pipelines.yml` (gswa has no GitHub Actions or pre-commit), or a `tests/meta/` test. squadra runners hit it through the runner skill's `## Gates`, which keeps them naive | DB-D18 assigns build verification to target CI, and Juval (10-09) put enforcement there. Running it per PR suits many small agent PRs: import-linter's cached graph runs in under a second | design-to-board runs once per document, not per PR. A wayfinder-emitted config would push repo paths into the document |

One package for both is the point: one graph, one rule source, Juval's "same
diff". Its home is open: its own repo like squadra, or a package in
claude-skills.

Prerequisites before half 1 has anything to diff:
- The sandbox (`rinman24/squadra-sandbox`) holds only `README.md` and
  `squadra.toml`, and acceptance runs have closed delivery by hand. It needs
  a Python skeleton and one map actually built.
- Target repos need `INP001` and `__init__.py` everywhere.

## 6. Open questions for Rich

1. **Tool.** import-linter, plus grimp and griffe for the diff
   (recommended), or Tach (one file, exact mode, JSON; single maintainer)?
2. **Owner and home.** Is the reconciler a standalone package, and if so in
   its own repo or in claude-skills? Does design-to-board's document reader
   stay private, or become a contract the reconciler reuses?
   → `/ask-juval`: is the reconciler one subsystem with two use cases, and is
   reusing design-to-board's reader a cross-subsystem bypass?
3. **Service → code mapping.** Is it the target-owned layer map
   (recommended; matches Juval 10-09), a new module or class column in
   DESIGN-FORMAT (T2a scope), or AST discovery by class name?
   → `/ask-juval` if a column is preferred, since it reverses his 10-09 line;
   `/ask-eric` for the column or file name.
4. **Classification rulings**, each needed before gswa's first run:
   - Is the composition root (`api/dependencies`, `manager/factory.py`) a
     Client, a Utility or an exempt hosting layer?
   - Are `workers` Clients?
   - Is sharing Row types between RA contracts (`RoleScopeRow` uses
     `RoleRow`) legal, or a missing shared contract?
   - Is `accounts.manager → authn.engines` legal (Engines shared across
     subsystems) or a bypass?

   → `/ask-juval` (structure).
5. **CI strictness.** Should CI enforce the declared `Calls` edges (generated
   per-service `forbidden` contracts plus a drift check; recommended), or
   only legal layer pairs (no dependency on the document)?
6. **Blocking.** Is the diff advisory or blocking in acceptance? Does gswa
   start warn-only, or with `ignore_imports` entries per existing violation,
   until the 7 findings are triaged?
7. **Sequencing.** Which unit gives the sandbox a real Python skeleton and a
   built map: T2c, or before it?
8. **Names.** "Reconcile" is already design-to-board's document-vs-board
   verb (DB-D9, DB-D11), so the diff needs another verb. Names are also
   needed for the tool, the layer map and the finding kinds.
   → `/ask-eric`, folded into his pending decomposition-vocabulary session.
