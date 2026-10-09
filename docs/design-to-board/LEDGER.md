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
- [ ] Fill in `## Choice` in `~/Code/board-knowledge/sessions/2026-10-09-juval-design-to-board-write-path.md`
      and `2026-10-09-eric-design-to-board-vocabulary.md` ((c) as amended; Eric's vocabulary in full).
- [ ] squadra A: contract for `queue_increment` / `withdraw_increment` /
      `increments_by_origin`, `Lifecycle.WITHDRAWN` (terminal, never from DONE,
      ACTIVE per DBQ3), unmapped states fail `validate_config`, second blocked
      reason, CLI surface; glossary rows **Origin** and **Withdrawn** (Eric's
      drafts in his session file). Check the cross-map Origin lookup before freezing.
- [ ] squadra B: fake provider implementing the verbs, registered in `PROVIDERS`; contract tests.
- [ ] squadra C: CLI subcommands + orchestration rules (claim scope, withdraw-while-active).
      design-to-board's F needs C.
- [ ] squadra D: GitHub adapter, reads and writes (already P1; now includes the write half).
      Order A → B → C → (design-to-board E, F) → D → G.

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
| DBQ2 | Mostly answered by DB-D1 (the mapping is the item's Origin, read with `increments_by_origin`); confirm, and settle the cross-map lookup (Eric: `increments_by_origin(parent)` is scoped by parent, a `<map>:<ID>` predecessor may sit under another parent). Where does the increment ID → board item mapping live? `Published` holds only `r<N>`, and the translator never patches the document (WD14) | Needed for idempotent re-runs, withdrawals and `<map>:<ID>` cross-map dependencies. Candidates: on the item (title, label, body marker), or a file the translator owns |
| DBQ3 | Half answered by DB-D1 (`withdraw_increment` → `Lifecycle.WITHDRAWN`). Open: Juval's blocking Q2 (is a revision published while squadra still runs an earlier revision's increments? if not, squadra refuses ACTIVE → WITHDRAWN, else C needs a cancel path) and Eric's blocking Q2 (can a revision withdraw a row whose increment is DONE, directly or through a foundation's `Kind` cell?). What does "withdraw" do on the board (close, state, label)? And must it refuse to withdraw an item squadra has already claimed? | WD22: the translator only creates and withdraws |
| DBQ4 | Mostly answered by DB-D1 (squadra's CLI checks claim scope and refuses an out-of-scope parent). Open: which parent design-to-board passes, and how it finds the target squadra config. How is claim scope honoured? Presumably `"parents"` → create each item under a `parent_scope_ids` parent (which one?), `"whole-board"` → anywhere. Where does it find the target `squadra.toml`? | `[[boards]]` (WSQ1) will change the config shape later |
| DBQ5 | What does "fails loudly back to wayfinder" mean concretely: a report to the user naming the failed check and row, writing nothing? | WD14, WD18 |
| DBQ6 | WD14 fails on "missing kind", but DESIGN-FORMAT and WD10 allow a blank Kind. Which holds? | Probably reword WD14 ("unknown kind") |
| DBQ7 | Eric's blocking Q1: if new items land held rather than QUEUED, the verb is renamed after the held state and "queue" goes to whatever releases it. Is publishing live? New queued in-scope items are claimable at the next tick. Should the skill end by suggesting `squadra tick --dry-run`, or create items in a non-queued state? | Must never set `tag_prefix` tags (WSQ1) |
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

## Session log

| Session | Date | Unit | Outcome | Handoff written |
|---|---|---|---|---|
| S0 | 2026-10-09 | Setup | Branch `feat/design-to-board` from `main` `205c5f2`; this ledger, lessons, template and S1 handoff; open questions DBQ1–DBQ8 from a read of the port ledger, DESIGN-FORMAT, wayfinder's Publish step and squadra | `handoffs/S1-scope.md` |
| S1 | 2026-10-09 | DB1 (part) | DBQ1 ruled as DB-D1 after `/ask-juval` and `/ask-eric`; DB-W added; squadra A–D in Rich's queue; DBQ2–DBQ4, DBQ7 annotated. Stopped at ~115K before DBQ2 | `handoffs/S1b-scope.md` |
