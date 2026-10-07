# Runbook: Install & verify the `adr` Claude Code plugin

This is a self-contained runbook. It assumes no prior context. Goal: install the
`adr` plugin from a personal plugin marketplace into a repo or dev container and
confirm it works.

---

## Background (what this is)

`adr` is a Claude Code plugin distributed via a self-hosted plugin
marketplace — which is just a public GitHub repo plus a catalog file.

- **Marketplace repo:** `https://github.com/rinman24/claude-skills` (public)
- **Marketplace name** (the `name` field in `.claude-plugin/marketplace.json`,
  used as the `@`-suffix when installing): `claude-skills`
- **Plugin name:** `adr`

### What the plugin does

The `adr` skill records architecture decisions, sparingly. It is
model-invocable: type `/adr`, or Claude loads it when you ask to record a
decision, and `domain-modeling` calls it when a decision looks ADR-worthy. It:

1. writes an ADR only when the decision is hard to reverse, surprising without
   context, and the result of a real trade-off; otherwise it writes nothing and
   names each failed gate with a reason;
2. follows the repo's existing ADR convention (location, numbering, template,
   status vocabulary, index file) if it finds one, and otherwise writes a
   one-paragraph `docs/adr/NNNN-slug.md`, creating `docs/adr/` on first use;
3. writes straight away when you asked for the ADR, but only offers it (and
   waits for your yes) when another skill or Claude raised it.

There are no hooks and no advisor calls. Adapted from `mattpocock/skills`
(MIT); see the README.

### Repo structure (for reference)

```
claude-skills/
├── .claude-plugin/marketplace.json      # catalog; name = "claude-skills"
└── plugins/adr/
    ├── .claude-plugin/plugin.json       # no hooks
    ├── LICENSE                          # upstream MIT notice
    └── skills/adr/
        ├── SKILL.md                     # gates, write-or-offer, convention detection
        └── ADR-FORMAT.md                # default docs/adr/ convention and template
```

---

## Prerequisites

```bash
which claude          # Claude Code CLI present
```

Run it inside a git repo: the default location is `docs/adr/` at the repo root.

---

## Step A — Add the marketplace and install the plugin

```bash
claude plugin marketplace add rinman24/claude-skills
claude plugin install adr@claude-skills --scope user
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
claude --plugin-dir /path/to/claude-skills/plugins/adr
```

---

## Step B — Validate the manifests

```bash
claude plugin validate /path/to/claude-skills              # whole marketplace
claude plugin validate /path/to/claude-skills/plugins/adr  # just this plugin
```

Expect a pass with no schema or JSON errors.

---

## Step C — Verify registration

Inside a Claude Code session:

```
/plugin      → confirm "adr" is listed AND enabled
```

`/adr` should also appear in slash-command completion.

---

## Step D — End-to-end smoke test

Use a scratch git repo (or a branch you'll throw away). Steps 1–2 were checked
headless on the build branch (S5); steps 3–5 need a second turn or a prepared
repo, so run them interactively.

1. In a repo with no ADRs, run:
   `/adr Record this decision: we use Postgres, not DynamoDB, for the event store. We weighed DynamoDB's scaling against Postgres's transactions and picked transactions. Migrating later means rewriting the storage layer, and readers will expect DynamoDB since everything else is on AWS.`
   Expected: `docs/adr/0001-<slug>.md` with a title heading and one paragraph,
   and a single `📝 Written:` line naming the file.
2. Run: `/adr Record this decision: the runbook uses numbered steps instead of bullets. Nobody suggested anything else.`
   Expected: no file written, and a reply naming each failed gate (here all
   three) with a one-line reason.
3. In a repo that already has ADRs elsewhere (e.g. `docs/decisions/ADR-007-foo.md`
   with `Status` / `Context` / `Decision` / `Consequences` headings), repeat
   step 1. Expected: `docs/decisions/ADR-008-<slug>.md` in the house template,
   each section short; no `docs/adr/` created. If an index file lists the
   ADRs, it gains a line.
4. Give a decision with no word on alternatives (e.g. "Record that we deploy
   to Fly.io"). Expected: one question about whether there was a real
   alternative, not a guess either way.
5. With `domain-modeling` also installed, settle a hard-to-reverse
   architectural choice during a `/domain-modeling` session. Expected: it calls
   `adr`, which offers the ADR in one line and writes only after you say yes.

---

## Definition of done

- `/plugin` shows `adr` enabled.
- Step D 1–5 behave as above.
- `git status` shows only the new ADR file (and an updated index file in step 3
  if the repo has one).
