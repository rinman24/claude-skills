# Logic prototype

One self-contained HTML file that lets anyone drive a state model by clicking buttons. Use it when the question is about **business logic, state transitions or data shape**: things that look reasonable on paper but only feel wrong once you push real cases through them.

It is one file with nothing to install, so it can go to a non-developer (an engineer on the project, a PM, a domain expert), who can try the model out for themselves. It speaks their language, not the code's.

If the question is "what should this look like?", this is the wrong branch. Use [UI.md](UI.md).

## One model or competing models

- **Default: one model.** The user's verdict is "holds", or "change X".
- **Competing models**, only when the question itself names alternatives ("per-site or per-portfolio dispatch?"): build each model as its own pure module and switch between them with a model tab at the top. Every walkthrough runs against the selected model, so the same scenario can be compared across models. The user's verdict picks a model, a mix, or neither.

## Process

### 1. State the question

Write the question and the state model at the top of the page, in one visible paragraph, not a comment. Then the prototype can be checked against it later, whether or not the user is watching now.

### 2. Keep the logic in a pure module

Write the logic that answers the question as one small, pure module inside a single `<script>` block, in whichever shape fits the question:

- **A reducer**, `(state, action) => state`, when actions are discrete events and state is a single value.
- **A state machine** with explicit states and transitions, when "which actions are legal right now" is part of the question.
- **A few pure functions** over a plain data type, when there is no current state, only transformations.
- **A class with a clear method surface**, when the logic really does own ongoing state.

No DOM, no `document`, no button handlers inside it. The page calls into the module, and nothing flows the other way. That keeps the model readable on its own, so whoever builds the real thing later can see exactly what was validated.

### 3. Build the page

Plain HTML, CSS and JS, all inline: no framework, no bundler, no server. It must open by double-click and still open after being emailed.

Label everything in domain language (buttons and state read like the business, not the reducer). Lay it out top to bottom:

1. **Title and the question** from step 1.
2. **Current state** as a labelled panel (not a raw JSON dump), re-rendered after every click, with the change called out.
3. **Free-play buttons**: one per action, always available, so anyone can poke at the model in any order. An illegal action shows why it was refused instead of failing silently.
4. **Guided walkthroughs**, one scenario per tab. Each tab gives the scenario in plain words (what it sets up and what to watch for), with the ordered buttons to press underneath it. Starting a walkthrough resets to a known initial state. Cover the happy path, a hard edge case, and an attempt at something that should be illegal.

Keep it clean and restrained: readable type, generous spacing, one accent colour, no animation.

### 4. Hand it over

Hand it over as [SKILL.md](SKILL.md) says, giving the file path and the walkthrough tabs, then wait. The useful moments are "wait, that shouldn't be possible" and "huh, I assumed X": those are bugs in the *idea*, which is what the prototype is for. If the user asks for new actions or scenarios, add them and hand it over again.

## Anti-patterns

- **Tests, real databases, generalising.** Each one means you've stopped prototyping.
- **Logic mixed into the page.** If the module touches the DOM, nobody can read the validated model on its own.
- **A framework, bundler or dev server.** That breaks "double-click to open".
- **Moving the module into the real codebase.** That's the build, which the user starts after the verdict.
