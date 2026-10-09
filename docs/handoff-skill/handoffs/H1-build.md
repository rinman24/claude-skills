# Handoff: H1 · Settle and build the handoff skill

Rich starts a fresh `claude` session in
`~/Code/claude-skills/.claude/worktrees/handoff-skill` and gives it this
file.

## Context

You are building the `handoff` plugin on branch `feat/handoff-skill` in
`rinman24/claude-skills`. Work in this worktree; never commit to main.
Fetch first; if `origin/main` moved, merge it in.

Read first, in order:
1. `docs/handoff-skill/LEDGER.md`: the upstream skill's essence, Rich's
   requirements, repo facts, open questions HQ1–HQ3
2. `docs/handoff-skill/LESSONS-LEARNED.md`
3. `plugins/local-backlog/` and `docs/local-backlog-plugin-install-runbook.md`
   (the house pattern)
4. An example of the ledger-and-template style the skill should support,
   from branch `feat/design-to-board`, read-only:
   `git show origin/feat/design-to-board:docs/design-to-board/handoffs/TEMPLATE.md`
   and `git show origin/feat/design-to-board:docs/design-to-board/handoffs/S1b-scope.md`

## This session's unit

Ledger items: H1
Goal: HQ1–HQ3 ruled by Rich and recorded as HD1, HD2, …; `plugins/handoff`
built (user-invoked SKILL.md carrying the upstream essence plus the
rulings, a bundled default template, `plugin.json`, marketplace entry,
install runbook); `claude plugin validate` passes for both; installed as
`handoff@claude-skills` and tried once by writing this session's own
handoff; PR opened.
Estimated work: ~70–90K tokens (budget: under 100K total, hard stop at 120K)

Order: HQ1 first. Offer Rich `/ask-juval` with this question to paste after
typing the command (he types it; you don't):

> A user-invoked `handoff` skill writes a document that lets a fresh agent
> session continue the current work: a summary structured by a template,
> suggested skills, and references (not copies) to the project's ledger,
> specs, ADRs and commits; secrets redacted. Where should the handoff file
> live: (a) the OS temp dir (upstream's choice; lost on reboot, invisible to
> others), (b) a git-ignored `handoffs/` in the repo, or (c) committed
> `handoffs/`? The ledger, which records status, decisions and the next
> handoff's path, stays committed. Rich leans away from version control:
> handoffs are noise in the repo. Which, and what does the ledger then
> point to?

Then HQ2 and HQ3, one at a time, each with your recommendation. If HQ1
moves handoffs out of version control, note (don't do) a follow-up for
existing efforts that commit handoffs (e.g. `docs/design-to-board/`).

## Decisions already made

- Essence of the upstream skill and Rich's requirements: ledger "Source"
  and "Rich's requirements". No attribution or upstream tracking.

## Out of scope for this session

- Changing other efforts' handoffs or ledgers (record a queue item instead).
- Other plugins.

## Suggested skills

grilling:grilling (HQ2, HQ3), `/ask-juval` typed by Rich (HQ1),
anthropic-skills:skill-creator if useful for the SKILL.md.

## Wrap-up

Follow the "End" steps of the session protocol in the ledger. Tell Rich the
PR URL and what's in his queue.
