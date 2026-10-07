# Bootstrapping a glossary for an existing codebase

Use this when a repo has code but no `GLOSSARY.md` and the user wants one. The work is split into batches so that neither you nor Eric reads the whole codebase at once, and the user reviews each batch before anything is written.

If `board-eric` is not available, say so and stop: every step below leads to a write, and every write needs Eric.

## 1. Batch the repo

List the top-level modules (one batch per top-level source directory or package; fold tiny ones together). Show the list to the user and let them drop or merge batches before you start. Work the batches one at a time, in the order the user prefers.

## 2. Extract candidate terms (read-only subagents)

For each batch, dispatch a read-only subagent (Agent tool, `subagent_type: Explore`; tell it it must not edit anything). Several batches can run in parallel. Ask each for:

- candidate domain terms in that batch: concepts specific to this business, not general programming concepts;
- for each: a one-line candidate definition (what it IS), the other names the code uses for the same thing, and `file:line` evidence for each name;
- at most about 25 terms, most central first;
- no code in the reply beyond identifiers.

## 3. Eric reviews the batch

Send Eric (`subagent_type: board-eric`) that batch's term list, never the raw code or file contents. Include terms already approved from earlier batches so he can spot collisions. Ask, per term: keep, rename (to what), merge with another term, or drop; and flag any term that seems to mean something different in another batch.

## 4. The user reviews the batch draft

Draft the batch's glossary entries in the [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md) format, applying Eric's verdicts, and show it with his notes beside the terms he changed or dropped. Put the remaining choices (which name wins, whether two terms are distinct) to the user as questions. Nothing is written until the user approves the batch.

Once approved, add the batch's entries to the root `GLOSSARY.md` and announce the write. Hold the `GLOSSARY-SETTLED.md` rows until step 6: a row's `Context` can never change after it is written, and the contexts aren't fixed until step 5.

## 5. Final pass: context boundaries

When every batch is approved, send Eric all the approved per-batch term lists together (still no code). Ask whether they form one bounded context or several, which terms collide across batches, and whether `GLOSSARY-MAP.md` is needed.

If he proposes several contexts, put the split to the user. On approval, create `GLOSSARY-MAP.md` and move each context's entries into its own `GLOSSARY.md`, as in [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md).

## 6. Settle

For every approved term, `Settle(term, rejected, context, ruling, ref)` in its final context, with `ref` as `session:<today's date>` unless the caller passed one. Distinction rulings the user made along the way are settled too. Announce the rows in one list.
