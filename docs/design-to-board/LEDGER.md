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

## Work items

| ID | Item | Unit | Est. | Status | Notes |
|---|---|---|---|---|---|
| DB1 | Scope `design-to-board`: settle the open questions below (Rich rules; Juval and Eric where named), then split the build into units of ~80K | S1, S1b | ~50–70K | in progress | Handoff `handoffs/S1-scope.md`. Records decisions; builds nothing. S1 ruled DBQ1 (DB-D1); S1b (`handoffs/S1b-scope.md`) rules DBQ2–DBQ8 and splits the build |
| DB2+ | Build units | — | — | todo | Defined by DB1 |
| DB-W | Wayfinder change from DB-D1: DESIGN-FORMAT "Increment identity" gains the invariant "A live row never depends on a withdrawn row" (the withdrawal cascade, restored by Publish) and translator check 14 with the same wording; `GLOSSARY-MAP.md` adds the design-to-board context and its relationships and translations (Eric, DB-D1). Bump wayfinder's version | set by DB1 | ~10K | todo | Before the design-to-board validation unit, which implements check 14 |
| DB-G | When T1 ships: `GLOSSARY-MAP.md:9` "(not yet built) will read" → "reads" (WD27) | last build unit | ~1K | todo | |

## Open questions (for DB1)

Found while setting up (research brief, 2026-10-09). Each becomes a decision
in the table below, or `dropped`.

| ID | Question | Notes |
|---|---|---|
| DBQ1 | **Ruled: DB-D1.** Write path: squadra has no create operation, ADO is its only adapter (and dropped by Rich), GitHub is deferred. Does `design-to-board` write to the provider directly, wait for squadra's GitHub adapter, or add create/link operations to squadra first? Which provider first? | Decides everything below. Closed architecture: the board write is ResourceAccess (WD14); where that access lives is the question |
| DBQ2 | **Ruled: DB-D4.** Mostly answered by DB-D1 (the mapping is the item's Origin, read with `increments_by_origin`); confirm, and settle the cross-map lookup (Eric: `increments_by_origin(parent)` is scoped by parent, a `<map>:<ID>` predecessor may sit under another parent). Where does the increment ID → board item mapping live? `Published` holds only `r<N>`, and the translator never patches the document (WD14) | Needed for idempotent re-runs, withdrawals and `<map>:<ID>` cross-map dependencies. Candidates: on the item (title, label, body marker), or a file the translator owns |
| DBQ3 | **Ruled: DB-D2.** Half answered by DB-D1 (`withdraw_increment` → `Lifecycle.WITHDRAWN`). Open: Juval's blocking Q2 (is a revision published while squadra still runs an earlier revision's increments? if not, squadra refuses ACTIVE → WITHDRAWN, else C needs a cancel path) and Eric's blocking Q2 (can a revision withdraw a row whose increment is DONE, directly or through a foundation's `Kind` cell?). What does "withdraw" do on the board (close, state, label)? And must it refuse to withdraw an item squadra has already claimed? | WD22: the translator only creates and withdraws |
| DBQ4 | **Ruled: DB-D5.** Mostly answered by DB-D1 (squadra's CLI checks claim scope and refuses an out-of-scope parent). Open: which parent design-to-board passes, and how it finds the target squadra config. How is claim scope honoured? Presumably `"parents"` → create each item under a `parent_scope_ids` parent (which one?), `"whole-board"` → anywhere. Where does it find the target `squadra.toml`? | `[[boards]]` (WSQ1) will change the config shape later |
| DBQ5 | What does "fails loudly back to wayfinder" mean concretely: a report to the user naming the failed check and row, writing nothing? | WD14, WD18 |
| DBQ6 | WD14 fails on "missing kind", but DESIGN-FORMAT and WD10 allow a blank Kind. Which holds? | Probably reword WD14 ("unknown kind") |
| DBQ7 | **Ruled: DB-D3.** Eric's blocking Q1: if new items land held rather than QUEUED, the verb is renamed after the held state and "queue" goes to whatever releases it. Is publishing live? New queued in-scope items are claimable at the next tick. Should the skill end by suggesting `squadra tick --dry-run`, or create items in a non-queued state? | Must never set `tag_prefix` tags (WSQ1) |
| DBQ8 | Determinism (WD13): two AFK runs on one document give identical increments. How is that tested (fake board, golden output)? | Shapes the build's test unit |

Housekeeping noticed (fix when convenient, not blocking): WD14 still says
"> 2 new services" (WD23 replaced it with ≤ 2 changed); Juval's ninth item
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

## Session log

| Session | Date | Unit | Outcome | Handoff written |
|---|---|---|---|---|
| S0 | 2026-10-09 | Setup | Branch `feat/design-to-board` from `main` `205c5f2`; this ledger, lessons, template and S1 handoff; open questions DBQ1–DBQ8 from a read of the port ledger, DESIGN-FORMAT, wayfinder's Publish step and squadra | `handoffs/S1-scope.md` |
| S1 | 2026-10-09 | DB1 (part) | DBQ1 ruled as DB-D1 after `/ask-juval` and `/ask-eric`; DB-W added; squadra A–D in Rich's queue; DBQ2–DBQ4, DBQ7 annotated. Stopped at ~115K before DBQ2 | `handoffs/S1b-scope.md` |
