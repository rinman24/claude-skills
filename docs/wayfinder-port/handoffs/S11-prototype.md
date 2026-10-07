# Handoff: S11 · Build the `prototype` plugin (runs in parallel with S8)

Rich starts a fresh `claude` session from the `claude-skills` checkout and
pastes this whole file as the first message. S8 is running in parallel on
`feat/wayfinder-domain-modeling`, so this session uses its **own branch and
worktree**.

## Context

You are continuing the wayfinder + domain-modeling port in
`rinman24/claude-skills`. Run `git worktree list` and `git fetch` first. Create
a branch and worktree off the port branch:
`git worktree add -b feat/prototype-plugin .claude/worktrees/prototype origin/feat/wayfinder-domain-modeling`,
then EnterWorktree with `path: .claude/worktrees/prototype`. Never commit to
main or to `feat/wayfinder-domain-modeling`. At the end, push
`feat/prototype-plugin` and open a **draft PR into
`feat/wayfinder-domain-modeling`** (not main); Rich merges it.
The marketplace is `claude-skills`; plugins install as `<plugin>@claude-skills`.

To keep the merge clean: in `docs/wayfinder-port/LEDGER.md` edit only the W5
row and add one S11 session-log row; append lessons under a new `## S11`
heading; put the marketplace entry and README section at the end of their
lists.

Read first, in order:
1. `docs/wayfinder-port/LEDGER.md`: W5, W6, WD3, WD7, WD10 (amended), WD25,
   WD26, GD7
2. `docs/wayfinder-port/LESSONS-LEARNED.md` (S2/S4/S5: headless smoke tests;
   S7: parallel sessions, no `cd` outside the worktree)
3. House pattern: `plugins/adr/` (closest: no advisor in the loop) and
   `docs/local-backlog-plugin-install-runbook.md`

Upstream reference: https://github.com/mattpocock/skills @ `6fd9479`. Shallow
clone into the job temp dir and find the `prototype` skill and its docs page
(`docs/engineering/…`, "Common questions" lists known defects).

## This session's unit

Ledger items: W5
Goal: `plugins/prototype` built (SKILL.md, any bundled format files, manifest,
upstream MIT LICENSE, marketplace entry, README section, runbook), validated
with `claude plugin validate .`, and headless smoke-tested with `claude -p
--plugin-dir plugins/prototype …` (add `--permission-mode acceptEdits` if it
writes). Start with one short `/grilling` round on how upstream's prototype
differs from what WD7 needs, then build.
Estimated work: ~60K tokens (budget: under 100K total, hard stop at 120K).

## Decisions already made

- WD7: `prototype` is its own plugin; the user picks the variant, never the
  agent (upstream defect 3).
- Prototypes are throwaway variants for a decision. Wayfinder itself never
  builds (WD4), and grilling never writes code (GD7). Prototype writing code
  is fine, but it must not turn into the build.
- Vocabulary: no "work", "deliverable", "slice", "task" or "board" in the
  sense of a wayfinder map (WD10, WD19, WD25).
- How wayfinder calls it (ticket kind `prototype`, WD26) is W6, not this
  session.

## Out of scope for this session

- Wiring prototype into wayfinder (W6, blocked by W3).
- Anything S8 owns: `plugins/domain-modeling`, `GLOSSARY*.md`.

## Suggested skills

- `grilling:grilling` (one round before building)
- `anthropic-skills:skill-creator` (optional, for SKILL.md structure)

## Wrap-up

Follow the "End" steps of the session protocol in the ledger, except: don't
write a next handoff (W6 waits for W3; the S10 session writes S12's handoff
if W5 has merged). Push `feat/prototype-plugin` with the `gh` credential
helper command from the lessons, open the draft PR into
`feat/wayfinder-domain-modeling`, and give Rich its URL.
