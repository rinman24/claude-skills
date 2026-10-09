# Runbook: Install & verify the `grilling` Claude Code plugin

This is a self-contained runbook. It assumes no prior context. Goal: install the
`grilling` plugin from a personal plugin marketplace into a repo or dev
container and confirm it works.

---

## Background (what this is)

`grilling` is a Claude Code plugin distributed via a self-hosted plugin
marketplace — which is just a public GitHub repo plus a catalog file.

- **Marketplace repo:** `https://github.com/rinman24/claude-skills` (public)
- **Marketplace name** (the `name` field in `.claude-plugin/marketplace.json`,
  used as the `@`-suffix when installing): `claude-skills`
- **Plugin name:** `grilling`

### What the plugin does

The `grilling` skill interviews you about a plan, decision, or idea until you
and Claude share an understanding of it. It is model-invocable: type
`/grilling`, or Claude loads it itself when you ask to be grilled. It:

1. maps the subject as a design tree and asks in rounds — each round is every
   question whose prerequisites are settled, numbered, each with a short "why
   now" and a `➡️` recommended answer;
2. lets you ask what a question means instead of answering it;
3. looks facts up itself with read-only sub-agents and puts only decisions to
   you;
4. ends with a numbered decision summary and waits for your explicit
   confirmation.

It never writes code or edits files. There are no hooks and no external
dependencies. Adapted from `mattpocock/skills` (MIT); see the README.

### Repo structure (for reference)

```
claude-skills/
├── .claude-plugin/marketplace.json               # catalog; name = "claude-skills"
└── plugins/grilling/
    ├── .claude-plugin/plugin.json                # no hooks
    ├── LICENSE                                   # upstream MIT notice
    └── skills/grilling/SKILL.md                  # the interview procedure
```

---

## Prerequisites

```bash
which claude          # Claude Code CLI present
```

No other tools are required, and it does not need a git repo.

---

## Step A — Add the marketplace and install the plugin

```bash
claude plugin marketplace add rinman24/claude-skills
claude plugin install grilling@claude-skills --scope user
```

Notes:

- `grilling@claude-skills` = plugin `grilling` from the marketplace named
  `claude-skills`. The `@` suffix is the marketplace **name** field in
  `marketplace.json`; it matches the repo name by convention, but the two are
  set independently.
- `--scope user` makes the plugin available across all projects. Alternatives:
  `--scope project` (committed for a repo's collaborators), `--scope local`
  (just this repo, just you).

If you later push changes to the repo, refresh each environment with:

```bash
claude plugin marketplace update claude-skills
```

### Trying an unmerged branch

The installed marketplace reads from GitHub's default branch, so changes on a
branch don't show up through it. Load the plugin straight from a working tree
for one session instead:

```bash
claude --plugin-dir /path/to/claude-skills/plugins/grilling
```

---

## Step B — Validate the manifests

```bash
claude plugin validate /path/to/claude-skills                   # whole marketplace
claude plugin validate /path/to/claude-skills/plugins/grilling  # just this plugin
```

Expect a pass with no schema or JSON errors.

---

## Step C — Verify registration

Inside a Claude Code session:

```
/plugin      → confirm "grilling" is listed AND enabled
```

`/grilling` should also appear in slash-command completion.

---

## Step D — End-to-end smoke test

1. Start `claude` in any directory.
2. Run `/grilling should I add a cache in front of our pricing API?`
3. Expected result:
   - The first round arrives as numbered `❓ **Q1** - **…**` questions separated
     by `---`, each a few lines long with a `➡️` recommendation that answers the
     question as worded.
   - No question in the round depends on another one in the same round.
   - Claude reads files or dispatches a sub-agent rather than asking you
     anything it could look up.
4. Reply to one question with "Q1?" and answer the rest. Claude should
   re-explain Q1 with a concrete example and keep it open; the others are
   settled.
5. Tell it "go ahead and write the cache". It should say that ends the
   grilling and stop, without writing code.
6. In a fresh session, grill to the end. It should post a numbered decision
   summary and wait for your confirmation, then hand back without building.

---

## Definition of done

- `/plugin` shows `grilling` enabled.
- The smoke test shows round format, clarification, and the confirmation gate
  working as above.
- No file in the working directory changed during the session (`git status` is
  clean if you ran it in a repo).

## After it works

Delete the older claude.ai-synced `grill-me` skill (one question at a time,
no confirmation gate) from claude.ai so the two don't compete for "grill me"
triggers.
