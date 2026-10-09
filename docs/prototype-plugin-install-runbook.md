# Runbook: Install & verify the `prototype` Claude Code plugin

This is a self-contained runbook. It assumes no prior context. Goal: install the
`prototype` plugin from a personal plugin marketplace into a repo or dev
container and confirm it works.

---

## Background (what this is)

`prototype` is a Claude Code plugin distributed via a self-hosted plugin
marketplace — which is just a public GitHub repo plus a catalog file.

- **Marketplace repo:** `https://github.com/rinman24/claude-skills` (public)
- **Marketplace name** (the `name` field in `.claude-plugin/marketplace.json`,
  used as the `@`-suffix when installing): `claude-skills`
- **Plugin name:** `prototype`

### What the plugin does

The `prototype` skill builds throwaway code to settle one design question that
talking can't. It is model-invocable: type `/prototype`, or Claude loads it
when you ask to prototype something undecided (wayfinder will call it for
`prototype` tickets once W6 lands). It:

1. checks there is an open question first, and stops on a settled design
   (the next step is building it) or a whole-app demo (not one question);
2. for a logic question, writes one double-clickable HTML file: a pure state
   model, a labelled state panel, free-play buttons and walkthrough tabs, with
   competing models on tabs only when the question names alternatives;
3. for a UI question, writes 3–5 structurally different variants switched by
   `?variant=` and a floating bar: on an existing page (preferred), a
   throwaway route, or one `<name>.prototype.html` file when the repo has no
   web app;
4. hands the prototype over and **waits for your verdict**. It never picks a
   variant or rules a model sound itself, headless or not;
5. after the verdict, records it in one line, offers once to commit the
   prototype to a never-merged `prototype/<name>` branch, returns the current
   branch to its pre-prototype state, names the next step and stops. It never
   folds the result into the real code.

There are no hooks and no advisor calls. Adapted from `mattpocock/skills`
(MIT); see the README.

### Repo structure (for reference)

```
claude-skills/
├── .claude-plugin/marketplace.json      # catalog; name = "claude-skills"
└── plugins/prototype/
    ├── .claude-plugin/plugin.json       # no hooks
    ├── LICENSE                          # upstream MIT notice
    └── skills/prototype/
        ├── SKILL.md                     # question check, branch pick, hand-over gate, after the verdict
        ├── LOGIC.md                     # single-file logic demo
        └── UI.md                        # variants, sub-shapes A/B/C, floating switcher
```

---

## Prerequisites

```bash
which claude          # Claude Code CLI present
```

Run it inside a git repo: keeping a prototype creates a `prototype/<name>`
branch.

---

## Step A — Add the marketplace and install the plugin

```bash
claude plugin marketplace add rinman24/claude-skills
claude plugin install prototype@claude-skills --scope user
```

`--scope user` makes the plugin available across all projects. Alternatives:
`--scope project` (committed for a repo's collaborators), `--scope local`
(just this repo, just you).

If you later push changes to the repo, refresh each environment with:

```bash
claude plugin marketplace update claude-skills
```

### Trying an unmerged branch

The installed marketplace reads from GitHub's default branch. Load the plugin
straight from a working tree for one session instead:

```bash
claude --plugin-dir /path/to/claude-skills/plugins/prototype
```

In a `--plugin-dir` session, the command is namespaced: type
`/prototype:prototype …`. A bare `/prototype` didn't resolve in S11's headless
runs.

---

## Step B — Validate the manifests

```bash
claude plugin validate /path/to/claude-skills                    # whole marketplace
claude plugin validate /path/to/claude-skills/plugins/prototype  # just this plugin
```

Expect a pass with no schema or JSON errors.

---

## Step C — Verify registration

Inside a Claude Code session:

```
/plugin      → confirm "prototype" is listed AND enabled
```

`/prototype` should also appear in slash-command completion.

---

## Step D — End-to-end smoke test

Status: steps 1–3 were checked headless on the build branch (S11), via
`--plugin-dir` and `/prototype:prototype`. Rich then ran steps 1–5 and 7
interactively in `~/Code/squadra`, and all passed. Step 6 passed later (Q2,
2026-10-08) in `~/Code/scratch/site-dash`, a toy Flask app built for it.

### Setup: a branch you'll throw away

Steps 1–5 and 7 need a repo with no web app; any Python or docs repo will do
(S11 used `~/Code/squadra`). Branch off first, because step 5 commits to a new
`prototype/<name>` branch and then cleans up the branch you're on:

```bash
cd ~/Code/squadra                        # or any repo with no web app
git switch -c scratch/prototype-test
claude --plugin-dir /path/to/claude-skills/plugins/prototype   # or the installed plugin
```

With `--plugin-dir`, type `/prototype:prototype` wherever the steps below say
`/prototype`.

When you're done, in a normal terminal:

```bash
git switch main
git branch -D scratch/prototype-test prototype/<name>
```

### Run order

Steps 4, 5 and 7 continue a hand-over, so each one has to come straight after
a step 1 in the same interactive session (a headless `claude -p` run ends
after one reply).

| Session | Repo | Steps |
|---|---|---|
| 1 | No web app, on `scratch/prototype-test` | Step 1 → step 4 → step 5. Then check `git status` (clean) and `git branch` (`prototype/<name>` exists) in a normal terminal. |
| 2 | Same | Step 1 again → step 7. It has to be a new session, because step 4 already settled session 1's question. |
| 3 | Same | Steps 2 and 3, each on its own (optional; both passed headless). |
| 4 | `~/Code/scratch/site-dash` (or any Flask/Jinja app with an `APP_ENV` switch), on a throwaway branch | Step 6 on its own. |

1. In a repo with no web app, run:
   `/prototype I can't decide what the battery dispatch summary should look like for a site with solar, a 2 MWh battery and a CHP unit. Show me options.`
   Expected: one `<name>.prototype.html` file with 3 structurally different
   variants, a floating ←/→ bar and `?variant=` keys, then a `🧪 Prototype
   ready` block ending in "Which one?". No variant named as the winner, no
   verdict recorded, no branch created.
2. Run: `/prototype Does this state model hold? A microgrid site is grid-tied, islanded or in transition; it can only island from grid-tied, and it must pass through transition both ways.`
   Expected: one HTML file with the question at the top, a state panel,
   free-play buttons (an illegal move shows why it was refused) and
   walkthrough tabs; then the hand-over block, and no ruling on the model.
3. Run: `/prototype We settled the settings page layout yesterday (variant B, sidebar). Prototype it.`
   Expected: one line saying the design is settled and the next step is
   building it. No files written.
4. After step 1, answer with a mix ("B's header with C's layout"). Expected:
   a one-line `✅ Verdict` in your words, one offer to keep the prototype on
   `prototype/<name>`, and a next step for you to start. No edits outside the
   prototype file.
5. Say yes to keeping it. Expected: a `prototype/<name>` branch holding the
   prototype, and the current branch with no prototype files left.
6. In `~/Code/scratch/site-dash` (`/sites/riverside` has a battery dispatch
   summary; see its README to run it, and `APP_ENV=production` for the
   production check), or any web app with an existing page that fits, repeat
   step 1.
   Expected: sub-shape A, with variants on the existing route behind
   `?variant=`, the bar hidden in production builds, and the only change to
   the page being the switcher mount.
7. After a hand-over, ask "just pick the best one". Expected: notes on each
   variant if useful, but no pick and no verdict; the question stays open.

---

## Definition of done

- `/plugin` shows `prototype` enabled.
- Step D 1–7 behave as above.
- `git status` on the current branch shows nothing from the prototype after
  step 5; the prototype lives only on `prototype/<name>`.
