---
name: handoff
description: Compact the current session into a handoff document a fresh agent session can pick up, structured by a template, pointing at the project's ledger and other artifacts instead of copying them, with secrets redacted. Checks the ledger could start the next unit on its own first. Manual invocation only.
disable-model-invocation: true
argument-hint: What will the next session be used for?
---

# handoff

Write a handoff document that lets a fresh agent session continue the
current work. If the user gave an argument, it says what the next session is
for: tailor the document to that focus.

A handoff is a message from this session to the next one. It is not a
record. The record is the effort's **ledger** (a committed `LEDGER.md`
holding status, decisions, the user's queue and a session log), when there is
one. The handoff carries only what the ledger can't: where the conversation
had got to, the current hypothesis, approaches tried and dropped and why,
gotchas, and which skills to use. A fresh session must be able to start the
next unit from the ledger alone; the handoff only makes it faster.

## 1. Find the ledger

Use the `LEDGER.md` this session has been working from. Otherwise look for
one under the repo (`git ls-files '*LEDGER.md'`) whose `Branch:` line matches
the current branch. If several match, ask which one. If none, there is no
ledger: skip steps 3 and 6.

## 2. Resolve where the handoff goes and which template it uses

This is the only place that decides locations. With the ledger at
`<dir>/LEDGER.md`:

| | Handoff file | Template |
|---|---|---|
| Ledger found | `<dir>/handoffs/` | `<dir>/HANDOFF-TEMPLATE.md` if it exists, else this skill's [TEMPLATE.md](TEMPLATE.md) |
| No ledger | `${TMPDIR:-/tmp}` (`%TEMP%` on Windows) | this skill's [TEMPLATE.md](TEMPLATE.md) |

Handoffs are never committed. Before writing into `<dir>/handoffs/`, run
`git check-ignore -q <dir>/handoffs/x.md`. If it isn't ignored, say so and
offer to add a line such as `docs/*/handoffs/` to the repo-root `.gitignore`;
if the user declines, write to `$TMPDIR` instead.

## 3. Check the ledger could start the next unit on its own

Read the ledger and ask: could a fresh session, given only this file, find
the next unit and take its first action without asking the user anything that
isn't already in the user's queue? Check that:

- the next unit has a work-item row with a goal and an estimate, and this
  session's unit has its final status;
- decisions made this session are recorded;
- the user's queue reflects what they now have to do.

If anything is missing or stale, list the gaps and offer to fix the ledger
before writing the handoff. Edit it only after the user says yes. Don't copy
the missing facts into the handoff instead: the handoff is not a substitute
for the ledger.

## 4. Name the file

Follow the ledger's numbering. If the session log names sessions `H0`, `H1`,
…, the next handoff is `H<N>-<slug>.md`, where `H<N>` is the session that
will read it and `<slug>` is two or three words for its unit. Without a
convention, or without a ledger, use `handoff-<YYYY-MM-DD>-<slug>.md`. Never
overwrite an existing handoff; ask first.

## 5. Write it from the template

Fill every section of the template; drop a section only if the template marks
it optional. Then:

- Reference other artifacts by path or URL: the ledger, specs, plans, ADRs,
  issues, PRs, commits, diffs, advisor session files. Don't copy their
  content. If a reader needs one section of a long file, name the section.
- Under "Suggested skills", name skills from the ones available in this
  session that the next agent should invoke, and when to use each.
- Redact secrets and personal data: tokens, keys, passwords, connection
  strings, customer names and contact details. Say that something was
  redacted, and where the next session can get it.
- Keep it short. Anything a reader could rebuild from the referenced
  artifacts in a minute doesn't belong.

## 6. Record the path in the ledger

Put the handoff's path, relative to the ledger, in this session's row of the
session log (the "Handoff written" column, or its equivalent). This is the
only ledger edit the skill makes without asking. If the ledger has no session
log, or no row for this session yet, say so rather than inventing structure.
Don't commit; committing the ledger is the session's job.

## 7. Report

Tell the user:

- the handoff's path;
- any ledger gaps from step 3 they chose not to fix;
- how to start the next session, e.g. "Start `claude` in `<worktree>` and give
  it `<path>`."
