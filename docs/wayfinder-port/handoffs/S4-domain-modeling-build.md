# Handoff: S4 · Build `plugins/domain-modeling`

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

S3 settled every design decision for domain-modeling (MD1–MD13, confirmed by
Rich). This session builds it. Don't reopen the decisions; if one turns out
unbuildable, stop and ask Rich.

Read first, in order:
1. `docs/wayfinder-port/LEDGER.md` (status, budget, session protocol, the
   domain-modeling decisions MD1–MD13, and GD7)
2. `docs/wayfinder-port/LESSONS-LEARNED.md` (S2: `--plugin-dir` smoke-test
   recipe and the worktree guard's limits; S3: calling board advisors)
3. `plugins/grilling/` and `docs/grilling-plugin-install-runbook.md` (house
   example; credits upstream MIT with a copied LICENSE)
4. The two advisor answers MD10–MD11 are built from, for exact wording (the
   settled-record header line, Lookup's typed answers):
   `/Users/richinman/Code/board-knowledge/sessions/2026-10-06-juval-settled-term-lookup.md`
   and `…/2026-10-06-eric-settled-term-verbs.md`. Where they differ, Eric's
   answer and MD11 win (no Retire, no `pruned`, `Term`/`Rejected` split).

Upstream reference: https://github.com/mattpocock/skills, pinned at commit
`6fd9479`. Clone it into your session scratchpad; don't vendor it into the
repo. Files for this unit: `skills/engineering/domain-modeling/SKILL.md` and
`GLOSSARY-FORMAT.md` (adapt), `LICENSE` (copy). `ADR-FORMAT.md` is not part of
this plugin (MD3; it goes to `plugins/adr`, item A1).

## This session's unit

Ledger items: M2
Goal: `plugins/domain-modeling` built from MD1–MD13, validated with
`claude plugin validate .`, and smoke-tested headless via `--plugin-dir`.
Estimated work: ~60K tokens (budget: under 100K total, hard stop at 120K)

Deliverables (match `plugins/grilling`):
- `.claude-plugin/plugin.json`, upstream `LICENSE` copy.
- `skills/domain-modeling/SKILL.md`: active vs passive, challenge/sharpen/
  scenarios/cross-reference (upstream), inline writes announced next round
  (MD4), bloat guard (MD5), Eric on every write via the `board-eric` agent,
  with refusal when it's missing (MD6–MD8), settled-record operations and
  "drift is not reopening" (MD10–MD11), ADR hand-off to the `adr` skill (MD3).
  Keep SKILL.md lean and put detail in format files.
- `GLOSSARY-FORMAT.md` (upstream's, adapted), a new `SETTLED-FORMAT.md`
  (MD10–MD11), and a bootstrap file for MD9 if SKILL.md would otherwise grow
  past ~120 lines.
- Marketplace entry, README section,
  `docs/domain-modeling-plugin-install-runbook.md`.

Smoke test: one bare `claude -p --plugin-dir plugins/domain-modeling "…"` from
the worktree root (no `cd`, pipes or redirects; see the S2 lessons). It will
write `GLOSSARY*.md` into the worktree, so run `git status` afterwards and
remove the test files before committing. Check that a settled term produces
both a `GLOSSARY.md` entry and a `GLOSSARY-SETTLED.md` row, and that Eric was
consulted. Anything needing a second turn (the next-round announcement,
Reopen, bootstrap review) goes in the runbook as interactive steps for Rich.

## Decisions already made

- MD1–MD13 (ledger: Decisions, domain-modeling).
- GD7: grilling writes nothing; domain-modeling owns doc writes.
- No dependency on `setup-matt-pocock-skills` (ledger: Goal). The upstream
  skill files have no `docs/agents/` references; keep it that way.
- One plugin per skill; marketplace name `claude-skills`.

## Out of scope for this session

- `plugins/adr` (A1, next session), wayfinder, grill-with-docs (MD13).
- Changing `~/Code/board` or `/ask-eric` (MD7).
- A `gh:` resolver or `term-settled` backfill (MD12).

## Suggested skills

- `anthropic-skills:skill-creator` (only if useful for structuring SKILL.md)

## Wrap-up

Follow the "End" steps of the session protocol in the ledger, including writing
the next handoff prompt (`S5-adr.md` for A1) and telling Rich its path.
