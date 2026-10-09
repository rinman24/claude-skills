---
name: adr
description: Record an architecture decision record (ADR), but only for a decision that is hard to reverse, surprising without context, and the result of a real trade-off. Use when the user asks to record, write or log an ADR or a decision, when another skill (e.g. domain-modeling) hands over an ADR-worthy decision, or when a hard-to-reverse architectural choice has just been made. Follows the repo's existing ADR convention if it has one.
---

# ADR

An ADR records _that_ a decision was made and _why_, in as few words as will do. It is not a diary of every choice made in a session; most decisions don't get one.

## The three gates

Write an ADR only when all three are true:

1. **Hard to reverse**: the cost of changing your mind later is meaningful.
2. **Surprising without context**: a future reader will look at the code and wonder "why on earth did they do it this way?"
3. **The result of a real trade-off**: there were genuine alternatives and one was picked for specific reasons.

If a decision is easy to reverse, skip it: it will just get reversed. If it isn't surprising, nobody will wonder why. If there was no real alternative, there is nothing to record beyond "we did the obvious thing."

What usually qualifies: architectural shape (monorepo, event-sourced writes); integration patterns between contexts; technology choices with lock-in (the ones that would take a quarter to swap out, not every library); boundary and scope decisions, including the explicit no-s; deliberate deviations from the obvious path, so nobody "fixes" them; constraints not visible in the code (compliance, partner SLAs); and rejected alternatives whose rejection is non-obvious.

### When a gate fails

Write nothing. Say which gate failed and why, one line per failed gate:

```
No ADR: fails gate 1 (hard to reverse). Swapping the date library is a one-file change.
```

If the conversation doesn't tell you whether a gate holds (for example, you can't tell whether alternatives were considered), ask the user that one question instead of guessing either way.

## Write or offer

- **The user asked for this ADR**: check the gates, then write it.
- **Another skill handed it over, or you spotted it yourself**: offer it in one line and write it only on the user's yes. A calling skill's request is not the user's permission. The line is the decision, why it clears the gates in a clause, and the question; no recap of the conversation, no list of the gates, no path:

  ```
  ADR? Handoffs are committed Markdown files: hard to undo once sessions depend on them, and picked over a hook-based handoff. Write it?
  ```

Either way, the gates are this skill's call. A caller saying a decision "looks ADR-worthy" doesn't pass them.

## Follow the repo's convention

Before writing, find out whether the repo already records decisions, and if it does, match it exactly.

1. **Instructions.** Check `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md` and `README.md` for an ADR location, template or rule, and tool config such as `.adr-dir` (adr-tools) or `.log4brains.yml`. Stated instructions win.
2. **Existing records.** Look for a decisions directory: `docs/adr/`, `docs/adrs/`, `docs/decisions/`, `docs/architecture/decisions/`, `doc/adr/`, `adr/`, `decisions/`, or any directory of numbered decision files.
3. **Match it.** Read the repo's template file if there is one (`template.md`, `0000-template.md` and the like), otherwise the two most recent ADRs. Copy their filename pattern and numbering (width, prefix such as `ADR-`, dates), frontmatter, headings and required sections, and status vocabulary. If an index file lists the ADRs, add a line for the new one.
4. **Conflicts.** If you find two conventions that disagree, ask the user which one to follow.
5. **Nothing found.** Use the default in [ADR-FORMAT.md](./ADR-FORMAT.md): `docs/adr/NNNN-slug.md`, one paragraph.

A house template with many required sections still gets short answers in each; don't pad it to look complete.

## After writing

Report the write in one line, then stop:

```
📝 Written: docs/adr/0004-billing-talks-to-ordering-via-events.md (Billing and Ordering communicate via domain events)
```

When the new ADR reverses an earlier one, follow the superseding rule in the repo's convention, or in [ADR-FORMAT.md](./ADR-FORMAT.md) if it has none. Never delete or rewrite an earlier ADR's decision.
