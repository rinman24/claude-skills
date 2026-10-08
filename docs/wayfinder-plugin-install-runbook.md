# Runbook: Install & verify the `wayfinder` Claude Code plugin

This is a self-contained runbook. It assumes no prior context. Goal: install the
`wayfinder` plugin from a personal plugin marketplace into a repo or dev
container and confirm it works.

---

## Background (what this is)

`wayfinder` is a Claude Code plugin distributed via a self-hosted plugin
marketplace — which is just a public GitHub repo plus a catalog file.

- **Marketplace repo:** `https://github.com/rinman24/claude-skills` (public)
- **Marketplace name** (the `name` field in `.claude-plugin/marketplace.json`,
  used as the `@`-suffix when installing): `claude-skills`
- **Plugin name:** `wayfinder`

### What the plugin does

The `wayfinder` skill charts the way to one destination that is too big for a
single session. It is user-invoked only: type `/wayfinder`. It:

1. **Begin**: settles the destination and its behaviours with `grilling` and
   `domain-modeling`, surveys the frontier breadth-first, and writes a map
   (`.scratch/wayfinder/<map>/map.md` plus one file per ticket). It resolves
   nothing.
2. **Resolve**: takes one ticket per session (the one you name, or the first
   on the frontier), marks it `in progress`, resolves it by its kind, records
   the Resolution and a line in Decisions so far, and graduates any fog the
   answer made precise.
3. **Revise**: only when you say a closed decision changed. It marks the
   ticket `revised`, opens a replacement, flags dependents, has
   `domain-modeling` reopen terms settled from that ticket, and sets a
   published design document to `revising`.
4. **Publish**: runs the design document's checks and writes
   `docs/design/<map>.md` with `status: cleared`.

It writes only the map and the design document; glossary files are written by
`domain-modeling` under its own rules. It never builds and never touches
squadra's board or any issue tracker. There are no hooks. Adapted from
`mattpocock/skills` (MIT); see the README.

### Repo structure (for reference)

```
claude-skills/
├── .claude-plugin/marketplace.json                  # catalog; name = "claude-skills"
└── plugins/wayfinder/
    ├── .claude-plugin/plugin.json                   # no hooks
    ├── LICENSE                                      # upstream MIT notice
    ├── GLOSSARY.md                                  # the Wayfinder context's language
    └── skills/wayfinder/
        ├── SKILL.md                                 # Chart: Begin / Resolve / Revise / Publish
        ├── MAP-FORMAT.md                            # map.md and ticket files
        └── DESIGN-FORMAT.md                         # design document contract and checks
```

---

## Prerequisites

```bash
which claude          # Claude Code CLI present
claude plugin install grilling@claude-skills --scope user
claude plugin install domain-modeling@claude-skills --scope user
```

- `grilling` and `domain-modeling` resolve every grilling ticket and the
  Begin conversation. Without `domain-modeling` there are no glossary writes.
- `board-eric` (needed by `domain-modeling` for writes) and `board-juval`
  (optional decomposition consult) ship with Rich's `~/Code/board` setup.
  Check with `/agents` inside a session.
- Run it inside a git repo: the map and design document are committed files.

---

## Step A — Add the marketplace and install the plugin

```bash
claude plugin marketplace add rinman24/claude-skills
claude plugin install wayfinder@claude-skills --scope user
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
claude --plugin-dir /path/to/claude-skills/plugins/wayfinder
```

---

## Step B — Validate the manifests

```bash
claude plugin validate /path/to/claude-skills                    # whole marketplace
claude plugin validate /path/to/claude-skills/plugins/wayfinder  # just this plugin
```

Expect a pass with no schema or JSON errors.

---

## Step C — Verify registration

Inside a Claude Code session:

```
/plugin      → confirm "wayfinder" is listed AND enabled
```

`/wayfinder` should also appear in slash-command completion.

---

## Step D — End-to-end smoke test

Use a scratch git repo (or a branch you'll throw away). Steps 1, 2, 3 and 5 passed
headless on the build branch (W4, S10; step 2 after the WD-B12 fix); steps 4,
6 and 7 need a second turn, so run them interactively.

1. Run `/wayfinder <a loose idea too big for one session>`. Expected: it loads
   `grilling` and `domain-modeling` and asks about the destination first.
   After you answer, it writes `.scratch/wayfinder/<map>/map.md` (Destination
   with `B1`…, Increments, empty Decisions so far, Fog) and ticket files, each
   with `Kind`, `Status: open` and `Unblocks:`. It resolves nothing and stops.
2. Run `/wayfinder` with an idea small enough for one session (e.g. "define a
   Python dataclass `Person` with `name: str` and `age: int`"). Expected: before
   any grilling round, it says no map is needed and asks how to proceed;
   nothing is written.
3. Run `/wayfinder <map>`. Expected: it takes the first frontier ticket, sets
   `Status: in progress` first, resolves it by its kind, then sets `closed`
   with a Resolution and adds one line to Decisions so far. One ticket only.
4. Start a second Resolve on the same map while a ticket is `in progress`.
   Expected: it stops and asks whether the other session is still going.
5. With every decision ticket closed and Fog empty, say "publish <map>".
   Expected: `docs/design/<map>.md` with `format: wayfinder-design/1`,
   `status: cleared`, `revision: 1`, and `Decided by` refs that all appear in
   Decisions. With a check failing, it names the failure and writes nothing.
6. Say "revise <ticket>: <what changed>". Expected: the ticket becomes
   `revised` with a `## Revised` section, a replacement ticket links back, its
   Decisions line points at the replacement, and the design document's status
   becomes `revising` with nothing else changed.
7. At any point, ask it to "just build" an increment. Expected: it declines;
   it writes nothing outside the map and the design document.

---

## Definition of done

- `/plugin` shows `wayfinder` enabled.
- Step D 1–7 behave as above.
- `git status` shows only files under `.scratch/wayfinder/`, `docs/design/`,
  and any glossary files `domain-modeling` wrote.
