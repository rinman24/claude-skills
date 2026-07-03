---
name: local-backlog
description: Set up a personal, git-excluded local backlog (BACKLOG.local.md) in the current repo — create the file, write the maintenance convention into CLAUDE.local.md, and wire both into .git/info/exclude. Manual-invocation only; run once per repo.
disable-model-invocation: true
---

# local-backlog

Set up a personal *local backlog* in the current repository: a git-excluded
`BACKLOG.local.md` for "things to do later" that don't (yet) warrant a formal
work item, plus the convention that keeps it visible. It is personal and is
**never committed** — it lives only in this clone.

Run this once per repo. It is idempotent: re-running only adds what is missing
and **never** clobbers an existing backlog.

## Why this is a skill *and* a `CLAUDE.local.md` edit

A skill runs once when you invoke it — it cannot, by itself, change how future
sessions behave. So this skill does two distinct things:

1. **Scaffolds the file** (`BACKLOG.local.md`) — the one-time setup.
2. **Writes the maintenance convention into `CLAUDE.local.md`** — the part that
   *persists*, so every later session announces changes, dates items, and keeps
   the list sorted without being told again.

Do not skip step 2: without it the file exists but nothing makes Claude maintain
it in a fresh session.

## Procedure

### 1. Find the repo root; bail if not a git repo

Run `git rev-parse --show-toplevel`. If it fails (not a git working tree), stop
and tell the user — the `.git/info/exclude` mechanism this skill relies on needs
a git repo. Do everything below relative to that root.

### 2. Don't clobber existing files

If `BACKLOG.local.md` already exists at the root, do **not** overwrite it. Report
that it's already present and stop — unless the user explicitly asks you to
reformat it to the standard header below. The same rule applies to the
`CLAUDE.local.md` section and the exclude entries: add only what is missing,
never rewrite what's there.

### 3. Detect the issue tracker

Read `git remote get-url origin` (fall back to any configured remote). Map the
host to a tracker name for the "promote real work to …" line:

- `dev.azure.com` or `visualstudio.com` → `Azure DevOps`
- `github.com` → `GitHub Issues`
- `gitlab` → `GitLab Issues`
- anything else, or no remote → `your issue tracker`

### 4. Create `BACKLOG.local.md` at the repo root

Write exactly this, substituting `<TRACKER>` from step 3:

```markdown
# Local Backlog (personal, not committed)

Local to this clone — excluded via `.git/info/exclude`, **not** shared with
teammates. This is the lightweight, visible place for "things to do later" that
don't (yet) warrant a formal work item in <TRACKER>.

## How this stays visible

- Claude announces in chat whenever it adds, checks off, or removes an item here
  (nothing gets tucked away unseen).
- Items are dated (absolute dates) and grouped by status.
- Items carry a priority tag: **(P1)** high, **(P2)** normal, **(P3)** low.
  Untagged items default to P2. Keep Open sorted highest-priority first.
- Promote anything that becomes real work to <TRACKER>, then check it off here
  with a pointer.

---

## Open

<!-- Add items here, highest priority first. Example:
- [ ] **(P2) Short title.** One or two sentences of context. Added YYYY-MM-DD. -->

## Done
```

### 5. Persist the convention in `CLAUDE.local.md`

Ensure `CLAUDE.local.md` exists at the repo root (create it if absent). If it
does not already contain a `## Local backlog` section, append this:

```markdown
## Local backlog

This repo has a personal, git-excluded backlog at `BACKLOG.local.md`. Whenever
you add to, check off, or remove an item:

- Announce the change in chat — never edit the backlog silently.
- Date items with absolute dates and group them under `## Open` / `## Done`.
- Tag priority `(P1)`/`(P2)`/`(P3)` (untagged defaults to P2) and keep `## Open`
  sorted highest-priority first.
- The file is personal and not committed (excluded via `.git/info/exclude`) —
  never add it to a tracked `.gitignore`, and never commit it.
- Promote anything that becomes real work to the project's issue tracker, then
  check it off here with a pointer.
```

### 6. Wire `.git/info/exclude`

Append `/BACKLOG.local.md` and `/CLAUDE.local.md` to `.git/info/exclude`, each
only if it is not already listed (grep first — never duplicate a line). This is
the *local* exclude: it ignores these files for this clone only, without
touching the shared, tracked `.gitignore`. A clear way to add them:

```bash
root="$(git rev-parse --show-toplevel)"
exclude="$root/.git/info/exclude"
for f in /BACKLOG.local.md /CLAUDE.local.md; do
  grep -qxF "$f" "$exclude" || printf '%s\n' "$f" >> "$exclude"
done
```

### 7. Announce what you did

Per the convention you just installed, report exactly which files you created or
edited and which exclude lines you added — then confirm the backlog is ready and
that future sessions will maintain it.
