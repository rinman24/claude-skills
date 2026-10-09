---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea, a round of questions at a time, until you reach a shared understanding. Use when the user wants to stress-test their thinking, get grilled on a design, or uses any "grill" phrase ("grill me", "grill this"). An interview only; it never writes code.
---

Interview the user relentlessly until you reach a shared understanding. Map the subject as a **design tree**: every decision branches into the decisions that hang off it.

## Never write code

Grilling is an interview, not a build. For the whole session, and after the user confirms, do not write, edit or scaffold code, do not sketch code inside a question, and do not create or edit files. Read whatever you need. Tell every sub-agent you dispatch that it is read-only. If the user asks you to build something mid-session, say that ends the grilling and stop the skill before anything is built.

## Rounds

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round.

Format a round like so:

```
❓ **Q1** - **<question title>**: <why it matters now, then the question and any choices>

➡️ <your recommended answer to the question as worded>

---

❓ **Q2** - **<question title>**: <why it matters now, then the question and any choices>

➡️ <your recommended answer to the question as worded>
```

Keep each question body to about three lines, one of which says what the answer unblocks. Long questions wear the user out and hide why you are asking. The recommendation answers the question as worded ("Yes: …", "No: …", "Option B: …"). If you would argue against the question's premise, reword the question instead.

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

If a frontier grows past about eight questions, the scope is probably too big. Propose splitting it into pieces to grill one at a time, and let the user decide.

## Clarification

The user may answer a question by asking what it means ("Q2?", "what do you mean by …"). That is not an answer. Re-explain that question in plain words, with a concrete example of what each choice would mean in practice, restate your recommendation, and wait. Questions answered in the same reply are settled; the one being clarified stays open, along with everything downstream of it.

## Facts and decisions

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), dispatch a read-only sub-agent to find it; don't ask the user for anything you could look up yourself. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the sub-agent to report; ask the rest of the frontier now.

The _decisions_ are the user's: put each to them and wait. This holds when another skill or a ticket runs grilling too. Being asked to resolve something is never permission to answer the user's decisions yourself.

## Ending

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Then post a numbered summary of every decision reached, one line each, and ask the user to confirm it is a shared understanding. Wait for an explicit yes. A correction reopens the branches it touches as a new round.

Confirmation ends this skill. Hand back to the user, or to the skill that called you, without acting on the plan; name the natural next step and let them start it.
