# Bootstrapping a glossary for an existing codebase

Use this when a repo has code but no `GLOSSARY.md` and the user wants one. The work is split into batches so that neither you nor Eric reads the whole codebase at once, and the user reviews each batch before anything is written.

If `board-eric` is not available, say so and stop: every step below leads to a write, and every write needs Eric.

## 1. Batch the repo

List the top-level modules (one batch per top-level source directory or package; fold tiny ones together). When the top-level directories are layers rather than modules (e.g. `access`, `contracts`, `workspace`), batch per subsystem instead, across the layers. Show the list to the user and let them drop or merge batches before you start. Work the batches one at a time, in the order the user prefers.

## 2. Extract candidate terms (read-only subagents)

For each batch, dispatch a read-only subagent (Agent tool, `subagent_type: Explore`; tell it it must not edit anything). Several batches can run in parallel. Ask each for:

- candidate domain terms in that batch: concepts specific to this business, not general programming concepts;
- for each: a one-line candidate definition (what it IS), the other names the code uses for the same thing, and `file:line` evidence for each name;
- at most about 25 terms, most central first;
- no code in the reply beyond identifiers.

## 3. Eric reviews the batch

Send Eric (`subagent_type: board-eric`) that batch's term list, never the raw code or file contents. Include terms already approved from earlier batches so he can spot collisions. Ask, per term: keep, rename (to what), merge with another term, or drop; and flag any term that seems to mean something different in another batch.

## 4. The user reviews the batch draft

Draft the batch's glossary entries in the [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md) format, applying Eric's verdicts, and show it with his notes beside the terms he changed or dropped. Put the remaining choices (which name wins, whether two terms are distinct) to the user as questions. Where the draft departs from Eric's verdict, that is a question too, not a note. Nothing is written until the user says yes to the batch draft as shown ([SKILL.md](./SKILL.md), "Eric reviews every write"). A trim ("only the Host batch"), a change to another entry or "next batch" is not a yes: apply it, then ask `Approve batch N as drafted?`.

Once approved, add the batch's entries to the root `GLOSSARY.md` exactly as approved, and announce the write with the `📝 Written since last round:` list and its `Wording:` line ([SKILL.md](./SKILL.md), "Writing a term" step 5). A wording the user took from Eric is `you approved` plus Eric's text, never `Eric approved`: `Wording: you approved the batch draft; for Berth you approved Eric's rename ("…")`. A wording that changes after the user's approval, including Eric's sharpening in step 5, goes back to the user as a question before it is written. Hold the `GLOSSARY-SETTLED.md` rows until step 6: a row's `Context` can never change after it is written, and the contexts aren't fixed until step 5.

## 5. Final pass: context boundaries

When every batch is approved, send Eric all the approved per-batch term lists together (still no code). Ask whether they form one bounded context or several, which terms collide across batches, and whether `GLOSSARY-MAP.md` is needed.

If he proposes several contexts, put the split to the user. On approval, create `GLOSSARY-MAP.md` and move each context's entries into its own `GLOSSARY.md`, as in [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md).

Show the final pass's changes and step 6's rows as one draft, with the exact text of every line that is new or changed: `GLOSSARY-MAP.md`, each context's heading and description line, pointer lines (in `GLOSSARY.md` or other docs, such as a `CONTEXT-MAP.md` row), each wording Eric sharpened, and each row. Then ask `Approve the final pass and these N rows as drafted?`. "Run the final pass and Settle" asks you to draft them, not to write them.

## 6. Settle

For every approved term, `Settle(term, rejected, context, ruling, ref)` in its final context, with `ref` as `session:<today's date>` unless the caller passed one. Distinction rulings the user made along the way are settled too. Write only after the yes in step 5.

Announce the step 5 edits and the rows together in one `📝 Written since last round:` list ([SKILL.md](./SKILL.md), "Writing a term" step 5), one line per file and per row, ending with the `Wording:` line:

```
📝 Written since last round:
- GLOSSARY-MAP.md: created, contexts Hosting and Adoption
- GLOSSARY.md: Adopt entries moved to src/adopt/GLOSSARY.md; First start reworded
- docs/CONTEXT-MAP.md: Host and Adopt rows point to their GLOSSARY.md
- GLOSSARY-SETTLED.md: 27 rows (session:2026-10-08)
  - Host settled in Hosting, rejects VM, box
  - …
- Wording: you approved each batch draft and the final pass; for First start you approved Eric's text ("…")
```
