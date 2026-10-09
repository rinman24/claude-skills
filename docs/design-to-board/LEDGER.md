# design-to-board (T1): ledger

Branch: `feat/design-to-board`
Worktree: `~/Code/claude-skills/.claude/worktrees/design-to-board`
Goal: build `design-to-board` as a plugin in this marketplace. It transcribes
a cleared wayfinder design document into increments on squadra's board; it
never designs (WD14).

This is T1 from the wayfinder port. The port's ledger,
`docs/wayfinder-port/LEDGER.md`, holds every decision this effort starts
from (WD1, WD13, WD14, WD18, WD19, WD21–WD24, WD27, WD-B9, WSQ1). Cite them
by ID; don't copy them here.

## Repo facts

- Marketplace `claude-skills`; plugins install as `<plugin>@claude-skills`.
- Validate before committing a manifest change: `claude plugin validate .`
  and `claude plugin validate plugins/<plugin>`.
- House pattern for a new plugin: `plugins/local-backlog/` plus
  `docs/local-backlog-plugin-install-runbook.md`. Bump `plugin.json`'s
  version in any PR that changes an installed plugin.
- Push: `git -c credential.helper= -c credential.helper='!gh auth git-credential' push`.
- Input contract: `plugins/wayfinder/skills/wayfinder/DESIGN-FORMAT.md`
  (front matter, Services, Increments, Rules; checks 6–13 are this skill's
  validation list). Wayfinder's hand-off: `SKILL.md` Publish step 5.
- Juval's validation list: `~/Code/board-knowledge/sessions/2026-10-07-juval-design-document-contract.md`
  ("What the translator validates").
- squadra (`~/Code/squadra`, Rich's repo): `[board]` config with mandatory
  `claim_scope` (`"parents"` | `"whole-board"`) and `parent_scope_ids`
  (README "Claim scope"; `src/squadra/config.py`). Its `BoardAccess`
  (`src/squadra/board.py`) has no create operation and only an ADO provider;
  the GitHub adapter is deferred (port ledger, Rich's queue). squadra reads
  an item's parent and Predecessor links, its state and its title
  (branch `feat/increment-<id>-<slug>`). `squadra tick --dry-run` shows what
  a tick would claim without writing.
- DB5's GitHub test board (set up 2026-10-09, S1d follow-up):
  `rinman24/squadra-sandbox`, private, default branch `main` (squadra's
  target repo; its `squadra.toml` goes there after SQ5). Parent issues: #1
  "design-to-board test parent (in scope)", the `parent_scope_ids` entry;
  #2 "design-to-board test parent (out of scope)", never in scope. Projects
  v2 project: `rinman24` project 1, "squadra sandbox" (private,
  https://github.com/users/rinman24/projects/1), linked to the repo; its
  Status field is single-select Todo / In Progress / Done, left as created
  until SQ5 says which native states it needs. #1 and #2 are not on the
  project. `gh` has the `project` scope. Never
  `squadra start` there; the acceptance test uses `squadra tick --dry-run`.
- design-to-board's tests (DB2, S2): `uvx pytest -p no:cacheprovider plugins/design-to-board/tests`
  from the repo root. No Python env in the repo: `uvx` runs pytest from its
  own cache, and the code under test is stdlib-only Python 3 (3.14 here).
  `-p no:cacheprovider` keeps `.pytest_cache` out of the tree;
  `__pycache__/` is gitignored. SKILL.md runs the script with `python3 -B`.
- design-to-board exit codes: 0 valid, 1 failed (nothing written), 2 usage
  (argparse). DB4 picks "stopped partway" (not 1 or 2).

This file is the single source of truth for what is done and what is next.
Every session reads it first and updates it last.

## Session budget

Same as the port: under ~100K tokens per session, hard ceiling 120K, ~80K
of planned work per unit, one unit per session. Near the ceiling, stop,
update this ledger and write the next handoff.

## How sessions hand off

Handoffs are prompt files in `handoffs/`. To start the next session, open a
terminal in the worktree, start `claude`, and give it the handoff (paste it,
or send its path and ask it to follow it).

## Session protocol

Start:
1. Read the handoff prompt.
2. Fetch; if `origin/main` moved, merge it into the branch (never rebase a
   pushed branch).
3. Read this ledger and `LESSONS-LEARNED.md` (and the port's lessons the
   handoff names).
4. Mark the unit `in progress` below.

End:
1. Update item statuses and the session log.
2. Update [Rich's queue](#richs-queue) and record his rulings in
   [Decisions](#decisions).
3. Append lessons to `LESSONS-LEARNED.md`.
4. Write the next handoff from `handoffs/TEMPLATE.md`.
5. Commit and push the branch.
6. Tell Rich the handoff path and what's open in his queue.

## Status legend

`todo` · `in progress` · `done` · `blocked` · `dropped`

## Rich's queue

Added at setup (2026-10-09):
- [x] Optional, before S1: `git -C ~/Code/squadra pull` on `main`. Local
      `main` is at `d9d2afa`, behind squadra PR #42 (mandatory claim scope),
      whose code is otherwise only in squadra's `mandatory-claim-scope`
      worktree. S1 reads squadra; it will use whichever is current.

Added S1 (2026-10-09), from DB-D1 (squadra work, Rich's repo; this effort never writes there):
- [x] Fill in `## Choice` in `~/Code/board-knowledge/sessions/2026-10-09-juval-design-to-board-write-path.md`
      and `2026-10-09-eric-design-to-board-vocabulary.md` ((c) as amended; Eric's vocabulary in full).
- [ ] squadra A–D runs in parallel in squadra, with its own ledger
      (`~/Code/squadra` `docs/board-writes/LEDGER.md`, branch
      `feat/board-writes`, items SQ1–SQ5). Start it now: give a fresh
      session in `~/Code/squadra` the handoff
      `docs/design-to-board/handoffs/SQ1-squadra-withdrawn.md` (SQ1: the
      withdrawn state, settled by DB-D1). SQ2 (the verb contract) is unblocked
      (S1b, 2026-10-09): freeze the contract in DB-D4, with DB-D2,
      DB-D3 and DB-D5. design-to-board's F needs
      SQ4; G needs SQ5. That ledger is squadra's source of truth; this one
      records decisions and points to it.

Added S1 (2026-10-09), not design-to-board work:
- [ ] Moved to its own effort (2026-10-09): branch `feat/handoff-skill`, worktree
      `.claude/worktrees/handoff-skill`, ledger `docs/handoff-skill/LEDGER.md`; start
      with `docs/handoff-skill/handoffs/H1-build.md`. Original item:
      Add a `handoff` skill to this marketplace, capturing the essence of
      https://github.com/mattpocock/skills/tree/main/skills/productivity/handoff
      (read at `0f5e033`; no attribution or upstream tracking needed). Essence:
      user-invoked only (`disable-model-invocation: true`), takes an optional
      argument "what will the next session be used for?" and tailors the
      document to it; compacts the current conversation into a handoff a fresh
      agent can continue from; includes a "Suggested skills" section naming
      skills the next agent should invoke; references existing artifacts
      (specs, plans, ADRs, issues, commits, diffs, ledgers) by path or URL
      instead of duplicating them; redacts secrets and PII. Decide one
      difference: upstream saves to `$TMPDIR`, outside the workspace; this
      repo's handoffs are committed prompt files (`handoffs/S<N>-<slug>.md`
      from `TEMPLATE.md`), so either save there when a ledger/template exists
      or keep `$TMPDIR` as the default. Follow the house pattern for a new
      plugin (`plugins/local-backlog/`), validate, install.
      Before building: `/ask-juval` where the handoff file goes. Rich's view
      (2026-10-09): either the temp folder or `handoffs/` is fine, keep the
      `TEMPLATE.md` structure and the ledger, but handoff files probably
      don't belong in version control (noise in the repo). The ledger stays
      committed.

Added S1c (2026-10-09):
- [x] Fill in `## Choice` in `~/Code/board-knowledge/sessions/2026-10-09-juval-failure-and-determinism.md`
      (DB-D6, DB-D7: Juval's version in full) and `2026-10-09-eric-blank-kind-failure-name.md`
      (DB-D8: Eric's version, no cross-map foundations).
- [ ] squadra SQ3 (fake provider), from DB-D7: besides seeding, a test must be
      able to change the fake's state between two `squadra board` CLI calls
      (move an item QUEUED → ACTIVE → DONE; inject a second item with an
      existing Origin). design-to-board's F runs T4–T6 and Juval's seven
      cases through the real CLI against the fake. If SQ3 can't, tell this
      effort: F then needs its own double plus a shared contract suite (~15K).

Added S1d (2026-10-09):
- [ ] Start S2: `handoffs/S2-validate.md` (DB-W, then DB2). S3 follows
      without waiting on squadra; S4 can't start until squadra's SQ3 and
      SQ4 are merged (the squadra item above), so keep that effort moving.
- [ ] Before S5: a GitHub board design-to-board can write to for the
      integration test, plus SQ5 merged. Done (S1d follow-up): the scratch
      repo, parent issues #1 (in scope) and #2 (out of scope), and project 1
      linked to it; see Repo facts. After SQ5 settles how GitHub states and the board
      are configured: the repo's `squadra.toml` (`provider = "github"`,
      `claim_scope = "parents"` with the in-scope parent, `[board.states]`)
      and `squadra init --check` green. Never `squadra start` there.
- [ ] Merge each build unit's PR (DB2–DB5) when you've reviewed it.

Added S2 (2026-10-09):
- [x] Start S2b: `handoffs/S2b-glossary.md`. You type `/ask-juval` and
      `/ask-eric` on "transcribes" (WD14) vs Eric's "reconciles", rule it
      (DB-D9), and S2b writes DB-W's `GLOSSARY-MAP.md` lines. Then merge
      PR #13 and start S3.
- [ ] Review DB2's readings of checks 6–15 (DB2 row) and the PR.

Added S2b (2026-10-09):
- [ ] Merge PR #13 (DB-W + DB2, now ready for review), then start S3:
      `handoffs/S3-plan.md` (DB3). Early in S3, rule Juval's unruled
      recommendation (DB-D9): the reconcile in a third Engine, the
      translation table as literal data with a completeness test.
- [ ] Optional: commit or keep the two uncommitted session files in
      `~/Code/board-knowledge/sessions/` (`2026-10-09-eric-transcribe-vs-reconcile.md`,
      `2026-10-09-juval-transcribe-or-reconcile.md`); `## Choice` is filled
      in from your rulings, so check it reads as you meant.
- [ ] Optional: the map's older line "Wayfinder → squadra fleet" still says
      "`design-to-board` (not yet built)"; a later glossary pass can drop it.

## Work items

| ID | Item | Unit | Est. | Status | Notes |
|---|---|---|---|---|---|
| DB1 | Scope `design-to-board`: settle the open questions below (Rich rules; Juval and Eric where named), then split the build into units of ~80K | S1, S1b, S1c, S1d | ~50–70K | done | Handoff `handoffs/S1-scope.md`. Records decisions; builds nothing. S1 ruled DBQ1 (DB-D1); S1b ruled DBQ2, DBQ3, DBQ4, DBQ7 (DB-D2–DB-D5, one `/ask-juval`); S1c ruled DBQ5, DBQ8, DBQ6 (DB-D6–DB-D8, `/ask-juval` and `/ask-eric` in parallel); S1d split the build into DB2–DB5 |
| DB2 | (E1) Plugin skeleton (`plugins/design-to-board/`: `plugin.json`, marketplace entry, SKILL.md as a Client, `scripts/`), strict reader, document checks 6–15, failure report. On a valid document it says so and exits 0 (no board read yet) | S2 | ~45K | done | Implements DB-D7 (strict reader, runtime, skill as Client; SKILL.md forbids supplying `--parent`, editing the document, re-running with changed arguments), DB-D6 (document checks all collected; report line `check · row · reason · fix`; document-class fix, with the "wayfinder's Publish missed it" note for 6–13; exit "failed, nothing written"), DB-D1 check 14, DB-D8 check 15 (malformed Kind, names the failed part). Tests: the reader rejects anything outside DESIGN-FORMAT's grammar; one failing fixture per check 6–15; several defects in one document all reported; report-line format. Settles and records in Repo facts how pytest runs (this repo has no Python env; stdlib-only code, nothing committed but tests). squadra: nothing. DB-W first, same session. Done S2 (`68307e8`, 50 tests). Readings Rich should check (none reopens a ruling): check 6 gates the body (unknown format or `revising` → only check 6 is reported); check 7 also catches a gap in the ID sequence (a row removed) and a same-map `Depends on` naming a row not in the table; "depends on" in checks 9, 10 and 12 is transitive (a path of edges); check 13 is strict (a dependency's Order is lower); checks 8–14 judge live rows; check 15 checks a withdrawn vertical row's form only, not that its behaviour is still in Destination (a revision may drop a behaviour); the "wayfinder's Publish checks missed this" note goes on 6–13 as DB-D6 says, though wayfinder 0.2.0 now runs 14 and 15 too; the grammar requires every row to carry `Published` within the revision, exactly one integration rule line (check 11 reads its limit, WD23), empty `changed` on revision 1, and Encapsulates on a new service |
| DB3 | (E2) Pure `reconcile(document, snapshot, parent_arg)` (DB-D9), board checks against the snapshot value, `origins` read, dry run | S3 | ~60K | todo | Implements DB-D7 (reconcile signature, named by DB-D9; steps name predecessors by Origin; dry run prints the plan; titles and bodies from row fields and Origin only), DB-D1's translation table (write out every row state × Lifecycle cell), DB-D2 (withdrawn row × ACTIVE → wait/stop, × DONE → delivered), DB-D4 (missing, withdrawn or out-of-scope predecessor Origin; items under more than one parent), DB-D5 (`--parent` rules), DB-D6 (board checks only on a valid document, all collected; `--parent` checks always run; withdrawals in dependency order, predecessors first; queues in Kahn order by `(Order, numeric ID)`; fix routing for sequencing, invocation and board-state classes). DB-D9 (cell "withdrawn row, Origin not on the board" → nothing; carried, not ruled: Juval's third Engine for the reconcile, the translation table as literal data with a completeness test that walks every cell, the Manager passing the snapshot in; settle the Engine's name with domain-modeling, not one named for the mechanism). Tests: T1 golden plan, T2 permutation invariance, T3 byte-identical subprocesses; Juval's cases 1, 3, 4, 5, 6 as plan tests on snapshot values. squadra: the frozen contract only (`verb-contract.md` `origins` JSON, read through a stub `squadra` on PATH). Reads SQ2b's settlement of N6 for the cell "live row, item WITHDRAWN" (expected: board-state failure) |
| DB4 | (F) Executor over `squadra board {origins,queue,withdraw}` | S4 | ~60K | todo | Implements DB-D7 (walks the plan, resolves Origins to item IDs as it goes, never recomputes; body via stdin), DB-D6 (barrier: a refused withdrawal stops before any queue; stop at the first refusal; "stopped partway" report with writes done and remaining, and its exit code; squadra's exit codes 1/2/3 mapped to report classes), DB-D3 (skill ends with what it queued and suggests `squadra tick --dry-run`; never sets `tag_prefix` tags). Tests: T4 executor fidelity, T5 crash convergence for every k, T6 race and phase barrier; Juval's seven cases through the real CLI against SQ3's fake (2 and 7 only possible here). Settles how tests find `squadra` (absent → skip with the reason). Cut line if the session runs long: T6 to a follow-up. squadra: SQ3 (fake, with the state-change requirement in Rich's queue, S1c) and SQ4 (the CLI), both merged |
| DB5 | (G) Integration on a real GitHub board; install | S5 | ~35K | todo | DB-D1's acceptance test on the real board (chain I1→I2→I3, withdraw and replace I2; `squadra tick --dry-run` shows I1 claimable, the replacement chain blocked in order, withdrawn items neither claimable nor done, nothing out of scope), recorded in the session log. Install runbook `docs/design-to-board-plugin-install-runbook.md` on the house pattern; installed as `design-to-board@claude-skills`; DB-G. squadra: SQ5 (GitHub adapter, N8 link ordering). Needs the GitHub board in Rich's queue |
| DB-W | Wayfinder change from DB-D1: DESIGN-FORMAT "Increment identity" gains the invariant "A live row never depends on a withdrawn row" (the withdrawal cascade, restored by Publish) and translator check 14 with the same wording; `GLOSSARY-MAP.md` adds the design-to-board context and its relationships and translations (Eric, DB-D1). DESIGN-FORMAT also gains (DB-D2): a published foundation's `Kind` cell is frozen; withdrawing an increment it names doesn't change it. Also (DB-D8): translator check 15, "Each Kind is blank, `vertical (B<n>)` naming a behaviour in Destination, or `foundation → I<n>, …` naming rows in the table, live or withdrawn" (failure name **malformed Kind**; foundation targets are same-map rows only); the Increments line says a blank Kind is "an increment with neither attribute"; WD14's parenthetical list (stale "missing kind", "> 2 new services") replaced by "fails loudly back to wayfinder on any of DESIGN-FORMAT's translator checks (6–15), reported by name". Bump wayfinder's version | S2, S2b | ~10–15K | done | Committed `0f72433` (DESIGN-FORMAT, Publish step 2 names the cascade, WD14, wayfinder 0.2.0). S2b wrote `GLOSSARY-MAP.md` (design-to-board context, Wayfinder → design-to-board, design-to-board → squadra fleet, the one-person line) and `GLOSSARY-SETTLED.md`'s Transcribe and Reconcile rows (DB-D9), Rich's yes on the exact text. First in S2, before DB2, which implements checks 14 and 15 and reads DESIGN-FORMAT as amended. Its own commit; touches only wayfinder, `GLOSSARY-MAP.md` and the port ledger's WD14 |
| DB-G | When T1 ships: `GLOSSARY-MAP.md:9` "(not yet built) will read" → "reads" (WD27) | S5 (DB5) | ~1K | todo | |

Build order and gates: S2 (DB-W, DB2) and S3 (DB3) need nothing from
squadra. S4 (DB4) waits for squadra's SQ3 and SQ4; S5 (DB5) for SQ5. As of
S1d, squadra's SQ1 and SQ2 are merged, SQ2b (N6–N8) is in progress and SQ3–SQ5
are `todo` (`~/Code/squadra/.claude/worktrees/board-writes/docs/board-writes/LEDGER.md`).
Each build unit is one vertical slice. It ends with commits pushed and a PR
from this branch, which Rich merges.

## Open questions (for DB1)

Found while setting up (research brief, 2026-10-09). Each becomes a decision
in the table below, or `dropped`.

| ID | Question | Notes |
|---|---|---|
| DBQ1 | **Ruled: DB-D1.** Write path: squadra has no create operation, ADO is its only adapter (and dropped by Rich), GitHub is deferred. Does `design-to-board` write to the provider directly, wait for squadra's GitHub adapter, or add create/link operations to squadra first? Which provider first? | Decides everything below. Closed architecture: the board write is ResourceAccess (WD14); where that access lives is the question |
| DBQ2 | **Ruled: DB-D4.** Mostly answered by DB-D1 (the mapping is the item's Origin, read with `increments_by_origin`); confirm, and settle the cross-map lookup (Eric: `increments_by_origin(parent)` is scoped by parent, a `<map>:<ID>` predecessor may sit under another parent). Where does the increment ID → board item mapping live? `Published` holds only `r<N>`, and the translator never patches the document (WD14) | Needed for idempotent re-runs, withdrawals and `<map>:<ID>` cross-map dependencies. Candidates: on the item (title, label, body marker), or a file the translator owns |
| DBQ3 | **Ruled: DB-D2.** Half answered by DB-D1 (`withdraw_increment` → `Lifecycle.WITHDRAWN`). Open: Juval's blocking Q2 (is a revision published while squadra still runs an earlier revision's increments? if not, squadra refuses ACTIVE → WITHDRAWN, else C needs a cancel path) and Eric's blocking Q2 (can a revision withdraw a row whose increment is DONE, directly or through a foundation's `Kind` cell?). What does "withdraw" do on the board (close, state, label)? And must it refuse to withdraw an item squadra has already claimed? | WD22: the translator only creates and withdraws |
| DBQ4 | **Ruled: DB-D5.** Mostly answered by DB-D1 (squadra's CLI checks claim scope and refuses an out-of-scope parent). Open: which parent design-to-board passes, and how it finds the target squadra config. How is claim scope honoured? Presumably `"parents"` → create each item under a `parent_scope_ids` parent (which one?), `"whole-board"` → anywhere. Where does it find the target `squadra.toml`? | `[[boards]]` (WSQ1) will change the config shape later |
| DBQ5 | **Ruled: DB-D6.** What does "fails loudly back to wayfinder" mean concretely: a report to the user naming the failed check and row, writing nothing? | WD14, WD18. S1b starting position (not ruled; `/ask-juval` in S1c): all-or-nothing. Every check (DESIGN-FORMAT 6–14, plus the board checks from DB-D2, DB-D4, DB-D5) runs before any write; all failures collected; on any failure nothing is written, exit non-zero, one line per failure (check, row, reason, fix = "Revise the map in wayfinder"); writes go withdrawals first, then queues in dependency order; a crash mid-run recovers by re-running (A3) |
| DBQ6 | **Ruled: DB-D8.** WD14 fails on "missing kind", but DESIGN-FORMAT and WD10 allow a blank Kind. Which holds? | Probably reword WD14 ("unknown kind"). S1b starting position (not ruled; `/ask-eric` in S1c): DESIGN-FORMAT holds, a blank Kind is a plain increment, only a non-blank Kind outside `vertical (B<n>)` / `foundation → I<n>, …` fails; WD14 reworded to "unknown kind" in DB-W along with its stale "> 2 new services" |
| DBQ7 | **Ruled: DB-D3.** Eric's blocking Q1: if new items land held rather than QUEUED, the verb is renamed after the held state and "queue" goes to whatever releases it. Is publishing live? New queued in-scope items are claimable at the next tick. Should the skill end by suggesting `squadra tick --dry-run`, or create items in a non-queued state? | Must never set `tag_prefix` tags (WSQ1) |
| DBQ8 | **Ruled: DB-D7.** Determinism (WD13): two AFK runs on one document give identical increments. How is that tested (fake board, golden output)? | Shapes the build's test unit. S1b starting position (not ruled; `/ask-juval` in S1c): the translation is a deterministic script the skill calls (the model only invokes it and relays the report). Test: two runs from one document against the same starting state of squadra's fake board, assert identical squadra calls and an identical final board; a golden file for the dry-run plan; Juval's 7 cases (DB-D4); ties broken by `Order`, then ID; titles and bodies from row fields only, no timestamps |

Housekeeping noticed (fix when convenient, not blocking): WD14 still says
"> 2 new services" (WD23 replaced it with ≤ 2 changed; now fixed by DB-W, DB-D8); Juval's ninth item
("writes only rows published or withdrawn in the current revision") is
translator behaviour, not a DESIGN-FORMAT check; squadra's
`docs/design/board-provider-seam.md:146` still calls the parent scope optional.

## Decisions

| ID | Decision | Status | Detail |
|---|---|---|---|
| DB-D1 | Board writes live in squadra (DBQ1 option (c) with Juval's amendments), in Eric's vocabulary. GitHub first | ruled 2026-10-09 (Rich, S1) | Juval (`~/Code/board-knowledge/sessions/2026-10-09-juval-design-to-board-write-path.md`): one Resource gets one ResourceAccess, so the provider representation is encapsulated once, in squadra's `BoardAccess`; option (b) dropped (it is (c) late). Amendments: A1 atomic business verbs, no separate link step (a tick between create and link would claim an unlinked item); A2 squadra CLI subcommands are Clients, and squadra's orchestration applies the claim-scope check and the withdraw-while-active rule; design-to-board's Resource is squadra's CLI, not GitHub (keeps WD14's ResourceAccess honest); A3 a fake provider registered in `PROVIDERS`. Rich: nobody works increments by hand before squadra's GitHub adapter (Juval's blocking Q1), so (c) and this order stand: A contract → B fake + contract tests → C CLI + rules (squadra) → E reader/validation/dry run → F reconcile + ordered queueing against the fake (design-to-board) → D GitHub adapter (squadra) → G integration on a real GitHub board, acceptance test: chain I1→I2→I3, withdraw and replace I2, `squadra tick --dry-run` shows I1 claimable, replacement chain blocked in order, withdrawn items neither claimable nor done, nothing out-of-scope. Put float before G. Eric (`.../2026-10-09-eric-design-to-board-vocabulary.md`), accepted in full: squadra verbs `queue_increment(origin, parent, predecessors, title, body) -> item_id`, `withdraw_increment(item_id)` (refused at DONE), `increments_by_origin(parent) -> {origin: (item_id, Lifecycle)}`; rejected `publish_*` (false cognate of wayfinder's Publish/`Published`), "key", "re-issued", "link". **Origin**: opaque string squadra stores and never parses; design-to-board writes `<map>:<ID>` (map front-matter value, never the revision). `Lifecycle.WITHDRAWN`: fourth, terminal bucket, recorded as a model change; unmapped native states fail `validate_config` instead of defaulting to QUEUED; tick reports a second blocked reason (predecessor withdrawn). The withdrawal cascade is wayfinder's rule ("a live row never depends on a withdrawn row"; DB-W), design-to-board only checks it (check 14) and transcribes. Context map: design-to-board is a context whose content is the translation table (row state × item Lifecycle → action); Wayfinder → design-to-board Published Language; design-to-board → squadra fleet downstream Conformist; translations `Depends on` → predecessors, row ID → Origin, withdrawn row → `withdraw_increment`, live row without its Origin on the board → `queue_increment`, `Published: rN` → nothing |
| DB-D2 | Withdrawal (DBQ3). squadra allows QUEUED → WITHDRAWN only and refuses ACTIVE and DONE; there is no cancel path in C. A published foundation's `Kind` cell is frozen (WD22 as written), so withdrawing its target never cascades up to the foundation, and WD22 is not reopened. WITHDRAWN's native state is set in squadra's state mapping (GitHub default: closed, reason "not planned"; no label). design-to-board sees only `Lifecycle.WITHDRAWN` | ruled 2026-10-09 (Rich, S1b) | Answers Juval's and Eric's blocking Q2s. design-to-board checks the board before any write, so a refused withdrawal leaves nothing half done. ACTIVE: recover by letting the run finish (or stopping it by hand), then re-run design-to-board, which is idempotent. DONE: fail loudly ("I2 is delivered; change delivered work with a new increment, not a withdrawal"). The translation table keeps two outcomes; a third ("withdrawn row, delivered item: leave alone and report") waits until a real document needs it. DB-W adds the frozen-`Kind` sentence to DESIGN-FORMAT |
| DB-D3 | New increments land QUEUED; the verb stays `queue_increment` (DBQ7) | ruled 2026-10-09 (Rich, S1b) | Answers Eric's blocking Q1. The ticker runs on its own (`squadra start`, `FLEET_TICK_INTERVAL_SECONDS`), so a run is live within one tick. The gate is wayfinder's `cleared` plus the act of running design-to-board; design-to-board's dry run (E) is the preview; `squadra stop` pauses the fleet. No held state, no fifth Lifecycle bucket. The skill ends by reporting what it queued and suggesting `squadra tick --dry-run`. It never sets `tag_prefix` tags (WSQ1) |
| DB-D4 | Mapping and lookup (DBQ2): the item's Origin is the only increment → item mapping (no file). `increments_by_origin()` drops its `parent` argument and returns every Origin on the configured board, in every Lifecycle, as `{origin: Increment}`, with `Increment` a named record `(item_id, parent, lifecycle, in_claim_scope)`; claim scope is reported, not filtered (A1). squadra raises on a duplicate Origin, naming both items (A2). `queue_increment` returns the existing item only when every argument matches, and refuses any difference (A3) | ruled 2026-10-09 (Rich, S1b) | Juval, `~/Code/board-knowledge/sessions/2026-10-09-juval-parent-and-lookup-scope.md`. Contract SQ2 freezes: `queue_increment(origin, parent, predecessors, title, body) -> item_id` (refuses an out-of-scope parent; A3; lands QUEUED, not claimable until links exist); `withdraw_increment(item_id)` (DB-D2); `increments_by_origin() -> {origin: Increment}` (A1, A2). Per board: a predecessor on another board (WSQ1 `[[boards]]`) resolves as missing. design-to-board fails loudly on a missing, withdrawn or out-of-scope predecessor Origin and on a map whose items sit under more than one parent. Juval's 7 discriminating tests (session file, "The test that discriminates") are SQ2 contract tests and F tests; case 5 (parent drops out of scope → report, write nothing) is the one that proves A1 |
| DB-D5 | Parent and config (DBQ4). `--parent` is required on a map's first run (no Origin with its `<map>:` prefix on the board, in any Lifecycle) and refused if missing. Later runs use the parent the map's items carry; more than one parent → fail loudly; a conflicting `--parent` is refused, a matching one accepted. The parent is required under `"whole-board"` too. The parent never goes in the design document. design-to-board never reads `squadra.toml`: it runs squadra's CLI in the target repo and squadra resolves its own config | ruled 2026-10-09 (Rich, S1b) | Juval, same session: (c) and DB-D4's board-wide query decide each other (per-parent lookup would force a map → parent file). Filtering Origins by map prefix is design-to-board's job; squadra never parses Origin. Re-parenting is a board act, not a design-to-board flag. Conformist downstream (DB-D1), so `[[boards]]` costs design-to-board nothing |
| DB-D6 | Failure and write semantics (DBQ5). Validation is all-or-nothing: document checks (DESIGN-FORMAT 6–15) run first and are all collected; board checks run only on a valid document and are all collected; `--parent` checks always run; any failure → nothing written. Writes promise "every prefix of the write sequence is a valid board state", not all-or-nothing (no rollback): withdraw in dependency order, predecessors first; barrier: a refused withdrawal stops the run before any queue; queue in Kahn order with priority `(Order, numeric ID)`, stop at the first refusal; a re-run completes the suffix (A3). Report: one line per failure, `check · row · reason · fix`, fix routed by class (document defect → revise the map in wayfinder, and for 6–13 note that wayfinder's Publish checks missed it; sequencing → transcribe the other map first; invocation → re-run with the right `--parent`; board state → wait/stop the run, squadra config, or repair the board by hand in squadra; stopped partway → writes done and remaining, re-run). Two non-zero exit codes: "failed, nothing written" and "stopped partway". No lock; never wraps a run in `squadra stop` | ruled 2026-10-09 (Rich, S1c) | Juval, `~/Code/board-knowledge/sessions/2026-10-09-juval-failure-and-determinism.md`. Correctness rests on squadra's write-time refusals (DB-D1 A2), prefix-safe ordering and A3; the pre-check gives the clean report. The race table (tick claims a target, ACTIVE → DONE, scope edited, concurrent run, cross-map withdrawal) is in the session file. squadra's own CLI exit codes (`verb-contract.md`: 0, 1, 2, 3) sit underneath |
| DB-D7 | Determinism seam and tests (DBQ8). Strict reader (DESIGN-FORMAT grammar exactly; anything else is a document defect) → pure `reconcile(document, snapshot, parent_arg) -> Plan \| [Failure]` (named `plan` until DB-D9) (snapshot = `increments_by_origin()` as a value; steps name predecessors by Origin, never item ID) → executor (walks the plan through `squadra board {origins,queue,withdraw}`, resolves Origins to item IDs as it goes, never recomputes; dry run prints the same plan). Skill is a Client: passes Rich's arguments verbatim, relays the report; SKILL.md forbids supplying `--parent`, editing the document, or re-running with changed arguments after a failure. Titles and bodies from row fields and Origin only. Runtime: Python 3, stdlib only, `plugins/design-to-board/scripts/`, invoked via `${CLAUDE_PLUGIN_ROOT}`; pytest in the plugin. Tests: T1 golden plan, T2 permutation invariance (snapshot and row order), T3 two subprocesses with different `PYTHONHASHSEED`/`TZ`/locale/cwd → byte-identical (T1–T3 need no board); T4 executor fidelity, T5 crash convergence for every k, T6 race and phase barrier (through the real CLI against SQ3's fake). Juval's seven cases are board-check correctness tests in F (squadra covers 2, 4–7 in its contract suite, N9) | ruled 2026-10-09 (Rich, S1c) | Juval, same session file. His blocking question (does the fake keep state across CLI processes, can a test change it between calls?) answered from squadra's SQ3 handoff: state outlives the process by design; the "change between calls" part is a new SQ3 requirement in Rich's queue. Runtime is Claude's addition (no plugin here ships code yet) |
| DB-D8 | Blank Kind (DBQ6). DESIGN-FORMAT holds: a blank Kind is "an increment with neither attribute" (squadra's wording; not "plain increment"). Translator check 15: "Each Kind is blank, `vertical (B<n>)` naming a behaviour in Destination, or `foundation → I<n>, …` naming rows in the table, live or withdrawn"; failure name **malformed Kind**, the line quotes the cell and names the failed part (form, unknown behaviour, unknown row). No cross-map foundations: `foundation → B:I3` is malformed Kind; cross-map enabling is a `Depends on: <map>:<ID>` edge. WD14 points to DESIGN-FORMAT's checks (6–15) by number instead of listing them. All wording changes go through DB-W | ruled 2026-10-09 (Rich, S1c) | Eric, `~/Code/board-knowledge/sessions/2026-10-09-eric-blank-kind-failure-name.md`. Blank is an absence squadra declined to name ("infrastructure increment" is _Avoid_); "plain" already means a glossary-less word in check 4; "unknown" blames the translator, "malformed" the document; capital-K ties the message to the column. "Live or withdrawn" follows from DB-D2's frozen `Kind` cell. Nothing in squadra's `src/` reads Kind |
| DB-D9 | Two verbs at two levels. **Transcribe** names design-to-board's whole act, a cleared design document to squadra's board; it never designs (WD14's description verb, unchanged in WD14, plugin.json, the marketplace entry and SKILL.md). **Reconcile** names only its comparison step: the document against `increments_by_origin()` through the translation table, yielding the Plan. DB-D7 amended: `plan(...)` is `reconcile(document, snapshot, parent_arg) -> Plan \| [Failure]`. WD14's "ResourceAccess" stands (role facing outward; inside, the reconcile is Engine work whose every cell is a rule owned by wayfinder, squadra or write safety). Translation table cell: withdrawn row whose Origin was never on the board → nothing (no write, no report line). Both terms settled in `GLOSSARY-SETTLED.md`, context design-to-board (Transcribe rejects Publish, Sync; Reconcile rejects Diff); `GLOSSARY-MAP.md` context line says "transcribes" | ruled 2026-10-09 (Rich, S2b) | Eric, `~/Code/board-knowledge/sessions/2026-10-09-eric-transcribe-vs-reconcile.md`: "reconciles" in his S2 context line was drift; one verb for both levels makes "the reconcile failed" ambiguous, and "reconcile" at the context level hides the direction of authority (only the board moves). Juval, `.../2026-10-09-juval-transcribe-or-reconcile.md`, chosen against on the name: one verb, the step stays "the plan", because "reconcile" implies two ledgers and an arbiter. Kept from Juval: WD14 unchanged; the test (one acceptable write set; every cell traces to an owner's rule; a cell needing any other rule reopens WD14); his table-as-data and third-Engine recommendation goes to DB3 unruled; the deferred DB-D2 third outcome stays a cell, never a flag. Eric's watch item: `Plan` is rejected in Wayfinder as a synonym for Design document; settle Plan in design-to-board if the document gets called "the plan" again |

## Session log

| Session | Date | Unit | Outcome | Handoff written |
|---|---|---|---|---|
| S0 | 2026-10-09 | Setup | Branch `feat/design-to-board` from `main` `205c5f2`; this ledger, lessons, template and S1 handoff; open questions DBQ1–DBQ8 from a read of the port ledger, DESIGN-FORMAT, wayfinder's Publish step and squadra | `handoffs/S1-scope.md` |
| S1 | 2026-10-09 | DB1 (part) | DBQ1 ruled as DB-D1 after `/ask-juval` and `/ask-eric`; DB-W added; squadra A–D in Rich's queue; DBQ2–DBQ4, DBQ7 annotated. Stopped at ~115K before DBQ2 | `handoffs/S1b-scope.md` |
| S1b | 2026-10-09 | DB1 (part) | DBQ3, DBQ7, DBQ2, DBQ4 ruled as DB-D2–DB-D5 (one `/ask-juval`, on the parent and the lookup scope); SQ2 unblocked (pushed `68eb3a7`); DBQ5, DBQ6, DBQ8 annotated with starting positions; stopped before two more consultations to stay under the ceiling | `handoffs/S1c-scope.md` |
| S1c | 2026-10-09 | DB1 (part) | Merged `origin/main` (`b11a7aa`); `/ask-juval` (DBQ5, DBQ8) and `/ask-eric` (DBQ6) run in parallel; ruled DB-D6–DB-D8; DB-W grows check 15 and the WD14 rewording; SQ3 requirement in Rich's queue. Stopped at ~110K before the build split | `handoffs/S1d-split.md` |
| S1d | 2026-10-09 | DB1 (done) | Merged `origin/main` (`078e4a5`, handoff-skill PR #12); read squadra's board-writes ledger (SQ2 merged, SQ2b in progress) and `verb-contract.md`; split the build into DB2 (E1), DB3 (E2), DB4 (F), DB5 (G); T1 moved from E1 to E2 (it asserts the plan); DB-W placed in S2 before DB2, DB-G in DB5. No rulings needed | `handoffs/S2-validate.md` |
| S2 | 2026-10-09 | DB-W (part), DB2 (done) | `origin/main` unchanged. DB-W: DESIGN-FORMAT, Publish step 2, WD14, wayfinder 0.2.0 (`0f72433`); `GLOSSARY-MAP.md` drafted, Eric (board-eric, via domain-modeling) approved with sharper wording on three lines and asked for a fourth, so it waits on Rich. DB2: plugin `design-to-board` 0.1.0, strict reader, checks 6–15, report, SKILL.md as a Client, marketplace entry; 50 tests green; all three `claude plugin validate` pass (`68307e8`); draft PR #13 | `handoffs/S3-plan.md` |
| S2b | 2026-10-09 | DB-W (done) | `origin/main` unchanged. `/ask-juval` and `/ask-eric` blind in parallel on "transcribes" vs "reconciles": both keep "transcribes" and WD14's ResourceAccess; Eric two verbs (reconcile = the step), Juval one (step stays "the plan"). Rich ruled DB-D9 (Eric's two verbs; withdrawn row never on the board → nothing); session files written from the transcripts. `GLOSSARY-MAP.md` lines and two `GLOSSARY-SETTLED.md` rows on Rich's yes, DB-D7 amended (`5a6aa02`). PR #13 ready for review | `handoffs/S3-plan.md` |
