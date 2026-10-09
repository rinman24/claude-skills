# Handoff: S6 · Lay out the wayfinder work items

Rich starts a fresh `claude` session in the worktree and pastes this whole file
as the first message.

## Context

You are continuing the wayfinder + domain-modeling port on branch
`feat/wayfinder-domain-modeling` in `rinman24/claude-skills`. Work in the
worktree for that branch at `.claude/worktrees/wayfinder-domain-modeling`.
Run `git worktree list` first; if it isn't there, create it with
`git worktree add .claude/worktrees/wayfinder-domain-modeling feat/wayfinder-domain-modeling`
and enter it with EnterWorktree (`path`). Never commit to main.
The marketplace is `claude-skills`; plugins install as `<plugin>@claude-skills`
(see the ledger's "Repo facts").

Read first, in order:
1. `docs/wayfinder-port/LEDGER.md` (status, budget, session protocol, all
   decisions, and especially "Inputs to triage"; check whether Rich has
   commented on MD-B1–B5 or AD-B1–B4)
2. `docs/wayfinder-port/LESSONS-LEARNED.md`
3. `plugins/grilling/`, `plugins/domain-modeling/`, `plugins/adr/` skim only
   (what wayfinder will call), and `plugins/local-backlog/` (a tracker option)

Upstream reference: https://github.com/mattpocock/skills, pinned at commit
`6fd9479`. Clone it into your session scratchpad; don't vendor it into the
repo. Files for this unit: `skills/engineering/wayfinder/` (all of it) and
`docs/engineering/wayfinder.md` ("Common questions" lists the known defects).

## This session's unit

Ledger items: W0
Goal: every entry in "Inputs to triage" becomes a work item, a decision, or
`dropped`; wayfinder's work items (W1…) are in the ledger with estimates and
sessions, sized to ~80K each; the S7 handoff is written for the first one.
Estimated work: ~40K tokens (budget: under 100K total, hard stop at 120K)

Suggested shape: outline upstream wayfinder (its operations, its dependencies
on `setup-matt-pocock-skills` and on `research`, `prototype`, `to-spec`,
`to-tickets`, `implement`, and its known defects), then grill Rich in rounds
with `/grilling` on the open choices. The tracker choice (GitHub sub-issues vs
`.scratch/` markdown vs `local-backlog`) and the `gh:` ref resolver are the
biggest ones; Rich expects GitHub. If the decisions run long, stop at
recording them and leave the item layout to S7.

## Decisions already made

- GD1–GD7 (grilling), MD1–MD13 (domain-modeling), MD3 and AD-B1–B4 (adr), all
  in the ledger. GD7 and MD13 bear directly on wayfinder: grilling tickets
  never produce code, and wayfinder calls `grilling` and `domain-modeling` by
  name via the Skill tool and checks both loaded.
- MD10: wayfinder passes its ticket ref into domain-modeling's `Settle` as the
  `Ref`.
- MD7: wayfinder tickets in a berth without `board-eric` get no glossary
  writes.

## Out of scope for this session

- Building any wayfinder code or plugin files.
- Changing `grilling`, `domain-modeling` or `adr`, unless Rich's comments on
  MD-B1–B5 or AD-B1–B4 ask for it (then record it as its own work item).

## Suggested skills

- `grilling:grilling` (for the decision rounds; it writes nothing, you record
  the decisions in the ledger after Rich confirms the summary)

## Wrap-up

Follow the "End" steps of the session protocol in the ledger, including writing
the next handoff prompt and telling Rich its path.
