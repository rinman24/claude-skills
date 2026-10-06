# my-skills

A personal [Claude Code plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces)
for distributing my own skills across repos, dev containers, and VMs from a
single source of truth.

A "marketplace" here is just this git repo plus a catalog file
(`.claude-plugin/marketplace.json`) — there is no separate hosted service.

## Install

Inside any Claude Code session (replace `rinman24/claude-skills`):

```
/plugin marketplace add rinman24/claude-skills
/plugin install local-backlog@my-skills
```

Or from the command line:

```
claude plugin marketplace add rinman24/claude-skills
claude plugin install local-backlog@my-skills --scope user
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
`claude plugin marketplace update my-skills` in each environment.

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
