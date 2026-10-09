# Handoff: Q4 · Scratch cleanup, then domain-modeling Step D 3 and 6 again

Rich starts a fresh `claude` session in the worktree and pastes this whole file
as the first message.

## Context

You are continuing the wayfinder + domain-modeling port on branch
`feat/wayfinder-domain-modeling` in `rinman24/claude-skills`. Work in the
worktree for that branch at `.claude/worktrees/wayfinder-domain-modeling`
(EnterWorktree with `path` if you aren't in it). Never commit to main. Fetch
first. PR #5 merged the port into `main` (`084df9f`). The branch now carries
ledger-only commits after that (`a6a3389` and the commit that added this
handoff); GitHub deleted the branch on merge and the W9 push recreated it.

All five port plugins are installed from the marketplace (`<plugin>@claude-skills`,
user scope, 0.1.0, enabled; checked 2026-10-09). Use the installed plugins
for the checks, with no `--plugin-dir`, so the bare `/domain-modeling` works.

Read first, in order:
1. `docs/wayfinder-port/LEDGER.md`: Rich's queue (Added in Q2, S13, W9),
   W8.2, MD-B2 and MD-B6, session log
2. `docs/wayfinder-port/LESSONS-LEARNED.md`, especially Q1 and Q2 (ask Rich to
   paste only the reply that decides the check; read the written files
   yourself) and S1 (git commands aimed at another repo are refused here;
   such commands go to Rich for a normal terminal)
3. `docs/domain-modeling-plugin-install-runbook.md` Step D 2, 3 and 6
4. `plugins/domain-modeling/skills/domain-modeling/SKILL.md` ("Eric reviews
   every write") and `BOOTSTRAP.md` step 4

## This session's unit

Ledger items: Q4 (Rich's queue: "Optional cleanup of Q2's scratch state" and
"domain-modeling Step D 3 and 6 again").
Goal: the scratch state is cleaned up per Rich's say, and domain-modeling
Step D 3 and 6 are re-run against W8.2. Each check is recorded as passed or
logged as a new W8.x row. Nothing is fixed this session.
Estimated work: ~30–45K (budget: under 100K total, hard stop at 120K).

Steps:
1. Cleanup first, because billet must be back on `main` before step 6
   bootstraps in it. State found at W9 (2026-10-09); re-check each before
   acting:
   - `~/Code/billet`: on `scratch/adr-check`, with
     `docs/adr/adr-0016-postgres-event-store.md` and a `mkdocs.yml` edit.
     Command in the queue item.
   - `~/Code/scratch/dm-smoke/docs/adr/`: delete. Keep the rest of dm-smoke,
     which hosts step 3.
   - `~/Code/scratch/wf-verdict`: toy map plus branch `prototype`. Ask Rich
     whether to delete the whole directory.
   - `~/Code/scratch/site-dash`: already clean (no `scratch/prototype-test`
     branch, nothing on port 5077). Keep it.
   - Not in the ledger: `~/Code/scratch/wayfinder-clarification` (an empty
     git repo with no commits) and two untracked files at squadra's root,
     `battery-dispatch-summary.prototype.html` and
     `microgrid-site-state.prototype.html` (Oct 7, likely prototype Step D in
     S11). Ask Rich. SQ1 runs in its own squadra worktree, so this doesn't
     block it.
   Put the deletions and git commands in one block for Rich to run in a
   normal terminal. Then verify by reading `.git/HEAD` and listing directories
   (absolute paths, no `cd`).
2. Step D 3 in `~/Code/scratch/dm-smoke`: Rich runs Step D 2 (a colliding
   term), answers the question, and pastes only the reply that follows. Pass:
   it opens with `📝 Written since last round:` and the `Wording:` line says
   `you approved` (Eric's wording beside it if it differed), not
   `Eric approved`. Check `GLOSSARY.md` and `GLOSSARY-SETTLED.md` against
   what he approved.
3. Step D 6 in `~/Code/billet` on a new branch `scratch/dm-bootstrap` (Rich
   creates it). Keep it to one batch (Q1 lesson: trim the batch list to one
   batch, then ask for the final pass and Settle). Pass: batching is per
   subsystem, since billet's top-level dirs are layers. Any departure from
   Eric comes back as a question, not a note. Any change after Rich's batch
   approval, including Eric's final-pass sharpening, comes back as a question
   before `GLOSSARY.md` changes. Each announcement names who approved each
   wording, and that matches what Rich actually approved. Read the written
   files and the deciding replies, not the skill's summary (Q1 lesson). Then
   give Rich the command to drop the branch and return billet to `main`.

## Decisions already made

- Rich's order after W9: these re-runs, then the cleanup, then squadra
  (2026-10-09). Cleanup moved first here only because step 6 needs billet
  on `main`.
- MD-B6: accepting Eric's sharpening in advance counts as Rich's approval
  (confirmed, S13).
- Keep `site-dash` as the prototype Step D 6 repo (W8.7).

## Out of scope for this session

- Any skill or runbook change. Log defects as new W8.x rows for a later unit.
- squadra code (SQ1, `handoffs/SQ1-mandatory-claim-scope.md`) and the squadra
  GitHub adapter.

## Suggested skills

`domain-modeling:domain-modeling`, typed by Rich in the target repos, not run by
the session.

## Wrap-up

Follow the "End" steps of the session protocol in the ledger. Tick the two
queue items (or record what's left). Write a handoff only if a W8.x fix unit
is needed. Then open a small PR from `feat/wayfinder-domain-modeling` to
`main` for the ledger-only commits, ready for review. Tell Rich the PR URL and
what's left in his queue.
