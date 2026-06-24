# my-skills

A personal [Claude Code plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces)
for distributing my own skills across repos, dev containers, and VMs from a
single source of truth.

A "marketplace" here is just this git repo plus a catalog file
(`.claude-plugin/marketplace.json`) — there is no separate hosted service.

## Install

Inside any Claude Code session (replace `YOUR_GITHUB_USERNAME/REPO`):

```
/plugin marketplace add YOUR_GITHUB_USERNAME/REPO
/plugin install handoff@my-skills
```

Or from the command line:

```
claude plugin marketplace add YOUR_GITHUB_USERNAME/REPO
claude plugin install handoff@my-skills --scope user
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
/plugin                             # confirm the handoff plugin is listed
/hooks                              # confirm the Stop hook registered
```

Update after editing: push to the repo, then
`claude plugin marketplace update my-skills` in each environment.

## Plugins

### handoff

Compacts the current conversation into `.pipeline/<slug>/handoff.md` and drops a
one-shot marker (`.pipeline/.spawn-successor`). The plugin's `Stop` hook then
spawns a fresh interactive Claude session in a new lower tmux pane, seeded with
the handoff document, to continue with a clean context window.

The hook is the **sole** spawner — the skill itself never spawns. That keeps the
model out of the spawn path entirely (it only writes a file and drops a marker,
both reliable), so exactly one successor is created and a forgotten spawn is
impossible.

Requirements: `tmux` (3.3a+), and `jq` for the hook's loop-guard (the hook
degrades gracefully without `jq`). The session must be running inside tmux for
the spawn to work.

## Troubleshooting

### The handoff runs but no new pane appears

If `/handoff` writes the document and drops the marker but no successor pane
spawns, the most common cause is that **the workspace is not trusted**. Claude
Code silently skips all hooks in untrusted workspaces — no error, nothing in the
pane. Trust the workspace (Claude Code prompts on first entry to a new
directory, or run `/permissions` / re-open the folder and accept the trust
prompt), then try again.

Other things to check, in order:

1. **Hook registered?** Run `/hooks` and confirm a `Stop` hook pointing at
   `spawn-handoff-successor.sh` is listed. If it isn't, the plugin install or
   manifest didn't load — re-run `claude plugin validate .` and reinstall. (The
   plugin manifest schema changes; valid-looking JSON has silently failed to
   load before.)
2. **Inside tmux?** The hook needs `$TMUX` set and a pane to split. If you
   launched `claude` outside tmux, the hook exits cleanly and leaves the marker
   in place. Start `claude` inside a tmux session.
3. **Marker present?** After a handoff, check `ls .pipeline/.spawn-successor`.
   If it's gone, the hook spawned successfully (it consumes the marker only on a
   successful spawn). If it's still there, the spawn didn't happen — re-check 1
   and 2.
4. **`jq` / `tmux` installed?** Missing `tmux` stops the spawn; missing `jq`
   only disables the loop-guard (the hook still works).
