# UI prototype

Several **radically different** UI variants in one place, switchable from a floating bar. The user flips between them, then gives the verdict: one variant, a mix of several, or none.

If the question is about logic or state rather than looks, this is the wrong branch. Use [LOGIC.md](LOGIC.md).

## Where the variants live

A UI is much easier to judge against the rest of the app (the real header, real data, real density). On an empty page, every variant looks fine. So pick the first sub-shape that fits:

- **A: an existing page (preferred).** The variants render on the existing route, gated by a `?variant=` search param. The existing data fetching, params and auth stay, and only the rendered subtree swaps. Something that would naturally live inside a page (a new card, section or step) is still sub-shape A: mount the variants inside the page that would host it. This is the only case where the prototype touches a production file (SKILL.md, rule 6). Keep the change to the switcher mount and make it removable in one revert.
- **B: a new throwaway route.** Use this only when there's an app but no page could sensibly host the variants. Follow the project's routing convention and put `prototype` in the path, e.g. `/prototype/<name>`.
- **C: no app to host it.** The repo has no web front end (a Python service, a docs repo, a CLI). Build one self-contained HTML file named `<name>.prototype.html` next to what it prototypes, with every variant inline, the same switcher and the same `?variant=` param, and realistic sample data inline. It opens by double-click.

## Process

### 1. State the question and pick N

Use **3 variants** by default, and never more than 5: past that, they stop being radically different. Write the plan in one line at the top of the prototype file:

> Three variants of the site summary card, switchable via `?variant=`, on the existing `/sites/:id` page.

### 2. Draft radically different variants

Each variant uses the page's real purpose and data, and the project's styling system (A and B) or plain inline CSS (C). Give each one a key and a short name, e.g. `A (Timeline)`, `B (Sidebar)`, `C (Single table)`.

Variants must differ in **structure**: layout, information hierarchy and the primary affordance, not colour or copy. If two drafts come out alike, redraft one with an explicit constraint ("no card grid"). A shared header is fine. A shared layout defeats the point.

### 3. Wire the switcher

One switcher picks the variant from `?variant=` (default `A`) and renders it. In sub-shape A, all existing data fetching stays above the switcher.

The floating bar is a small, fixed pill at the bottom centre, styled so it is obviously not part of any design:

- **← / →** buttons cycle through the variants (wrapping around), and the arrow keys do the same unless an `<input>`, `<textarea>` or `[contenteditable]` has focus.
- A **label** shows the current key and name, e.g. `B (Sidebar)`.
- Switching updates the URL (with the framework's router in A and B, or `history.replaceState` in C), so a variant can be shared and survives a reload.
- In A and B, it is hidden in production builds (`process.env.NODE_ENV !== 'production'` or the equivalent), so a stray merge can't ship it.

### 4. Hand it over

Hand it over as [SKILL.md](SKILL.md) says: the URL or file path, the command to start it, and every `?variant=` key with its name. Then wait for the user to pick. The most useful answer is usually a mix ("B's header with C's sidebar"), and that mix is the user's verdict to give, not yours.

## Anti-patterns

- **Variants that differ only in colour or copy.** That's a tweak, not a prototype.
- **Variants wired to real mutations.** Point anything that would write at a stub. The question is how it looks, not whether the backend behaves.
- **Picking the winner.** Say what you noticed about each variant if that helps, but the user picks.
- **Promoting a variant to production.** It was written under prototype rules. After the verdict, the user starts the build, and the variant gets rewritten properly there.
