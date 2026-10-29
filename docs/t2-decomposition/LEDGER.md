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
  - The layer map is target-owned.
  - gswa-backend is an example only.
  - import-linter is the CI tool.
  - The conformance check is built on grimp and griffe.
  - The tool has its own public repo with semver tags.
  - Output starts as plain text.
- Names: `~/Code/board-knowledge/sessions/2026-10-28-eric-decomposition-vocabulary.md`,
  Choice: proving path, conformance check, surplus, shortfall. Everything
  else in that session is unruled until T2-E.
- [T2-D1](#decisions): protecting the rule sources.

## Repo facts

- **Target repo:** `rinman24/squadra-sandbox`.
  - Private, default branch `main`, cloned at `~/Code/squadra-sandbox`.
  - T2c-1 (2026-10-28) added the closed-layer skeleton in sandbox PR #17
    (`feat/skeleton`): package `sandbox`, `layer-map.toml`,
    `docs/design/skeleton.md` (provisional), `importlinter.composition.toml`,
    `importlinter.edges.toml`, `tests/test_bad_import_fixtures.py`,
    `.github/CODEOWNERS` and `.github/workflows/import-direction.yml`.
  - Rulesets on `main`, no bypass actors:
    - `26103469` "import-direction required", active: required status check
      `import-direction` from GitHub Actions (integration 15368).
    - `26103470` "rule sources: code-owner review", **disabled**: a
      `pull_request` rule with code-owner review and 0 approvals. Enable it
      before the first squadra run in the sandbox (T2-D2).
  - Since ruleset A, a commit reaches `main` only through a PR whose
    `import-direction` check passed. That includes the `[fleet] name`
    bookkeeping.
  - The plan allows rulesets on this private repo. Branch protection GET
    returned 404 "Branch not protected", not the 403 upgrade message, and a
    ruleset created as `disabled` was accepted.
  - The `import-edges (advisory)` job runs the allow-list and isn't required
    (DB-D23).
  - Board history is in `docs/design-to-board/LEDGER.md`, Repo facts.
- **gswa-backend:** an example only. Read it if useful; never edit it or run
  anything against it.
- **The tool:** the conformance check plus the config generator. Its repo
  doesn't exist yet; the name waits on Eric (T2-E). Until then, write it as
  `<tool>`.
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

- [ ] Run T2-E, the `/ask-eric` follow-up (`/Users/richinman/Code/claude-skills/.claude/worktrees/t2-s0/docs/t2-decomposition/handoffs/T2-E-eric-followup.md`).
  It is on the critical path: T2a and the tool's name wait on it.
- [ ] Review and merge sandbox PR #17 (https://github.com/rinman24/squadra-sandbox/pull/17),
  the T2c-1 skeleton. Until ruleset B is on, your review is the only guard
  on rule sources.
- [ ] Before the first squadra run in the sandbox (T2-D2):
  1. Create the agent authoring identity as a machine user. Name it for its
     role. Keep "genshift" out of its login, display name and commit email.
     Check GitHub's terms on machine accounts first.
  2. Add it to the sandbox as a write collaborator, never as a bypass actor.
  3. Give squadra and Claude sessions its token through `GH_TOKEN`.
  4. Enable ruleset `26103470`.
  5. Run Juval's test. A layer-map change opened by the identity is
     unmergeable until you approve, then mergeable. The same change opened as
     `rinman24` is unmergeable. If the second merges, find the bypass first.
- [ ] Before sandbox r5, the bookkeeping carried from design-to-board S16:
  1. Add `[fleet] name` to `~/Code/squadra-sandbox/squadra.toml`, and merge
     it to the sandbox's `main` through a PR (ruleset A blocks direct pushes).
  2. Reinstall squadra at `main`.
  3. Run `squadra init --check --provider github` there.

## Work items

| ID | Item | Depends on | Est. | Status | Notes |
|---|---|---|---|---|---|
| S0 | Set up T2: this ledger, lessons, template, handoffs for T2-E and T2c-1; rule question 6 (T2-D1) | — | ~35K | done | |
| T2-E | `/ask-eric` follow-up, then settle terms with the domain-modeling skill | — | ~60K | todo | Handoff written. Covers T2c-R2 questions 7–8, DB-D22's format consequences and the vocabulary session's unruled items |
| T2a | Wayfinder: DESIGN-FORMAT and the Publish step. Covers the `Calls` column (telling "calls nothing" from "not declared", DB-D22), contract operations and type pairs, DB-D20 and DB-D21 Rules lines, and the gaps Eric's session lists | T2-E | ~80K | todo | Splits if the gaps add more than ~20K |
| T2b | design-to-board: composition-rule checks; `Depends on` derived from call edges; every callee in `Calls` needs a Services row with a Layer (DB-D22); operation-count warnings; pulse and milestone ordering | T2a | ~80K | todo | |
| T2c-1 | Sandbox skeleton (DB-D23) and T2-D1 | — | ~70K | done | Sandbox PR #17, open, CI green, waiting on Rich's merge. Hand-written import-linter configs until T2c-2's generator replaces them. Two configs: composition rules in the required `import-direction` job; the allow-list in a separate, non-required `import-edges (advisory)` job, not `continue-on-error`, because a job that stays green hides the findings DB-D23's calibration counts. The fixtures are a test in the required job, not fixture branches: branches rot as `main` moves and nobody runs them, while the test runs on every PR and fails if a config is weakened. Seven of the nine fixtures cover edge kinds (call up; Client→non-Manager; Manager→Manager; Engine→Engine; RA→RA; undeclared edge; implementation import), and two have unlisted importers (a package and a module). "No queued calls into Engines or ResourceAccess" isn't import-visible. Ruleset B is disabled until T2-D2's identity exists |
| T2c-2 | Create `<tool>`'s repo. Build the config generator: a per-service allow-list from each service's latest `Calls`, plus a rules-only tier (DB-D22). Build the drift check and its separate CI job, and replace T2c-1's hand-written config | T2-E (name), T2a (format), T2c-1 | ~80K | todo | Includes the composite Action and the Azure step from T2C-STATE-OF-THE-ART §3 |
| T2c-3 | Conformance check in `<tool>`, proved on seeded fixtures: a known surplus edge, a shortfall, an undeclared operation and a missing module against a hand-written document; it must report exactly those (DB-D23) | T2c-2 | ~80K | todo | JSON is the record and Markdown is rendered from it, with three outcomes per surface |
| T2-r5 | Sandbox r5: the first map squadra builds, delivered through merges, then checked. Advisory until a run has zero check defects (DB-D23) | T2a, T2b, T2c-3, squadra delivering through merges, `[fleet] name`, T2-D2 (authoring identity, ruleset B enabled) | ~80K | todo | If squadra can't yet deliver through merges, that gap goes on squadra's ledger and T2c still closes on its fixtures |

## Open items

- **T2-D1 and identity.** Resolved by T2-D2. The authoring identity and
  enabling ruleset B are in Rich's queue, ahead of the first squadra run in
  the sandbox.
- **For T2-E (Eric).**
  - T2c-R2 question 7, about "reads code only", has two framings: Juval's
    difference of cadence and findings (DB-D22), and the two-job split
    (T2C-STATE-OF-THE-ART §1).
  - Question 8: a term for "conforms", and the names of the tool and the
    layer map.

## Decisions

| ID | Decision | Status | Source |
|---|---|---|---|
| T2-D1 | The rule sources in each target repo are protected. These are the layer map, `docs/design/` and the generated import-linter config, plus any exemptions file. Rich is their CODEOWNER. A ruleset on `main` requires the import-direction check as a status check and code-owner review for those paths. No bypass actors: no Copilot coding agent and no agent identity. Large organisations route boundary changes to a human owner (T2C-STATE-OF-THE-ART §1). Amended by T2-D2: an agent authoring identity exists with write access only and is never a bypass actor; `CODEOWNERS`, the check's workflow and the fixture test are also code-owned | ruled 2026-10-28 (Rich, T2 S0); amended 2026-10-28 (Rich, T2c-1) | T2c-R2 question 6, as recommended. DB-D23's "advisory until calibrated" governs whether the edge gate blocks; T2-D1 governs who may change the rules |

| T2-D2 | One agent authoring identity, a machine user, authors every agent PR, from squadra and Claude sessions alike. It has write access only, is not a code owner and is never a bypass actor. `rinman24` stays the only code owner and approves. Consequence, accepted knowingly: no rule-source change authored as `rinman24` can land. squadra needs no code change because its token comes from `GH_TOKEN`; an App can replace the machine user later by minting the token outside squadra. Which to use follows who owns the board: a machine user (classic PAT with `repo` and `project`) when the board is a personal Projects v2 board, as the sandbox's is, because a GitHub App's installation token very likely can't reach a user-owned project; a GitHub App when the boards live in an organization (organization projects permission, per-repo installation, 1-hour tokens refreshed outside squadra). Rich chose the machine user for the sandbox (2026-10-29). Which agent opened a PR is PR metadata (a branch prefix or a label), not a second account. "genshift" stays out of squadra's repos: the identity is named for its role. Meanwhile ruleset B (code-owner review) is built but disabled; it is enabled before the first squadra run in the sandbox, not before T2c-1 merges | ruled 2026-10-28 (Rich, T2c-1) | Juval (`~/Code/board-knowledge/sessions/2026-10-28-juval-pr-authoring-identity.md`), option 1 plus option 3 for the interim. His blocking questions: squadra only opens PRs and never merges them (runner template; no `pr merge` in `src/squadra`); GitHub's terms on a machine account are to be checked when it's created. Juval also added `CODEOWNERS` and the workflow to the protected paths; T2c-1 added the fixture test on the same test (it is part of the required check) |

## Session log

Sessions before S0 (T2c-R, T2c-R2, T2c-J) are logged in
`docs/wayfinder-port/LEDGER.md`.

| Session | Date | Unit | Outcome | Handoff written |
|---|---|---|---|---|
| S0 | 2026-10-28 | S0 · set up T2 (branch `docs/t2-s0`) | Created this ledger, `LESSONS-LEARNED.md`, `HANDOFF-TEMPLATE.md`, and handoffs for T2-E and T2c-1 (local under HD1, in the `t2-s0` worktree). Units T2a–T2-r5 sized from DB-D18–DB-D23 and the T2c rulings. Rich ruled question 6 (T2-D1). The port ledger's T2 row now points here | `/Users/richinman/Code/claude-skills/.claude/worktrees/t2-s0/docs/t2-decomposition/handoffs/T2-E-eric-followup.md`, `/Users/richinman/Code/claude-skills/.claude/worktrees/t2-s0/docs/t2-decomposition/handoffs/T2c-1-sandbox-skeleton.md` |
| T2c-1 | 2026-10-28 | T2c-1 · sandbox skeleton (branch `docs/t2c-1-skeleton`; sandbox `feat/skeleton`) | Plan check passed. Identity conflicted: squadra and Claude sessions both open PRs as `rinman24`. Ran `/ask-juval` and Rich chose Juval's plan (T2-D2). Built the skeleton: sandbox PR #17, https://github.com/rinman24/squadra-sandbox/pull/17, open, CI green on both jobs, merge state CLEAN, waiting on Rich. Rulesets `26103469` (active) and `26103470` (disabled). Amended T2-D1 | None. T2c-2 waits on T2-E (the name) and T2a (the format); write its handoff once both are done |
