# GLOSSARY-SETTLED.md Format

`GLOSSARY-SETTLED.md` is the settled record: one row per naming ruling, at the repo root, shared by every context. It answers one question deterministically, without a network or a tracker: has this naming question already been ruled on here?

It is separate from `GLOSSARY.md` because the two have opposite retention rules. The glossary gets pruned; rulings are permanent.

## Structure

```md
# Settled terms

Rulings domain-modeling must not reopen on its own initiative. Match Term or Rejected within the same Context, case-insensitive. Reopen only on explicit user instruction; a reopened row is superseded when the term is settled again. Never delete.

| Term | Rejected | Context | Ruling | Status | Settled | Ref |
|---|---|---|---|---|---|---|
| Order | Purchase, Transaction | Sales | Use Order for a customer's request to buy | settled | 2026-10-06 | gh:org/repo#123 |
| Site, Campus | | Generation | Not synonyms; a Campus groups Sites | settled | 2026-10-06 | session:2026-10-06 |
| Module | Unit | Generation | Use Module for a swappable battery block | reopened | 2026-09-01 | session:2026-09-01 |
```

The rows above are illustrative, not rulings. Copy the header line exactly when creating the file.

## Columns

- **Term**: the chosen term. A distinction ruling ("these are different things") lists every term it separates here, comma-separated, and leaves `Rejected` empty.
- **Rejected**: the forms ruled out in favour of `Term`, comma-separated. Mirrors `_Avoid_` in `GLOSSARY.md`, but survives pruning.
- **Context**: the bounded context, named as in its `GLOSSARY.md` heading (`# {Context Name}`). A single-context repo still fills it in.
- **Ruling**: one line a person can read. Not a definition and not rationale; the "term or spec?" test applies. Rationale lives behind `Ref`.
- **Status**: `settled`, `reopened`, `superseded` or `withdrawn`.
- **Settled**: the date the row was written, `YYYY-MM-DD`.
- **Ref**: an opaque `scheme:locator` pointing to where the argument happened: `gh:`, `scratch:`, `backlog:`, `session:`. Never follow it during a lookup. A caller such as wayfinder passes its own ticket ref; with no caller ref, use `session:<date>`.

## Rules

- Rows are never deleted and never edited, except the `Status` cell, which only moves forward:
  - `settled` → `reopened` → `superseded`
  - `settled` or `reopened` → `withdrawn`
- The bloat threshold does not apply to this file, and pruning `GLOSSARY.md` never changes it.
- Git history on the file is the audit trail (who, when, which PR).

## Operations

Three operations, all owned by domain-modeling. Grilling never calls them.

### `Settle(term, rejected, context, ruling, ref)` (command)

Called at the same moment `GLOSSARY.md` is written, after Eric reviews it. Appends a `settled` row. If a `reopened` row covers any of these forms in this context, flip that row to `superseded`. Re-settling the same ruling after a reopen still appends a new row with the new ref, so the reconfirmation is on record.

Settle never overrides a `settled` row. If one covers the form in this context, the user has to reopen it first.

### `Lookup(form, context)` (query, no writes)

Match `form` case-insensitively against `Term` and `Rejected` on rows whose status is `settled` or `reopened`. `superseded` and `withdrawn` rows are history; Lookup ignores them. Return exactly one answer:

| Answer | When | What the skill does |
|---|---|---|
| `settled-term` | `form` is the single `Term` of a `settled` row in this context | Use it. Don't ask. |
| `rejected-form(→ term)` | `form` is in `Rejected` of a `settled` row in this context | Report drift ("Drift: code uses Purchase; settled as Order on …") and continue. Don't ask. |
| `distinct-from(other)` | `form` is one of several `Term`s of a `settled` distinction row in this context | Don't ask, and don't propose merging them. |
| `reopened` | the matching row in this context is `reopened` | The question is open: ask it, and don't enforce the old ruling. |
| `ruled-in(other context)` | no row in this context, but one in another | Information only. Mention it if it helps; don't enforce it here. |
| `unsettled` | no match | Ask the question if it matters. |

Drift reports never use the word "reopen".

### `Reopen(form, context, reason, ref)` (command, explicit user instruction only)

Run only when the user says to reopen or revisit a ruling. Flip the matching `settled` row to `reopened`; write no new ruling. Lookup returns `reopened` until a later Settle supersedes the row.

If the user says the concept has gone with no replacement (for example, the reference architecture changed), flip the row to `withdrawn` instead. Lookup then ignores it.

Put `reason` and `ref` in the announcement of the change; the row itself keeps its original `Settled` and `Ref`.
