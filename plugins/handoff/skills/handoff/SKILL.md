---
name: handoff
description: Compact the current conversation into a handoff document and drop a marker so a fresh agent is spawned in a new tmux pane to continue with a clean context window.
argument-hint: "What will the next session be used for?"
---

# handoff

Compact the current conversation into a handoff document and drop a marker. A
fresh Claude Code session is then spawned automatically in a new tmux pane (by
this plugin's `Stop` hook) to continue the work with a clean context window.

Your only two jobs in this session are (1) write the handoff document and (2)
drop the marker. **Do not spawn the successor yourself and do not continue the
work** — the hook handles the spawn at the end of your turn. This is deliberate:
keeping the model out of the spawn path is what makes the handoff reliable.

## 1. Write the handoff document

Write a handoff document summarising the current conversation so a fresh agent
can continue the work. Save it to `.pipeline/<slug>/handoff.md` in the current
workspace, where `<slug>` is the active pipeline slug for this work — match an
existing `.pipeline/<slug>/` folder if one already holds this task's artifacts
(`plan.md`, `prd.md`, etc.); otherwise derive a short kebab-case slug from the
task and create the folder. `.pipeline/` is gitignored, so the handoff is not
committed.

Start the document with YAML front matter recording the slug, e.g.:

```
---
slug: <slug>
---
```

Include a "suggested skills" section in the document, which suggests skills that
the next agent should invoke.

Do not duplicate content already captured in other artifacts (PRDs, plans, ADRs,
issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally
identifiable information.

If the user passed arguments, treat them as a description of what the next
session will focus on and tailor the doc accordingly. **Any follow-up task the
user mentions in the same message (e.g. "/handoff and then run the security
review") is an instruction for the SUCCESSOR session, not for this one — write
it into the handoff document so the next agent picks it up. Do not do it here.**

## 2. Drop the spawn marker

After the document is written, create a one-shot marker file at the top of the
pipeline folder:

```
.pipeline/.spawn-successor
```

That's the last thing you do. When your turn ends, the plugin's `Stop` hook sees
the marker, spawns a fresh Claude session in a new lower tmux pane seeded with
the handoff document, and removes the marker. Exactly one successor is created,
and it never depends on the model remembering to spawn.
