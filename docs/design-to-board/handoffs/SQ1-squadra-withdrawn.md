# Handoff: SQ1 · squadra learns "withdrawn" (board-writes, part 1)

Rich starts a fresh `claude` session in `~/Code/squadra` (it creates its own
worktree) and gives it this file. This session works in squadra, not in
claude-skills. It runs in parallel with design-to-board's S1b.

## Context

claude-skills' `design-to-board` will put increments on squadra's board.
Decision DB-D1 (claude-skills `docs/design-to-board/LEDGER.md`, Decisions)
puts every board write in squadra: `BoardAccess` gains `queue_increment`,
`withdraw_increment` and `increments_by_origin`, behind squadra CLI
subcommands that design-to-board calls. That work is activities A–D in
squadra. Part of A is still open in design-to-board's S1b (DBQ2, DBQ3,
DBQ4, DBQ7 shape the verbs and the CLI), so this session builds only what
DB-D1 already settles: the withdrawn state.

Read first, in order:
1. squadra `CLAUDE.md` and `GLOSSARY.md` (its rules win inside squadra: no
   Claude/Anthropic authorship trailers, type-prefixed commits, PR with
   merge commit, rebase onto `main` before merge).
2. DB-D1, read-only: `/Users/richinman/Code/claude-skills/.claude/worktrees/design-to-board/docs/design-to-board/LEDGER.md`
   (grep `DB-D1`; don't edit that file).
3. Eric's reasoning, read-only, sections "`Lifecycle.WITHDRAWN`" and "Key
   becomes Origin": `/Users/richinman/Code/board-knowledge/sessions/2026-10-09-eric-design-to-board-vocabulary.md`.
4. squadra code: `src/squadra/domain.py` (`Lifecycle`), `src/squadra/board.py`
   (`_lifecycle_of`, `validate_config`, `PROVIDERS`), the blocked logic in
   `src/squadra/supervisor.py` (~491–493), `src/squadra/engines.py`, and the
   contract-test fakes.

First step: create the worktree and branch `feat/board-writes` from `main`,
then create `docs/board-writes/LEDGER.md` from the seed below. That ledger is
the source of truth for squadra's A–D; claude-skills' ledger only points to it.

## This session's unit

Ledger items: SQ1
Goal: squadra models withdrawal, with no writer yet:
- `Lifecycle.WITHDRAWN`, terminal; the docstring's "domain invariant" is
  rewritten as a four-bucket model change (an ADR if squadra's ADR bar
  is met: hard to reverse, surprising, a real trade-off).
- Transitions asserted by tests: reachable from QUEUED; never from DONE;
  from ACTIVE left undecided (DBQ3), so it raises for now.
- A withdrawn item is never claimed and never counts as done; its successors
  are reported blocked with a distinct reason ("predecessor withdrawn"), not
  the in-flight blocked label.
- An unmapped native state fails `validate_config` loudly instead of
  defaulting to QUEUED (`board.py` `_lifecycle_of`).
- The contract-test fakes and `[board.states]` config learn `withdrawn`.
- `GLOSSARY.md` rows **Origin** and **Withdrawn**, from Eric's drafts.
- `squadra tick --dry-run` still passes its contract test.
Then a PR to squadra `main`.
Estimated work: ~60–80K tokens (budget: under 100K total, hard stop at 120K)

## Out of scope for this session

- The three verbs, the CLI subcommands, Origin storage and the fake
  provider's write half (SQ2+, after S1b rules DBQ2/3/4/7).
- The GitHub adapter (D).
- Any write in claude-skills or board-knowledge.

## Wrap-up

Update `docs/board-writes/LEDGER.md` (status, session log, next handoff in
`docs/board-writes/handoffs/`), commit, push, open the PR. Tell Rich the PR
URL and the next handoff path; he updates claude-skills' queue.

---

## Seed: `docs/board-writes/LEDGER.md`

```markdown
# board-writes: ledger

Branch: `feat/board-writes`
Goal: squadra owns every board write design-to-board needs (claude-skills
DB-D1): `Lifecycle.WITHDRAWN`, then `queue_increment(origin, parent,
predecessors, title, body) -> item_id`, `withdraw_increment(item_id)` (by
Origin since DB-D10),
`increments_by_origin(parent) -> {origin: (item_id, Lifecycle)}`, behind
CLI subcommands, with a registered fake provider, then the GitHub adapter.

Decisions come from claude-skills `docs/design-to-board/LEDGER.md` (DB-D1
and later DB-D<n>); cite them by ID, don't copy them. That ledger is
read-only from here. This file is the source of truth for squadra's part.

## Session budget

Under ~100K tokens per session, hard ceiling 120K, one unit per session.

## Work items

| ID | Item | DB-D1 activity | Depends on | Status |
|---|---|---|---|---|
| SQ1 | `Lifecycle.WITHDRAWN`, transitions, second blocked reason, unmapped states fail `validate_config`, glossary rows Origin and Withdrawn | A (part) | DB-D1 | in progress |
| SQ2 | Verb contract on `BoardAccess` + CLI surface; Origin stored opaquely; ACTIVE → WITHDRAWN rule | A (rest) | SQ1; design-to-board S1b rulings on DBQ2, DBQ3, DBQ4, DBQ7 | blocked |
| SQ3 | Fake provider implementing the verbs, registered in `PROVIDERS`; contract tests | B | SQ2 | todo |
| SQ4 | CLI subcommands as Clients; orchestration applies claim scope and the withdraw-while-active rule | C | SQ2, SQ3 | todo |
| SQ5 | GitHub adapter, reads and writes; `[[boards]]` and `in_claim_scope` (WSQ1) | D | SQ2; after design-to-board F per DB-D1 order | todo |

## Session log

| Session | Date | Unit | Outcome | Handoff written |
|---|---|---|---|---|
```
