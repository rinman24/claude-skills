---
name: domain-modeling
description: Build and sharpen a project's domain language. Use when discussing codebase terminology, settling what a term means, writing or editing GLOSSARY.md, checking whether a naming question was already settled, or bootstrapping a glossary for an existing codebase.
---

# Domain Modeling

Actively build and sharpen the project's domain model as you design: challenge terms, invent edge-case scenarios, and write the language down the moment it is settled. Merely _reading_ `GLOSSARY.md` for vocabulary is not this skill; any skill can do that. This skill is for changing the model.

## Files

All at the repo root, created lazily (only when there is something to write):

- `GLOSSARY.md`: the language. Format: [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md).
- `GLOSSARY-MAP.md`: only in multi-context repos; points to each context's `GLOSSARY.md`. Same format file.
- `GLOSSARY-SETTLED.md`: the settled record, one row per naming ruling, never deleted. Format and operations: [SETTLED-FORMAT.md](./SETTLED-FORMAT.md).

Read all three that exist before the first question. In a multi-context repo, infer which context the topic belongs to; if unclear, ask.

## Eric reviews every write

Every write to `GLOSSARY.md` or `GLOSSARY-MAP.md`, every `Settle`, and every pruning pass goes to Eric Evans first: call the Agent tool with `subagent_type: board-eric`. Do not use `/ask-eric`, and write no session file; the glossary and the settled record are the record.

Give Eric the proposed entry (term, definition, `_Avoid_` forms, context, one-line ruling), the existing entries it sits next to, and any `Lookup` hits. Never send him raw code. Ask for a short verdict: approve, approve with a sharper wording, or object, with one line of reason.

- Approve: write it, exactly as Eric saw it.
- Sharper wording or objection: don't write yet (unless the user accepted a sharper wording in advance; see below). Put Eric's point to the user as a question in the next round. The user decides; Eric advises.

Only two wordings can be written: one Eric approved unchanged, or one the user approved after Eric's verdict (or in advance, in so many words: "if Eric only sharpens it, I accept"). Any other change after Eric has seen it (taking his sharper wording, departing from his verdict, or your own edit) goes to the user as a question first. A note in a draft is not a question.

If `board-eric` is not an available agent type, or the call fails, say so plainly at the start: "`board-eric` isn't available here, so I'll challenge and sharpen terms but won't write `GLOSSARY.md`, `GLOSSARY-MAP.md` or `GLOSSARY-SETTLED.md`." Don't offer the drafted entries for the user to paste in by hand, or any other route around Eric's review. Everything read-only (challenging, `Lookup`, drift reports) still runs. `Reopen` adds no language and records only the user's instruction, so it does not need Eric.

## During the session

### Look up before you ask

Before raising any naming question, run `Lookup(form, context)` against `GLOSSARY-SETTLED.md` and act on the answer as [SETTLED-FORMAT.md](./SETTLED-FORMAT.md) says. A settled ruling is not a question: use it.

### Challenge against the glossary

When the user uses a term that conflicts with `GLOSSARY.md`, call it out immediately: "Your glossary defines 'cancellation' as X, but you seem to mean Y. Which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term: "You're saying 'account': do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios that probe edge cases and force precision about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If it doesn't, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible. Which is right?"

### Drift is not reopening

When code or the user's wording uses a form a ruling rejected, report it as drift and keep going: "Drift: code uses Purchase; settled as Order on 2026-10-06 (gh:org/repo#123)." Don't turn it into a question, and never use the word "reopen" in a drift report. Only the user reopens a ruling.

## Writing a term

When the user settles a term, write it right then. Don't batch.

1. **Term or spec?** The entry defines what the term IS, in one or two sentences, with no implementation detail. The same test applies to the one-line ruling. If it describes behaviour, storage or an algorithm, it belongs in a spec or an ADR; cut it.
2. **Lookup.** If the form is already `settled-term`, `rejected-form` or `distinct-from` in this context, there is nothing to settle; a change needs the user to reopen it first.
3. **Eric** reviews it (above).
4. **Write both files.** Add or update the entry in `GLOSSARY.md` and `Settle(term, rejected, context, ruling, ref)` a row in `GLOSSARY-SETTLED.md`. `ref` is what the caller passed in (wayfinder passes its ticket ref); otherwise `session:<today's date>`.
5. **Announce it** at the top of your next round or reply, so the user reviews every write:

   ```
   📝 Written since last round:
   - GLOSSARY.md: **Order** (Sales), avoid Purchase, Transaction
   - GLOSSARY-SETTLED.md: Order settled in Sales, rejects Purchase, Transaction (session:2026-10-06)
   - Wording: Eric approved
   ```

   Say who approved each wording: `Eric approved`, or `you approved` (or `you approved in advance`) plus what Eric said when it differs (e.g. `you approved; Eric had sharpened it to "…"`). Never say the user accepted a wording they weren't asked about.

   A correction to something just written is a reopen by the user followed by a new `Settle`; rows are never edited or deleted.

When grilling runs alongside this skill, grilling writes nothing; this skill owns every doc write, and its announcement goes at the top of grilling's next round.

## Reopen

Only on the user's explicit instruction ("reopen Order", "let's revisit Site"): `Reopen(form, context, reason, ref)`. It flips the row to `reopened`, or to `withdrawn` when the user says the concept has gone with no replacement. The reopened question then stays on your frontier until a new `Settle` supersedes the row. Never reopen on your own initiative, and never because of drift.

## Bloat guard

Run after every write. When `GLOSSARY.md` passes about 40 terms or 150 lines, propose a pruning pass with specific cuts (general programming concepts, terms nobody uses any more, definitions that have grown into specs) and send it to Eric first. Pruning touches `GLOSSARY.md` only. The settled record is never pruned, and a pruned term's ruling still holds.

## Decisions that need an ADR

ADRs are not glossary entries. When a decision is hard to reverse, surprising without context and the result of a real trade-off, call the `adr` skill (Skill tool) if it is installed; otherwise suggest recording an ADR and name what it would cover. Don't write one from here.

## Existing codebase, no glossary

For a repo with code but no `GLOSSARY.md`, offer a bootstrap and follow [BOOTSTRAP.md](./BOOTSTRAP.md). It needs `board-eric` for every step that leads to a write.
