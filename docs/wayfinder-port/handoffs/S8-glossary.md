# Handoff: S8 · "slice" → "batch" in domain-modeling, then the first glossary rows

Rich starts a fresh `claude` session in the worktree and pastes this whole file
as the first message. S11 (W5, prototype) may be running in parallel on its own
branch; don't touch `plugins/prototype` or its ledger row.

## Context

You are continuing the wayfinder + domain-modeling port on branch
`feat/wayfinder-domain-modeling` in `rinman24/claude-skills`. Work in the
worktree for that branch at `.claude/worktrees/wayfinder-domain-modeling`.
Run `git worktree list` first; enter it with EnterWorktree (`path`) if you
aren't in it. Never commit to main. Fetch first: if S11's PR has merged into
this branch, pull it before editing the ledger.
The marketplace is `claude-skills`; plugins install as `<plugin>@claude-skills`.

Read first, in order:
1. `docs/wayfinder-port/LEDGER.md`: W1, W2, MD6–MD11, WD10 (amended), WD12,
   WD19, WD25
2. `docs/wayfinder-port/LESSONS-LEARNED.md` (S4: smoke tests with Eric; S7:
   no `cd` outside the worktree)
3. `plugins/domain-modeling/skills/domain-modeling/SKILL.md`,
   `SETTLED-FORMAT.md`, `BOOTSTRAP.md`
4. Only if a row needs it: board-knowledge sessions
   `2026-10-06-eric-term-board.md` ("Edits this implies") and
   `2026-10-06-eric-design-document-contract.md` ("Two consequences")

## This session's unit

Ledger items: W1, W2
Goal: (W1) every "slice" meaning "one module's batch of terms" in
`plugins/domain-modeling` and in MD9 becomes "batch"; `rg -n -i slice
plugins/domain-modeling` is clean except where it means Juval's unit.
(W2) run `/domain-modeling` (Eric reviews every write, MD6) to create
`GLOSSARY.md` and `GLOSSARY-SETTLED.md` at the repo root with:
- `subsystem`, rejected `slice`, `vertical slice`; context architecture (WD12)
- `map`, rejected `local board`; context wayfinder (WD19)
- `increment` as squadra's term (squadra PR #41 merged; squadra's own row:
  Vertical / Foundation, rejects `infrastructure increment`), so
  Lookup("increment") here returns ruled-in(squadra) or settled per Eric
- `errand`, rejected `task`, `chore`; context wayfinder (WD25)
Then run Eric's done-test from WD19: `rg -n -i '\bboards?\b' plugins/
docs/wayfinder-port/` returns only squadra-sense uses, agent ids and history.
Estimated work: ~45K tokens (budget: under 100K total, hard stop at 120K).

## Decisions already made

- WD1–WD26 (ledger), all confirmed by Rich in S7. Vocabulary per WD10
  (amended), WD19, WD25.
- MD6/MD7: no glossary write without `board-eric`; MD-B2: Eric advises, Rich
  decides (put sharper wording or objections to Rich before writing).
- `Ref` for these rows: Eric/Rich choose; `session:<board-knowledge file>` fits
  MD10's schemes.

## Out of scope for this session

- Building wayfinder (W3, S9) or anything in `plugins/prototype` (W5, S11).
- Other WD10 terms (`design document`, `decision ticket`, `cleared`): W3 may
  settle them as it writes the skill.
- Anything in squadra.

## Suggested skills

- `domain-modeling:domain-modeling` (W2; it owns the glossary writes)

## Wrap-up

Follow the "End" steps of the session protocol in the ledger. The next handoff
is `handoffs/S9-wayfinder-build.md` for W3 (blocked by W2); tell Rich its path.
