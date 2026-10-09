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
- [ ] Optional, before S1: `git -C ~/Code/squadra pull` on `main`. Local
      `main` is at `d9d2afa`, behind squadra PR #42 (mandatory claim scope),
      whose code is otherwise only in squadra's `mandatory-claim-scope`
      worktree. S1 reads squadra; it will use whichever is current.

## Work items

| ID | Item | Unit | Est. | Status | Notes |
|---|---|---|---|---|---|
| DB1 | Scope `design-to-board`: settle the open questions below (Rich rules; Juval and Eric where named), then split the build into units of ~80K | S1 | ~50–70K | todo | Handoff `handoffs/S1-scope.md`. Records decisions; builds nothing |
| DB2+ | Build units | — | — | todo | Defined by DB1 |
| DB-G | When T1 ships: `GLOSSARY-MAP.md:9` "(not yet built) will read" → "reads" (WD27) | last build unit | ~1K | todo | |

## Open questions (for DB1)

Found while setting up (research brief, 2026-10-09). Each becomes a decision
in the table below, or `dropped`.

| ID | Question | Notes |
|---|---|---|
| DBQ1 | Write path: squadra has no create operation, ADO is its only adapter (and dropped by Rich), GitHub is deferred. Does `design-to-board` write to the provider directly, wait for squadra's GitHub adapter, or add create/link operations to squadra first? Which provider first? | Decides everything below. Closed architecture: the board write is ResourceAccess (WD14); where that access lives is the question |
| DBQ2 | Where does the increment ID → board item mapping live? `Published` holds only `r<N>`, and the translator never patches the document (WD14) | Needed for idempotent re-runs, withdrawals and `<map>:<ID>` cross-map dependencies. Candidates: on the item (title, label, body marker), or a file the translator owns |
| DBQ3 | What does "withdraw" do on the board (close, state, label)? And must it refuse to withdraw an item squadra has already claimed? | WD22: the translator only creates and withdraws |
| DBQ4 | How is claim scope honoured? Presumably `"parents"` → create each item under a `parent_scope_ids` parent (which one?), `"whole-board"` → anywhere. Where does it find the target `squadra.toml`? | `[[boards]]` (WSQ1) will change the config shape later |
| DBQ5 | What does "fails loudly back to wayfinder" mean concretely: a report to the user naming the failed check and row, writing nothing? | WD14, WD18 |
| DBQ6 | WD14 fails on "missing kind", but DESIGN-FORMAT and WD10 allow a blank Kind. Which holds? | Probably reword WD14 ("unknown kind") |
| DBQ7 | Is publishing live? New queued in-scope items are claimable at the next tick. Should the skill end by suggesting `squadra tick --dry-run`, or create items in a non-queued state? | Must never set `tag_prefix` tags (WSQ1) |
| DBQ8 | Determinism (WD13): two AFK runs on one document give identical increments. How is that tested (fake board, golden output)? | Shapes the build's test unit |

Housekeeping noticed (fix when convenient, not blocking): WD14 still says
"> 2 new services" (WD23 replaced it with ≤ 2 changed); Juval's ninth item
("writes only rows published or withdrawn in the current revision") is
translator behaviour, not a DESIGN-FORMAT check; squadra's
`docs/design/board-provider-seam.md:146` still calls the parent scope optional.

## Decisions

| ID | Decision | Status | Detail |
|---|---|---|---|

## Session log

| Session | Date | Unit | Outcome | Handoff written |
|---|---|---|---|---|
| S0 | 2026-10-09 | Setup | Branch `feat/design-to-board` from `main` `205c5f2`; this ledger, lessons, template and S1 handoff; open questions DBQ1–DBQ8 from a read of the port ledger, DESIGN-FORMAT, wayfinder's Publish step and squadra | `handoffs/S1-scope.md` |
