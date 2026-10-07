---
name: prototype
description: Build a throwaway prototype to settle one open design question that talking can't settle, either a clickable logic demo ("does this state model feel right?") or several radically different UI variants ("what should this look like?"). Use when the user asks to prototype, mock up or try variants of something undecided, or when another skill (e.g. wayfinder) hands over a prototype ticket. Not for building a settled design or a whole-app demo. The user always picks the verdict; the skill never builds the real thing.
---

# Prototype

A prototype is **throwaway code that answers one question**. The question decides its shape, and the user's verdict is the answer.

## First, check there is a question

Before building anything, name the open design question in one sentence. Build only if that question is unsettled and talking hasn't settled it.

- **The design is already settled** (decided in conversation, in an ADR, or on a closed ticket): say so in one line and stop. The next step is building it, and that is not this skill's job.
- **The ask is the whole application** (a demo for prospects, "prototype the app"): say that it isn't one question and stop. Offer to cut it down to the single question that is actually open.
- **The question is grillable** (it could be answered by talking it through): suggest `/grilling` instead, and build only if the user still wants a prototype.

## Pick a branch

Which question is being asked?

- **"Does this logic or state model feel right?"** → [LOGIC.md](LOGIC.md): one self-contained HTML file that anyone can drive by clicking.
- **"What should this look like?"** → [UI.md](UI.md): several radically different variants that you switch between in one place.

The two branches produce very different artifacts, so ask the user if the question fits either. If they can't be reached, use the surrounding code to decide (a backend module → logic, a page or component → UI) and state that assumption at the top of the prototype.

## Rules for both branches

1. **Throwaway, and visibly so.** Put it next to what it prototypes, and give it a name with `prototype` in it. For a UI route, follow the project's routing convention.
2. **Trivial to run.** One command, or a file you double-click.
3. **No persistence.** State lives in memory. If persistence is the question, use a scratch file or database named so it's obvious it can be wiped (`PROTOTYPE-wipe-me`).
4. **No polish.** No tests, no error handling beyond what keeps it running, no abstractions, no generalising. The moment you harden it, you have stopped prototyping.
5. **Surface the state.** Show the full relevant state after every action or variant switch.
6. **Write only prototype files.** Never edit production code, not even to mount a variant, unless UI.md's sub-shape A needs a switcher on an existing page. In that case, keep the change to that page and make it removable in one revert.

## Hand it over and wait

When it runs, hand it over:

```
🧪 Prototype ready: <path or URL, plus the command to start it>
Question: <the one-sentence question>
Options: <variant keys and names, or the walkthrough tabs>
Which one? (a variant, a mix like "B's header with C's sidebar", "holds" or "change X", or "none, the question changes")
```

Then **stop and wait for the user's verdict.** It always comes from the user:

- Never pick a variant, rule a model sound, or record a verdict yourself, even if one looks clearly best. You may say what you noticed in each option, but not which one wins.
- This holds when you run headless, when the user is away, and when another skill or a ticket asked you to resolve the question. Being asked to resolve a question doesn't give you permission to answer it for the user. Leave the question open and report that the prototype is waiting for a verdict.
- If the user asks for changes ("add a scenario", "try a variant without the sidebar"), make them and hand over again. Prototypes evolve until the user rules.

## After the verdict

1. **Record it.** In one line, give the question and the user's verdict in their own words. Put it wherever the caller asks (e.g. a wayfinder ticket's resolution). Otherwise, put it in your reply.
2. **Offer to keep the prototype.** The prototype is the evidence the verdict came from, so offer once to commit it to a throwaway `prototype/<name>` branch that is never merged. Create that branch only on the user's yes, and give its name with the verdict. Either way, the current branch ends as it was before the prototype: with the user's yes, take every prototype file and any switcher mount off it; on a no, ask before deleting them.
3. **Stop.** Don't fold the winner into the real code or promote a variant into a real route. Name the natural next step (e.g. "build the settings page from variant B") and let the user start it.

```
✅ Verdict: <question> → <user's verdict>. Prototype kept on prototype/<name>.
Next step (yours to start): <one line>
```
