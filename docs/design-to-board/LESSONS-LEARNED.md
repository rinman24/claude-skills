# Lessons learned

Append-only. One entry per lesson: what happened, and how to apply it next
time. Newest at the bottom.

The wayfinder port's lessons (`docs/wayfinder-port/LESSONS-LEARNED.md`)
still apply; the ones that matter most here: push command (S1), merge
`origin/main` rather than rebasing a pushed branch (S1), absolute paths and
no `cd` into another repo (S6/S7), "read the consumer, not only the config"
(Q3), continue the same advisor agent with SendMessage (S8), `/ask-juval`
is typed by Rich (Q3), and the headless-check recipe (S14, S15).

## S0 · 2026-10-09

- **squadra has no create path.** Its `BoardAccess` only reads, moves state,
  tags and comments, and only ADO is wired. Apply: don't assume "publish to
  the board" means "call squadra"; DBQ1 decides where board writes live.

## S1 · 2026-10-09

- **An advisor who proposes names needs Eric before the ruling is final.**
  Juval's structure was right, but his verb `publish_increment` collided with
  wayfinder's settled Publish/`Published`, and his cascade placement would
  have had the translator invent IDs. Apply: when Juval's answer introduces
  verbs, states or identities, route the vocabulary through `/ask-eric`
  before recording the decision.
- **Two advisor consultations cost about 60K of a session.** Each answer is
  relayed verbatim and written verbatim to its session file, so it lands in
  context twice (~25–30K each). Apply: plan at most one consultation per
  session alongside other rulings, or a session that is only consultations.
- **One ruling can settle several questions.** DB-D1 answered most of DBQ2
  and DBQ4 and half of DBQ3. Apply: after each ruling, re-annotate the open
  questions before asking the next one, so Rich rules only what is left.

## S1b · 2026-10-09

- **Two options that each depend on the other are one question.** Juval
  showed that "where does the parent come from" and "how wide is the lookup"
  forced each other ((c) needs a board-wide query; a per-parent query needs a
  map → parent file). Apply: before putting two coupled questions to Rich as
  separate rulings, check whether one answer forces the other, and ask them
  as one.
- **A read scope is not a write scope.** The first draft of the lookup
  filtered by claim scope; Juval's A1 showed that turns "out of scope" into
  "first run" and queues a map twice. Apply: when a query feeds a "does it
  exist yet?" decision, it reads everything and reports the scope as a fact.
- **Ask whether Rich wants an advisor before recommending the ruling.** Rich
  sent DBQ4 and then DBQ5, DBQ6 and DBQ8 to advisors after seeing my
  recommendation, which cost a round each time. Apply: for a question that
  shapes a contract or a validation rule, offer the advisor up front as part
  of the question.
- **The background-isolation guard rejects writes to `~/Code/board-knowledge`.**
  `/ask-*` session files there aren't in a worktree. Apply: with Rich's
  OK, write the session file with a quoted shell heredoc (uncommitted, as
  the ask skill says).

## S1c · 2026-10-09

- **Two independent consultations can run in parallel in one turn.** Rich
  typed both prompts in one `/ask-juval`; Juval and Eric ran as two blind
  background agents at once and both answers arrived before the first
  ruling. Apply: when the questions don't feed each other, launch both
  advisors together; the wall-clock cost is one consultation.
- **Write a long answer's session file from the agent transcript, not by
  retyping it.** Extracting the final text from the agent's output file into
  the session file keeps it verbatim and puts it in context once (the
  relay), not twice. Apply: relay in chat, then `cat` the extracted text
  into the heredoc. Eric's answer was retyped and cost ~5K more.
- **Read the other ledger before answering an advisor's blocking question.**
  Juval's blocker (does the fake keep state across processes?) was already
  SQ3's first design question in squadra's ledger; one grep turned it into
  a requirement instead of a question to Rich. Apply: grep the sibling
  effort's ledger and handoffs before putting a blocker to Rich.
- **Two consultations plus three rulings filled the session.** ~110K at the
  last ruling, so the split went to S1d as the handoff allowed. Apply: the
  S1 estimate (two consultations ≈ 60K) holds; budget the boot (~25K here,
  merge included) on top, and plan the next unit as split only.
- **Handoffs are no longer committed.** The `origin/main` merge brought
  handoff-skill's HD1: `docs/*/handoffs/` is gitignored, so `S1d-split.md`
  lives only in this worktree. Earlier handoffs stay tracked. Apply: don't
  `git add -f` a handoff; the ledger's session log names it, and the
  worktree must not be removed before the next session starts.

## S1d · 2026-10-09

- **A test belongs to the unit that builds what it asserts.** The suggested
  cut put T1 (the golden plan) in the reader unit, which has no `plan` yet.
  Apply: when splitting, name each test's subject and place it with that
  code; give earlier units their own tests (here: one failing fixture per
  check).
- **The sibling ledger's status sets the build order, not the split.** E1 and
  E2 need only squadra's frozen contract (SQ2, merged); F and G wait on SQ3,
  SQ4 and SQ5, which are still `todo`. Apply: record each unit's squadra
  gate in its row, and before starting a gated unit grep squadra's ledger for
  those items' status first.
- **A small cross-plugin change can share a build session.** DB-W (~12K)
  must precede checks 14 and 15, and a session of its own would be mostly
  boot. Apply: pair it with the unit that consumes it, as its own commit,
  when the two together stay under ~70K of planned work.

## S2 · 2026-10-09

- **A glossary write can't close inside a build session without Rich.**
  domain-modeling sends every `GLOSSARY-MAP.md` write to Eric and then needs
  Rich's yes on the exact text; Eric sharpened three lines and asked for a
  fourth, so DB-W's map edit missed the session. Apply: launch Eric in the
  background at the very start, put the question to Rich as soon as it
  returns, and commit the rest of the unit without waiting.
- **An advisor's review can drift from an earlier ruling.** Eric proposed
  "reconciles" where WD14 (approved by him) says "transcribes", and "checks
  6–14" where DB-D8 since added 15. Apply: before relaying a sharper wording,
  diff it against the settled wording and the latest decisions, and show
  Rich each conflict next to the line.
- **`uvx pytest` runs a stdlib plugin's tests with no env in the repo.** Add
  `-p no:cacheprovider` and gitignore `__pycache__/`. Apply: the same command
  for DB3–DB5 (Repo facts).
- **An exactly-once assert in the fixture factory paid for itself.** Ten
  test failures were wrong edit strings, not wrong code, and the assert
  named each one. Apply: keep fixture edits as `(old, new)` pairs on one
  valid document, each asserted to match once.
- **Rich commits to the branch during a session.** A ledger commit landed
  mid-session. Apply: `git log -3` before editing the ledger at the end.
