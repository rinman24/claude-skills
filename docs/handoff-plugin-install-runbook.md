# Runbook: Install & verify the `handoff` Claude Code plugin

This is a self-contained runbook. It assumes no prior context. Goal: install the
`handoff` plugin from a personal plugin marketplace into a repo or dev container
and confirm it works.

---

## Background (what this is)

`handoff` is a Claude Code plugin distributed via a self-hosted plugin
marketplace — which is just a public GitHub repo plus a catalog file.

- **Marketplace repo:** `https://github.com/rinman24/claude-skills` (public)
- **Marketplace name** (the `name` field in `.claude-plugin/marketplace.json`,
  used as the `@`-suffix when installing): `claude-skills`
- **Plugin name:** `handoff`

### What the plugin does

The `/handoff` skill compacts the current session into a document a fresh
agent session can pick up. It is user-invoked only; an optional argument says
what the next session is for. It:

1. finds the effort's `LEDGER.md` (the committed record: status, decisions,
   the user's queue, a session log), if there is one;
2. resolves the location and template in one rule: with a ledger, the file goes
   to a git-ignored `handoffs/` beside it and uses `HANDOFF-TEMPLATE.md` beside
   it if present, else the bundled `TEMPLATE.md`; with no ledger, it goes to
   `$TMPDIR` with the bundled template;
3. checks the ledger alone could start the next unit, and offers to fix any
   gaps before writing (it edits the ledger only after a yes);
4. writes the handoff, referencing the ledger, specs, ADRs, PRs and commits by
   path or URL instead of copying them, naming suggested skills, and redacting
   secrets and personal data;
5. records the handoff's path in the ledger's session log, its only unasked
   ledger edit, and never commits.

There are no hooks and no advisor calls. The decisions behind it are HD1–HD3 in
`docs/handoff-skill/LEDGER.md`.

### Repo structure (for reference)

```
claude-skills/
├── .claude-plugin/marketplace.json      # catalog; name = "claude-skills"
├── .gitignore                           # ignores docs/*/handoffs/
└── plugins/handoff/
    ├── .claude-plugin/plugin.json       # no hooks
    └── skills/handoff/
        ├── SKILL.md                     # ledger check, location rule, write, record
        └── TEMPLATE.md                  # default handoff template
```

---

## Prerequisites

```bash
which claude          # Claude Code CLI present
```

A repo whose efforts keep a ledger at `docs/<effort>/LEDGER.md` gets the full
behaviour; anywhere else the handoff goes to `$TMPDIR`. The repo must ignore
`docs/*/handoffs/` (or the skill offers to add it).

---

## Step A — Add the marketplace and install the plugin

```bash
claude plugin marketplace add rinman24/claude-skills
claude plugin install handoff@claude-skills --scope user
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
claude --plugin-dir /path/to/claude-skills/plugins/handoff
```

---

## Step B — Validate the manifests

```bash
claude plugin validate /path/to/claude-skills                  # whole marketplace
claude plugin validate /path/to/claude-skills/plugins/handoff  # just this plugin
```

Expect a pass with no schema or JSON errors.

---

## Step C — Verify registration

Inside a Claude Code session:

```
/plugin      → confirm "handoff" is listed AND enabled
```

`/handoff` should appear in slash-command completion with the hint "What will
the next session be used for?". Claude should not load it unprompted.

---

## Step D — End-to-end smoke test

1. In a scratch directory with no ledger, have a short conversation, then run
   `/handoff`. Expected: a `handoff-<date>-<slug>.md` in `$TMPDIR` built from
   the bundled template, and a reply naming its path.
2. In a repo with `docs/<effort>/LEDGER.md` that has a session log and an
   up-to-date next work item, run `/handoff`. Expected: the file lands in
   `docs/<effort>/handoffs/`, named by the ledger's numbering; the session log
   row gains its path; `git status` shows the ledger change but not the handoff.
3. Add `docs/<effort>/HANDOFF-TEMPLATE.md` with an extra section and repeat.
   Expected: the handoff follows that template, not the bundled one.
4. Make the ledger stale (e.g. leave this session's unit `in progress` with no
   next work item) and run `/handoff`. Expected: it lists the gaps and offers to
   fix the ledger before writing; it changes nothing until you say yes.
5. Paste a fake token (e.g. `ghp_EXAMPLE0000`) into the conversation first.
   Expected: the handoff says something was redacted and doesn't contain it.

---

## Definition of done

- `/plugin` shows `handoff` enabled.
- Step D 1–5 behave as above.
- No handoff file is ever staged or committed.
