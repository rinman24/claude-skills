# Runbook: Install & verify the `design-to-board` Claude Code plugin

This is a self-contained runbook. It assumes no prior context. Goal: install the
`design-to-board` plugin from a personal plugin marketplace, point it at a
squadra target repo, and confirm it writes to a real board.

---

## Background (what this is)

`design-to-board` is a Claude Code plugin distributed via a self-hosted plugin
marketplace — which is just a public GitHub repo plus a catalog file. This
runbook only covers **installing and verifying** it.

- **Marketplace repo:** `https://github.com/rinman24/claude-skills` (public)
- **Marketplace name** (the `name` field in `.claude-plugin/marketplace.json`,
  used as the `@`-suffix when installing): `claude-skills`
- **Plugin name:** `design-to-board`

### What the plugin does

The `/design-to-board` skill transcribes a cleared wayfinder design document
(`docs/design/<map>.md`) into increments on squadra's board. It never designs.
Run it in squadra's target repo, after wayfinder's Publish says the document is
cleared:

1. reads the document strictly and runs DESIGN-FORMAT's translator checks 6–15;
2. reads the board with `squadra board origins` (squadra finds its own
   `squadra.toml`; the plugin never reads it);
3. reconciles the two into a plan: withdrawals first (predecessors first), then
   queues in dependency order;
4. writes the plan through `squadra board withdraw` and `squadra board queue`,
   stopping at the first write squadra refuses. With `--dry-run` it prints the
   plan and writes nothing.

A map's first run needs `--parent <id>` (an item in squadra's claim scope);
later runs use the parent the map's items already carry. Re-running on the same
document is idempotent ("nothing to write"), and a re-run after a stop finishes
the remaining writes.

Exit codes: 0 written (or nothing to write; with `--dry-run`, the plan), 1
failed and nothing written, 2 usage, 3 stopped partway.

### Repo structure (for reference)

```
claude-skills/
├── .claude-plugin/marketplace.json               # catalog; name = "claude-skills"
└── plugins/design-to-board/
    ├── .claude-plugin/plugin.json                # no hooks
    ├── skills/design-to-board/SKILL.md           # the /design-to-board Client
    ├── scripts/                                  # stdlib-only Python 3: the transcriber
    └── tests/                                    # pytest, run with uvx
```

---

## Prerequisites

```bash
which claude python3 gh uv
squadra board --help          # squadra with the board verbs (SQ4 or later)
gh auth status                # GitHub provider: gh's own auth, `project` scope
```

`squadra` isn't a plugin dependency; install it as a uv tool from the commit you
want (a local clone may be behind `origin/main`):

```bash
uv tool install "git+https://github.com/rinman24/squadra@<sha>"
```

The target repo needs a `squadra.toml` that passes squadra's own check. For a
GitHub board, scaffold it and pass `--provider github` to the check too (the
flag defaults to `ado` and outranks the file; the check also rewrites the two
skill templates, so delete them if you don't want them):

```bash
cd <target repo>
squadra init --provider github           # then set claim_scope, parent_scope_ids, [board.github]
squadra init --check --provider github   # expect "squadra: config OK"
```

On the GitHub project, the "Item added to project" workflow must be off or set
a Status mapped to `queued` (squadra reads the Status back once after each
queue and fails loudly otherwise). Turn "Item closed" off too: otherwise a
withdrawn issue shows in the project's Done column, though squadra reads it as
withdrawn.

---

## Step A — Add the marketplace and install the plugin

```bash
claude plugin marketplace add rinman24/claude-skills
claude plugin install design-to-board@claude-skills --scope user
```

Notes:

- `design-to-board@claude-skills` = plugin `design-to-board` from the
  marketplace named `claude-skills`.
- `--scope user` makes the plugin available in every project, which is what you
  want: it runs in whichever repo is squadra's target.

If you later push changes to the repo, refresh each environment with:

```bash
claude plugin marketplace update claude-skills
claude plugin update design-to-board@claude-skills
```

---

## Step B — Validate the manifests and run the tests

```bash
claude plugin validate /path/to/claude-skills                          # whole marketplace
claude plugin validate /path/to/claude-skills/plugins/design-to-board  # just this plugin
cd /path/to/claude-skills && uvx pytest -p no:cacheprovider plugins/design-to-board/tests
```

Expect a pass with no schema or JSON errors, and every test passing. The
fake-board tests run only when a `squadra` on PATH answers
`squadra board --help`; otherwise they skip and name the reason.

---

## Step C — Verify registration

```bash
claude plugin list        # design-to-board@claude-skills, Status: enabled
```

Inside a Claude Code session, `/plugin` lists it as well, and
`/design-to-board` is the slash command. The skill is user-invoked only.

---

## Step D — End-to-end test on a real board

The acceptance documents live in this repo:
`docs/design-to-board/acceptance/sandbox-r1.md` (map `sandbox`, chain
I1 → I2 → I3) and `sandbox-r2.md` (I2 and I3 withdrawn, replaced by I4 → I1 and
I5 → I4). Use a scratch target repo with an in-scope parent issue and an empty
board. Never `squadra start` there.

1. In the target repo, run `/design-to-board <path>/sandbox-r1.md --parent <in-scope id> --dry-run`.
   Expected: 3 queues, nothing written.
2. Run it again without `--dry-run`. Expected: `queued sandbox:I1 · item …`
   and the same for I2 and I3, each naming its predecessor's item, then exit 0.
3. Re-run step 2. Expected: "nothing to write; the board already matches the
   document."
4. Run `/design-to-board <path>/sandbox-r2.md`. Expected: `withdrew
   sandbox:I2`, `withdrew sandbox:I3`, `queued sandbox:I4` (predecessor I1's
   item), `queued sandbox:I5` (predecessor I4's item).
5. `squadra tick --dry-run`. Expected last line:
   `claimable=[<I1>] states={<I1>: 'claimable', <I4>: 'blocked', <I5>: 'blocked'}`,
   with I2's and I3's items absent (neither claimable nor done) and nothing
   under an out-of-scope parent.
6. `squadra board origins`: I2 and I3 read `"lifecycle": "withdrawn"`. On
   GitHub they are closed as not planned.

To reset the scratch board for another run, delete the Origin-bearing issues
(`gh issue delete <n> -R <repo> --yes`); closing them isn't enough, since
`origins` lists closed issues too.

---

## Definition of done

- `claude plugin list` shows `design-to-board@claude-skills` enabled.
- The tests pass with `squadra` on PATH (none skipped).
- On a real board, r1 then r2 give the tick in step 5, and each re-run writes
  nothing.
