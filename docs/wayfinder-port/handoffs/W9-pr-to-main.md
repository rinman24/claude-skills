# Handoff: W9 · PR to main and marketplace install

Rich starts a fresh `claude` session in the worktree and pastes this whole file
as the first message.

## Context

You are continuing the wayfinder + domain-modeling port on branch
`feat/wayfinder-domain-modeling` in `rinman24/claude-skills`. Work in the
worktree for that branch at `.claude/worktrees/wayfinder-domain-modeling`
(EnterWorktree with `path` if you aren't in it). Never commit to main. Fetch
first, and pull if the branch moved. The marketplace is `claude-skills`;
plugins install as `<plugin>@claude-skills` (see the ledger's "Repo facts").

Read first, in order:
1. `docs/wayfinder-port/LEDGER.md`: Repo facts, Rich's queue, W9, and the
   session log
2. `docs/wayfinder-port/LESSONS-LEARNED.md` (the push command; no
   force-push; merge `origin/main` rather than rebase)
3. `README.md` and `.claude-plugin/marketplace.json`
4. Each new plugin's runbook "Step A–C" (install) sections:
   `docs/grilling-plugin-install-runbook.md`,
   `docs/domain-modeling-plugin-install-runbook.md`,
   `docs/adr-plugin-install-runbook.md`,
   `docs/wayfinder-plugin-install-runbook.md`

## This session's unit

Ledger items: W9.
Goal: a ready-for-review PR from `feat/wayfinder-domain-modeling` to `main`
with a body that lists the new plugins (grilling, domain-modeling, adr,
wayfinder), the changes to `prototype` and the docs, what was verified
(headless and Rich's interactive Step D runs, per the ledger), and what is
still open (Rich's optional
re-runs). Rich reviews and merges; the session does not merge. After he
merges: `claude plugin marketplace update claude-skills`, install the four new
plugins at user scope, update `prototype`, and check `/plugin` lists each
enabled.
Estimated work: ~10–15K (budget: under 100K total, hard stop at 120K).

Steps:
1. Fetch; check whether `main` moved since the branch point. If it did, merge
   `origin/main` into the branch (no rebase), resolve, re-validate.
2. `claude plugin validate .` and each plugin under `plugins/`.
3. Check the branch carries no scratch state: nothing under `.scratch/`, no
   toy maps, prototypes or `GLOSSARY*.md` at the repo root that a smoke test
   left behind (`git diff --stat origin/main...HEAD`; the port's own
   `GLOSSARY-SETTLED.md`, `GLOSSARY-MAP.md` and `plugins/wayfinder/GLOSSARY.md`
   are intended, per WD27).
4. Open the PR with `gh pr create` (Rich has asked for this unit; open it
   ready for review, not draft, unless he says otherwise). Base `main`.
5. Hand Rich the install commands for after the merge, and run them only if
   he says it's merged.

## Decisions already made

- Order Q1 → S13 → PR to main (Rich, 2026-10-08; ledger Q1 row).
- `prototype` already shipped to main via PR #3; this PR carries only its
  later doc and wiring changes.
- Rich's open queue items (the optional domain-modeling Step D 3 and 6
  re-run, Q2 scratch cleanup, W-SQ, the squadra GitHub adapter) don't block
  the PR; list them in its body as follow-ups.

## Out of scope for this session

- Any skill or runbook change. If the PR review turns something up, log it as
  a new ledger row for a later unit.
- squadra work (W-SQ, GitHub adapter) and `design-to-board` (T1).

## Suggested skills

None.

## Wrap-up

Follow the "End" steps of the session protocol in the ledger. W9 is the last
unit of the port: mark W9 done once the PR is open (or merged and installed,
if Rich merges in-session), move anything still open to Rich's queue, and
tell Rich the PR URL and what's left in his queue. No next handoff unless a
follow-up unit is needed.
