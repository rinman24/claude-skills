# GLOSSARY.md Format

## Structure

```md
# {Context Name}

{One or two sentence description of what this context is and why it exists.}

## Language

**Order**:
{A one or two sentence description of the term}
_Avoid_: Purchase, transaction

**Invoice**:
A request for payment sent to a customer after delivery.
_Avoid_: Bill, payment request

**Customer**:
A person or organization that places orders.
_Avoid_: Client, buyer, account
```

The `# {Context Name}` heading is the name `GLOSSARY-SETTLED.md` uses in its `Context` column.

## Rules

- **Be opinionated.** When multiple words exist for the same concept, pick the best one and list the others under `_Avoid_`. The same forms go in the settled row's `Rejected` column.
- **Keep definitions tight.** One or two sentences max. Define what it IS, not what it does.
- **Term or spec?** Before every write, ask whether the entry defines a word or describes behaviour, storage, an algorithm or a decision. Only the first belongs. The rest goes in a spec or an ADR. `GLOSSARY.md` is not a spec, a scratch pad or a home for implementation decisions; it is a glossary and nothing else.
- **Only include terms specific to this project's context.** General programming concepts (timeouts, error types, utility patterns) don't belong even if the project uses them extensively. Before adding a term, ask: is this a concept unique to this context, or a general programming concept? Only the former belongs.
- **Group terms under subheadings** when natural clusters emerge. If all terms belong to a single cohesive area, a flat list is fine.

## Bloat guard

Past about 40 terms or 150 lines in one `GLOSSARY.md`, propose a pruning pass. Name each cut and why:

- general programming concepts that slipped in;
- terms nobody uses any more, in code or conversation;
- definitions that have grown past two sentences or into behaviour (trim them back, don't delete the term).

Eric reviews the pass before anything is cut, and the user approves it. Pruning edits `GLOSSARY.md` only. A pruned term's row in `GLOSSARY-SETTLED.md` stays as it is, and its ruling still holds.

## Single vs multi-context repos

**Single context (most repos):** One `GLOSSARY.md` at the repo root.

**Multiple contexts:** A `GLOSSARY-MAP.md` at the repo root lists the contexts, where they live, and how they relate to each other:

```md
# Glossary Map

## Contexts

- [Ordering](./src/ordering/GLOSSARY.md): receives and tracks customer orders
- [Billing](./src/billing/GLOSSARY.md): generates invoices and processes payments
- [Fulfillment](./src/fulfillment/GLOSSARY.md): manages warehouse picking and shipping

## Relationships

- **Ordering → Fulfillment**: Ordering emits `OrderPlaced` events; Fulfillment consumes them to start picking
- **Fulfillment → Billing**: Fulfillment emits `ShipmentDispatched` events; Billing consumes them to generate invoices
- **Ordering ↔ Billing**: Shared types for `CustomerId` and `Money`
```

`GLOSSARY-SETTLED.md` stays a single file at the root for every context.

The skill infers which structure applies:

- If `GLOSSARY-MAP.md` exists, read it to find contexts
- If only a root `GLOSSARY.md` exists, single context
- If neither exists, create a root `GLOSSARY.md` lazily when the first term is settled

When multiple contexts exist, infer which one the current topic relates to. If unclear, ask.
