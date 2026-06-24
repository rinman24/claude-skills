# Runbook: Install & verify the `handoff` Claude Code plugin in a dev container

This is a self-contained handoff document. It assumes no prior context from the
session that produced it. Goal: install the `handoff` plugin from a personal
plugin marketplace into a dev container and verify it works end to end.

---

## Background (what this is)

`handoff` is a Claude Code plugin distributed via a self-hosted plugin
marketplace — which is just a public GitHub repo plus a catalog file. The repo
has already been built and pushed; this runbook only covers **installing and
verifying** it in a container.

- **Marketplace repo:** `https://github.com/rinman24/claude-skills` (public)
- **Marketplace name** (the `name` field in `.claude-plugin/marketplace.json`,
  used as the `@`-suffix when installing): `my-skills`
- **Plugin name:** `handoff`

### What the plugin does

The `handoff` skill compacts the current conversation into a handoff document at
`.pipeline/<slug>/handoff.md`, then drops a one-shot marker file at
`.pipeline/.spawn-successor`. A bundled `Stop` hook
(`spawn-handoff-successor.sh`) is the **sole** spawner: when the marker is
present at the end of a turn, the hook spawns a fresh `claude` session in a new
lower tmux pane (60% height), seeded with the handoff document, then removes the
marker. The skill itself never spawns — keeping the model out of the spawn path
guarantees exactly one successor and makes a forgotten spawn impossible.

### Repo structure (for reference)

```
claude-skills/
├── .claude-plugin/marketplace.json          # catalog; name = "my-skills", owner = rinman24
├── README.md                                # install + troubleshooting
└── plugins/handoff/
    ├── .claude-plugin/plugin.json           # wires the Stop hook via ${CLAUDE_PLUGIN_ROOT}
    ├── skills/handoff/SKILL.md              # write doc → drop marker (does NOT spawn)
    └── hooks/spawn-handoff-successor.sh      # Stop hook = sole spawner; portable (no GNU-only find -printf)
```

---

## Prerequisites (verify first)

Run these in the target container and confirm before proceeding:

```bash
which claude          # Claude Code CLI present
which tmux            # required — the hook splits a tmux pane to spawn
tmux -V               # expect 3.3a+ (hook uses `-l 60%`, not the removed `-p 60`)
which jq              # used by the hook's loop-guard; hook degrades gracefully without it
echo "$TMUX"          # MUST be non-empty — the hook only spawns when inside tmux
```

If `$TMUX` is empty, start/attach a tmux session and launch `claude` **inside
it**, otherwise the spawn cannot work. The intended launch pattern is
`claude --dangerously-skip-permissions` running inside a tmux pane.

> CLI flags and the plugin manifest schema change over time. If any command
> below is rejected, check `claude plugin --help`, `claude plugin install --help`,
> and the current docs at https://code.claude.com/docs/en/plugin-marketplaces
> before improvising.

---

## Step A — Add the marketplace and install the plugin

```bash
claude plugin marketplace add rinman24/claude-skills
claude plugin install handoff@my-skills --scope user
```

Notes:
- `handoff@my-skills` = plugin `handoff` from the marketplace named `my-skills`.
  The `@` suffix is the marketplace **name** field, not the repo name.
- `--scope user` makes the plugin available across all projects in this
  container (right choice for per-container setup). Alternatives: `--scope
  project` (committed for a repo's collaborators), `--scope local` (just this
  repo, just you).
- The plugin source is cloned into the local cache at
  `~/.claude/plugins/cache`.

If you later push changes to the repo, refresh each environment with:

```bash
claude plugin marketplace update my-skills
```

---

## Step B — Validate the manifests

`claude plugin validate` checks schema/JSON validity. Point it at a local clone
of the repo (or the cached copy):

```bash
# Against the whole marketplace (checks marketplace.json + referenced plugins):
claude plugin validate /path/to/claude-skills

# Against just the plugin directory (checks plugin.json + its skill/hook files):
claude plugin validate /path/to/claude-skills/plugins/handoff
```

Expect a pass with no schema or JSON errors.

---

## Step C — Verify registration (do not skip `/hooks`)

Inside a Claude Code session in the container:

```
/plugin      → confirm "handoff" is listed AND enabled
/hooks       → confirm a Stop hook pointing at spawn-handoff-successor.sh is registered
```

**The `/hooks` check is the critical one.** A valid-looking plugin manifest has
silently failed to register its hook before. If the skill shows under `/plugin`
but no Stop hook appears under `/hooks`, the plugin loaded but the hook did not —
treat that as a failure and see Troubleshooting.

---

## Step D — End-to-end smoke test

1. Start `claude` inside a tmux session in a workspace (a throwaway test repo is
   fine). Make sure the workspace is **trusted** (see Troubleshooting).
2. In the session, run the handoff skill — e.g. invoke `/handoff` (optionally
   with a follow-up task as an argument to confirm it gets written into the doc
   for the successor rather than executed in-session).
3. Let the turn end. Expected result:
   - A handoff document appears at `.pipeline/<slug>/handoff.md`.
   - A new tmux pane opens below (≈60% height) running a fresh `claude` session,
     seeded to read the handoff doc and continue.
   - **Exactly one** new pane — never two.
   - The marker is gone: `ls .pipeline/.spawn-successor` → no such file (the
     hook consumes it only on a successful spawn).

If the marker still exists afterward, the hook did not spawn — see
Troubleshooting.

---

## Troubleshooting (in priority order)

1. **Workspace not trusted.** Claude Code silently skips ALL hooks in untrusted
   workspaces — no error, nothing in the pane. This is the most common cause of
   "handoff ran but no pane appeared." Trust the workspace (Claude Code prompts
   on first entry to a new directory; or re-open the folder / check
   `/permissions` and accept the trust prompt), then retry.
2. **Hook not registered.** If `/hooks` doesn't list the Stop hook, the manifest
   didn't load its hook. Re-run `claude plugin validate` against the plugin dir,
   reinstall, and re-check `/hooks`.
3. **Not inside tmux.** The hook needs `$TMUX` set and a pane to split. If
   `claude` was launched outside tmux, the hook exits cleanly and leaves the
   marker in place. Relaunch inside tmux.
4. **Marker present after a handoff.** Means the spawn didn't happen — re-check
   items 1–3. (Marker absent = spawn succeeded.)
5. **Missing tools.** No `tmux` → no spawn. No `jq` → only the loop-guard is
   disabled; the hook still works.

---

## Definition of done

- `/plugin` shows `handoff` enabled.
- `/hooks` shows the Stop hook → `spawn-handoff-successor.sh`.
- Smoke test spawns exactly one fresh tmux pane seeded with the handoff doc, and
  the marker is consumed.

---

## After this works

- **Retire the old skill.** There is a pre-plugin copy at
  `~/.claude/skills/handoff` that should be removed once the plugin is confirmed
  working, so two handoff implementations don't compete.
- **Expand the marketplace toward the `flotilla` skill namespace.** The longer-
  term goal is a public reference implementation of a skill namespace
  (`/tdd`, `/to-qa`, `/prototype`, `/research`, …) that the `flotilla` PyPI
  package depends on by *name/contract* (not by content). Skills would be added
  as additional `plugins/<plugin>/skills/<name>/SKILL.md` folders. The package
  must only verify the skill *names* resolve, never assume these specific
  implementations — users are expected to customize freely. NOTE: how a Python
  process can programmatically detect which skills/plugins are installed in a
  Claude Code environment is not yet confirmed against current docs; verify that
  surface exists before building any runtime verification on it.
