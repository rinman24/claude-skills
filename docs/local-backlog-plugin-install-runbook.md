# Runbook: Install & verify the `local-backlog` Claude Code plugin

This is a self-contained runbook. It assumes no prior context. Goal: install the
`local-backlog` plugin from a personal plugin marketplace into a repo or dev
container and confirm it works.

---

## Background (what this is)

`local-backlog` is a Claude Code plugin distributed via a self-hosted plugin
marketplace — which is just a public GitHub repo plus a catalog file. The repo
has already been built and pushed; this runbook only covers **installing and
verifying** it.

- **Marketplace repo:** `https://github.com/rinman24/claude-skills` (public)
- **Marketplace name** (the `name` field in `.claude-plugin/marketplace.json`,
  used as the `@`-suffix when installing): `claude-skills`
- **Plugin name:** `local-backlog`

### What the plugin does

The `/local-backlog` skill sets up a personal, git-excluded backlog in the
current repo. Invoked once per repo, it:

1. creates `BACKLOG.local.md` at the repo root (the backlog itself — dated
   items, `(P1)`/`(P2)`/`(P3)` priorities, `## Open` / `## Done`), with the
   "promote real work to …" line pointed at the repo's tracker (Azure DevOps /
   GitHub / GitLab, auto-detected from the `origin` remote);
2. writes a `## Local backlog` section into `CLAUDE.local.md` — the standing
   instruction that makes *future* sessions maintain the backlog (announce
   changes, date items, keep it sorted). A skill runs once; this section is what
   persists the behaviour;
3. adds `/BACKLOG.local.md` and `/CLAUDE.local.md` to `.git/info/exclude` (the
   **local** exclude — never the shared, tracked `.gitignore`).

It is idempotent (re-running only adds what's missing) and never overwrites an
existing backlog. There are no hooks and no external dependencies — it only
reads and writes files.

### Repo structure (for reference)

```
claude-skills/
├── .claude-plugin/marketplace.json               # catalog; name = "claude-skills"
└── plugins/local-backlog/
    ├── .claude-plugin/plugin.json                # no hooks — pure file scaffolder
    └── skills/local-backlog/SKILL.md             # the /local-backlog procedure
```

---

## Prerequisites

```bash
which claude          # Claude Code CLI present
git rev-parse --show-toplevel   # run /local-backlog inside a git working tree
```

The skill relies on `.git/info/exclude`, so it must be run inside a git repo.
No other tools are required.

---

## Step A — Add the marketplace and install the plugin

```bash
claude plugin marketplace add rinman24/claude-skills
claude plugin install local-backlog@claude-skills --scope user
```

Notes:

- `local-backlog@claude-skills` = plugin `local-backlog` from the marketplace
  named `claude-skills`. The `@` suffix is the marketplace **name** field in
  `marketplace.json`; it matches the repo name by convention, but the two are
  set independently.
- `--scope user` makes the plugin available across all projects in this
  container (right choice for a personal dev container). Alternatives:
  `--scope project` (committed for a repo's collaborators), `--scope local`
  (just this repo, just you).

If you later push changes to the repo, refresh each environment with:

```bash
claude plugin marketplace update claude-skills
```

---

## Step B — Validate the manifests

```bash
claude plugin validate /path/to/claude-skills                     # whole marketplace
claude plugin validate /path/to/claude-skills/plugins/local-backlog   # just this plugin
```

Expect a pass with no schema or JSON errors.

---

## Step C — Verify registration

Inside a Claude Code session:

```
/plugin      → confirm "local-backlog" is listed AND enabled
```

There is no hook to check, so `/plugin` is the only
registration surface.

---

## Step D — End-to-end smoke test

1. Start `claude` in a throwaway git repo (a fresh `git init` directory is fine).
2. Run `/local-backlog`.
3. Expected result:
   - `BACKLOG.local.md` appears at the repo root with the standard header and
     empty `## Open` / `## Done` sections.
   - `CLAUDE.local.md` contains a `## Local backlog` section.
   - `.git/info/exclude` lists `/BACKLOG.local.md` and `/CLAUDE.local.md`.
   - `git status` shows **no** new tracked/untracked files for either file (they
     are excluded).
   - Claude announces exactly what it created.
4. Re-run `/local-backlog`. It should report the backlog already exists and
   change nothing (idempotent, no clobber).

---

## Definition of done

- `/plugin` shows `local-backlog` enabled.
- A fresh repo smoke test creates the three artifacts above, and `git status`
  confirms both files are locally excluded.
- Re-running the skill is a no-op that preserves the existing backlog.
