# claude-skills

A personal [Claude Code plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces)
for distributing my own skills across repos, dev containers, and VMs from a
single source of truth.

A "marketplace" here is just this git repo plus a catalog file
(`.claude-plugin/marketplace.json`) — there is no separate hosted service.

## Install

Inside any Claude Code session (replace `rinman24/claude-skills`):

```
/plugin marketplace add rinman24/claude-skills
/plugin install local-backlog@claude-skills
```

Or from the command line:

```
claude plugin marketplace add rinman24/claude-skills
claude plugin install local-backlog@claude-skills --scope user
```

### Scope

- `--scope user` — available to you across all projects in this Claude Code
  install (recommended for a personal dev container).
- `--scope project` — committed for all collaborators on a repo.
- `--scope local` — just you, just this repo.

CLI flags change; confirm with `claude plugin install --help` if `--scope` is
not accepted.

### Verify

```
claude plugin validate .            # validate the whole marketplace
/plugin                             # confirm the plugin is listed and enabled
```

Update after editing: push to the repo, then
`claude plugin marketplace update claude-skills` in each environment.

## Plugins

### local-backlog

Sets up a personal, git-excluded backlog in the current repo. Invoke
`/local-backlog` once per repo and it will:

- create `BACKLOG.local.md` at the repo root (dated items, `(P1)`/`(P2)`/`(P3)`
  priorities, `## Open` / `## Done`), with the "promote real work to …" line
  pointed at the repo's tracker (Azure DevOps / GitHub / GitLab, auto-detected
  from the `origin` remote);
- write a `## Local backlog` section into `CLAUDE.local.md` so future sessions
  keep announcing changes, dating items, and sorting by priority — the part a
  one-shot skill can't do on its own;
- add `/BACKLOG.local.md` and `/CLAUDE.local.md` to `.git/info/exclude` (the
  *local* exclude — never the shared, tracked `.gitignore`).

It is idempotent and never overwrites an existing backlog. It has no hooks and
only reads/writes files. See
[docs/local-backlog-plugin-install-runbook.md](docs/local-backlog-plugin-install-runbook.md).

### grilling

A relentless interview that stress-tests a plan, decision, or idea before
anyone acts on it. Type `/grilling`, or Claude reaches for it on its own when
you ask to be grilled. It:

- maps the subject as a design tree and asks it in rounds: each round is every
  question whose prerequisites are settled, numbered, each with a short "why
  now" and a recommended answer you can accept by number;
- lets you ask what a question means instead of answering it, and re-explains
  it with a concrete example;
- looks facts up itself (read-only sub-agents) and puts only decisions to you;
- ends with a numbered decision summary and waits for your confirmation.

It never writes code or edits files, during the session or after it; building
is a separate step you start. Install with
`claude plugin install grilling@claude-skills --scope user`. See
[docs/grilling-plugin-install-runbook.md](docs/grilling-plugin-install-runbook.md).

Adapted from `grilling` in [mattpocock/skills](https://github.com/mattpocock/skills)
(commit `6fd9479`), MIT, Copyright (c) 2026 Matt Pocock; the upstream license is
in [plugins/grilling/LICENSE](plugins/grilling/LICENSE). Changes from upstream:
shorter questions with a "why now" line, recommendations that answer the
question as worded, a clarification path, a scope-split prompt for oversized
rounds, a decision summary at the gate, and a hard no-code rule.

### domain-modeling

Builds and sharpens a repo's domain language while you design. Type
`/domain-modeling`, or Claude loads it when terminology, `GLOSSARY.md` or a
naming question comes up. It:

- challenges terms that conflict with `GLOSSARY.md`, sharpens fuzzy ones,
  stress-tests boundaries with scenarios, and checks claims against the code;
- writes each term to `GLOSSARY.md` the moment it is settled and announces the
  write at the top of the next round, so you review every one;
- records each ruling in `GLOSSARY-SETTLED.md` (never pruned, never deleted),
  looks it up before asking any naming question, reports drift from it without
  reopening it, and reopens a ruling only when you say so;
- guards against bloat: a "term or spec?" test on every write, and a proposed
  pruning pass past about 40 terms or 150 lines;
- bootstraps a glossary for an existing codebase one module at a time, with
  read-only extractor sub-agents and your review of each slice;
- hands ADR-worthy decisions to the `adr` skill if it is installed.

Every glossary write, settlement and pruning pass is reviewed first by Eric
Evans via the `board-eric` agent from Rich's board of advisors. Where
`board-eric` isn't available, the skill still challenges and looks things up,
but writes nothing. Install with
`claude plugin install domain-modeling@claude-skills --scope user`. See
[docs/domain-modeling-plugin-install-runbook.md](docs/domain-modeling-plugin-install-runbook.md).

Adapted from `domain-modeling` in
[mattpocock/skills](https://github.com/mattpocock/skills) (commit `6fd9479`),
MIT, Copyright (c) 2026 Matt Pocock; the upstream license is in
[plugins/domain-modeling/LICENSE](plugins/domain-modeling/LICENSE). Changes from
upstream: the settled-term record and its operations, Eric's review of every
write, write announcements, the bloat guard, the brownfield bootstrap, and ADRs
moved out to a separate `adr` plugin.
