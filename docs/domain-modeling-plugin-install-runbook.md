# Runbook: Install & verify the `domain-modeling` Claude Code plugin

This is a self-contained runbook. It assumes no prior context. Goal: install the
`domain-modeling` plugin from a personal plugin marketplace into a repo or dev
container and confirm it works.

---

## Background (what this is)

`domain-modeling` is a Claude Code plugin distributed via a self-hosted plugin
marketplace — which is just a public GitHub repo plus a catalog file.

- **Marketplace repo:** `https://github.com/rinman24/claude-skills` (public)
- **Marketplace name** (the `name` field in `.claude-plugin/marketplace.json`,
  used as the `@`-suffix when installing): `claude-skills`
- **Plugin name:** `domain-modeling`

### What the plugin does

The `domain-modeling` skill builds and sharpens a repo's domain language while
you design. It is model-invocable: type `/domain-modeling`, or Claude loads it
when terminology or `GLOSSARY.md` comes up. It:

1. challenges terms that conflict with `GLOSSARY.md`, sharpens fuzzy ones,
   stress-tests boundaries with scenarios, and checks claims against the code;
2. writes each settled term to `GLOSSARY.md` and a ruling row to
   `GLOSSARY-SETTLED.md` straight away, and announces the writes at the top of
   its next reply;
3. looks up the settled record before asking any naming question, reports
   drift from a ruling without reopening it, and reopens only when you say so;
4. proposes a pruning pass when `GLOSSARY.md` passes about 40 terms or 150
   lines (the settled record is never pruned);
5. bootstraps a glossary for an existing codebase one module at a time;
6. hands ADR-worthy decisions to the `adr` skill if that plugin is installed.

Every glossary write, settlement and pruning pass is reviewed first by the
`board-eric` agent (Eric Evans, from Rich's board of advisors). Without it, the
skill still challenges and looks things up but writes nothing. There are no
hooks. Adapted from `mattpocock/skills` (MIT); see the README.

### Repo structure (for reference)

```
claude-skills/
├── .claude-plugin/marketplace.json                  # catalog; name = "claude-skills"
└── plugins/domain-modeling/
    ├── .claude-plugin/plugin.json                   # no hooks
    ├── LICENSE                                      # upstream MIT notice
    └── skills/domain-modeling/
        ├── SKILL.md                                 # the procedure
        ├── GLOSSARY-FORMAT.md                       # GLOSSARY.md / GLOSSARY-MAP.md format, bloat guard
        ├── SETTLED-FORMAT.md                        # GLOSSARY-SETTLED.md format; Settle / Lookup / Reopen
        └── BOOTSTRAP.md                             # existing-codebase bootstrap
```

---

## Prerequisites

```bash
which claude          # Claude Code CLI present
```

- The `board-eric` agent must be installed for any writes (it ships with Rich's
  `~/Code/board` setup). Check with `/agents` inside a session.
- Run it inside a git repo: the glossary files are written at the repo root.

---

## Step A — Add the marketplace and install the plugin

```bash
claude plugin marketplace add rinman24/claude-skills
claude plugin install domain-modeling@claude-skills --scope user
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
claude --plugin-dir /path/to/claude-skills/plugins/domain-modeling
```

---

## Step B — Validate the manifests

```bash
claude plugin validate /path/to/claude-skills                          # whole marketplace
claude plugin validate /path/to/claude-skills/plugins/domain-modeling  # just this plugin
```

Expect a pass with no schema or JSON errors.

---

## Step C — Verify registration

Inside a Claude Code session:

```
/plugin      → confirm "domain-modeling" is listed AND enabled
```

`/domain-modeling` should also appear in slash-command completion.

---

## Step D — End-to-end smoke test

Use a scratch git repo (or a branch you'll throw away). Steps 1–2 were checked
headless on the build branch (S4); steps 3–7 need a second turn, so run them
interactively.

1. Start `claude` in the repo and run:
   `/domain-modeling The term is Handoff, in the Sessions context: the prompt file one session writes so the next can start cold. Rejected: baton, continuation prompt. If Eric only sharpens the wording, I accept it. Settle it.`
   (Naming the context matters in an empty repo: without it, the
   `GLOSSARY.md` heading is Claude's guess, and a guess Eric questions is
   rightly asked first.)
   Expected: Claude calls `board-eric`, then writes `GLOSSARY.md` (a
   `**Handoff**` entry with `_Avoid_`) and `GLOSSARY-SETTLED.md` (the header
   line plus one `settled` row with `session:<date>`), and opens its reply with
   a `📝 Written since last round:` list that includes Eric's verdict.
2. Ask it to settle a term that collides with something else in your domain.
   Expected: nothing is written, and the collision comes back to you as a
   question. Claude's own challenge against the glossary may catch it before
   Eric is called; if it reaches Eric and he sharpens or objects, his point is
   the question.
3. Answer that question. Expected: any line it proposes to add (e.g. a
   pointer to `GLOSSARY-MAP.md`) is shown word for word before it asks for
   your yes; a reply that isn't a yes to what it showed gets one line,
   "Approve … as drafted?", and nothing written. After your yes, the next
   reply opens with the `📝 Written since last round:` announcement of every
   file it wrote, and its wording line says `you approved` (with Eric's
   wording beside it if his differed), not `Eric approved`. It credits Eric
   only with the lines he changed, quoting his text, and names any line he
   approved unchanged as such; check it against his verdict.
4. Say "we pass the baton to the next session". Expected: a drift note
   ("settled as Handoff …") and no question about it; the word "reopen" does
   not appear.
5. Say "reopen Handoff". Expected: the row's status becomes `reopened` and the
   naming question is put to you. Settle it again; expect a new `settled` row
   and the old row's status `superseded` (no row deleted).
6. In a repo with code but no glossary, ask it to bootstrap one. When the
   batch list is shown, trim it then (e.g. "Only the Host batch"); if the list
   comes as a multiple-choice question, pick "Other" and type the trim there.
   Expected: a batch list for you to confirm (per subsystem if the top-level
   directories are layers), read-only extractor sub-agents, Eric's review of
   each batch's term list, and a draft you approve before anything is written; settled rows
   only after the final context pass. Where the draft departs from Eric, it
   asks rather than notes it. Only an explicit yes writes: answer a batch
   draft with anything else (e.g. "next batch") and expect "Approve batch 1 as
   drafted?" and nothing written. Ask it to "run the final pass and Settle":
   expect a draft of the final edits and rows (exact text of any map, pointer
   or reworded line, including lines in other docs) and "Approve the final
   pass and these N rows as drafted?", not a write; if Eric sharpens a wording
   there, it is a question. After your yes, expect one `📝 Written since last
   round:` list of every file and row, ending with a `Wording:` line. Each
   announcement names who approved each wording: a wording you accepted from
   Eric reads `you approved` plus his text, never `Eric approved`; check it
   against what you actually approved.
7. In an environment without `board-eric`, run step 1 again. Expected: it says
   plainly that it won't write the glossary files, writes nothing, and doesn't
   offer the entry for you to paste in by hand.

---

## Definition of done

- `/plugin` shows `domain-modeling` enabled.
- Step D 1–7 behave as above.
- `git status` shows only `GLOSSARY.md`, `GLOSSARY-SETTLED.md` (and
  `GLOSSARY-MAP.md` if a bootstrap split contexts) as new files.
