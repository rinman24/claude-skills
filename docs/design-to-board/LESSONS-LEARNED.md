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

## S2b · 2026-10-09

- **Blind advisors can agree on structure and split on a name.** Juval and
  Eric both kept "transcribes" and WD14's ResourceAccess, then split on the
  step's name. One question to Rich with both options settled it; the parts
  of the losing answer that didn't conflict (Juval's third Engine, table as
  data) were carried to the next unit as unruled, not silently adopted.
  Apply: after a split, list what both agree on, rule only the conflict, and
  park the rest with a named owner.
- **Extract the agent's last assistant text from the JSONL transcript with a
  short Python parser.** It kept both answers verbatim and out of context
  (only the relay was in context). Apply: reuse it for every `/ask-*` file.
- **`docs/*/handoffs/` is gitignored on this branch.** Handoff edits never
  reach a commit or PR. Apply: anything a later session must rely on goes in
  the ledger (rows, queue, decisions), not only in a handoff.
- **A consultation-only session with both advisors in parallel came in near
  the estimate** (~75K with the writes). Apply: keep naming disputes to
  their own short session, as S2b did.

## S2c · 2026-10-09

- **The sibling effort can move between the brief and the session.** The
  brief said "SQ2c is PR #48; SQ3 next"; by boot #48 had merged and SQ3 was
  done in PR #49. Apply: check the sibling PR's state (`gh pr view`) and
  ledger rows at boot, record what is true, and read sources from `main`
  once their PR has merged.
- **A ruling made in the other effort is recorded here as a new row that
  amends, not as an edit.** DB-D1 and DB-D4 keep their text and gain
  "amended by DB-D10" in their status cells; the rows that build on them
  (DB3, DB4) carry the change. A recording-only unit came in near ~30K.
  Apply: the same pattern when squadra's SQ5 or a later note reopens a DB-D
  ruling.

## S3 · 2026-10-09

- **Put the unruled structure to Rich and the name to Eric in the same
  turn.** Eric ran in the background while Rich answered; both were back
  before the first line of code, and the name cost no main context. Apply:
  any build unit that opens with a carried recommendation and a name.
- **A completeness test alone doesn't prove the code reads the table.** A
  second test parametrized over every cell runs `reconcile` and checks the
  row's outcome against `TRANSLATION_TABLE[cell]`. Apply: the same pair
  when DB4 maps squadra's exit codes to report classes.
- **One fixture covers a second map.** Juval's cross-map cases derive map
  `portal` from `valid.md` with two `(old, new)` edits (the map name, one
  `billing:I3` in `Depends on`). Apply: no new fixture document for DB4.
- **A stub `squadra` with a `sys.executable` shebang on a monkeypatched PATH**
  serves both the in-process Access and the subprocess CLI tests (T1, T3).
  Apply: DB4 swaps it for SQ3's fake (`provider = "fake"`) through the real
  CLI once SQ4 lands.
- **S3 ran over budget** (~160K by the session counter, against ~100K and a
  120K ceiling): the start-up reads (hook rules, a 43K ledger, squadra's
  contract, the Juval and Eric files) took about a third. Apply: in S4 read
  only the ledger rows the handoff names (DB4, DB-D6, DB-D7, DB-D10, DB-D11),
  not the whole ledger.

## S4 · 2026-10-09

- **Read squadra from `origin/main` with `git show`, never by checking it
  out.** Rich's `~/Code/squadra` sat on an older `main`; `git show
  origin/main:<path>` and `git archive origin/main` gave the contract, the
  notes and an installable tree without touching his checkout. Apply: any
  session that needs another repo's merged state.
- **A shim in front of the real CLI gives crash, race and fault injection
  for free.** One small script on PATH counts write calls and, before write
  n, fails it or patches the fake's file (which also arms the fake's one-shot
  create fault). T5's every-k, the inside-create partials and T6's race came
  from the same fixture, with no change to squadra. Apply: DB5's GitHub run
  needs none of it; reuse it for any later executor test.
- **Assert the precondition a convergence test depends on.** T5 passed
  first time; checking that the inside-create stops really left a partial
  item (`state: null`, for j < k only) is what proved the re-run finished one.
- **Start-up reads stayed small by reading rows, not files** (S3's lesson
  applied): the ledger rows by line number, squadra's notes N16–N19 by grep.
  The fixed cost is the injected rules and the system prompt, ~60K before the
  first read here. Apply: S5 reads the DB5 row, Repo facts and SQ5's row only.

## S5 · 2026-10-27

- **An integration run can be a sibling effort's first live test.** SQ5b moved
  the adapter's sandbox run to SQ5c, so DB5's transcription made the GitHub
  adapter's first real writes. Apply: before an integration unit, read the
  sibling's cut lines as well as its status, and report what the run verified
  back to that effort (Rich's queue).
- **Probe the case the acceptance test passes vacuously.** "Nothing out of
  scope" held because nothing was under #2. A cheap probe (`--parent 2` on a
  fresh map) showed the first-run gap and a looping fix line. Apply: for each
  negative criterion, try one input that should trip it. And say which run in
  a probe writes: the second call here was a real run, harmless only because
  squadra refused it.
- **A CLI flag's default can outrank the config it validates.** `squadra init
  --check` without `--provider` checked an ADO board and failed with ADO's
  state names. Apply: when a check fails naming states the board doesn't have,
  suspect the provider before the map.
- **Install another repo's tool from origin, not the local clone.** Rich's
  squadra clone was 41 commits behind; `uv tool install git+…@<sha>` pins the
  merged commit and leaves his checkout alone (S4's `git show` lesson, applied
  to installs).

## S6 · 2026-10-27

- **A fix that says "re-run, the checks will name it" is a coverage claim.**
  DB4's exit-3 fix is only true if every exit 3 squadra can raise has a board
  check that sees it; DB6 (and Juval's partial-item case, DB11) are the holes.
  Apply: when a fix line defers to another check, list the cases it covers
  next to the check that catches each one, and an empty cell is the next gap.
- **Ask the other component the question, not for its config.** Exposing
  `claim_scope` would move squadra's scope rule across the boundary; a
  `scope --parent` verb keeps it inside, and an agreement test pins the verb
  to the refusal it predicts. Apply: before asking a sibling for data, ask
  which decision you'd make with it, and request that decision as a verb.
- **Answer an advisor's blocking question from the source before the ruling.**
  Juval's verdict held either way but its price depended on whether squadra
  already shared one predicate; a two-line `git grep` on `origin/main` settled
  it and let Rich rule in the same round.

## S6b · 2026-10-27

- **Gate on a merge, not on a sibling ledger's status.** squadra's `main`
  ledger said SQ5e `todo` while Rich had it in progress on a branch; the
  status lags the work. Apply: write a gate as "<row> merged on `main`" and
  check it with `git show origin/main:…`, which is true or false.
- **A session's write guard covers sibling checkouts too.** board-knowledge
  is a shared checkout, so the `## Choice` line was refused here. Apply: when
  a ruling belongs in another repo's file, queue the exact line for Rich
  instead of working around the guard.

## S8 · 2026-10-27

- **Ask the sibling only on the path where its answer decides.** The scope
  question matters only on a first run; a later run's items already carry
  `in_claim_scope`. Putting "is this a first run" in the engine
  (`first_run_parent`) kept the Manager free of prefix logic and kept the
  extra subprocess off every later run. Apply: when a new read feeds a pure
  check, let the engine name when it's needed and the Manager fetch it.
- **A loop test needs the board to change between the read and the write.**
  The flip test only proves something because the shim narrows
  `squadra.toml` before write 1, so squadra's real refusal fires after
  design-to-board's checks passed. Apply: for a "the re-run's checks name it"
  claim, script the change inside the run and assert both runs' exit codes.
- **Write the coverage table when you close a cell.** Listing every exit-3
  class against what the re-run sees showed which cells the translation
  table already covered and left exactly one gap (partial items, DB11).

## S9 · 2026-10-27

- **A fault-injection hook needs the state it patches to exist.** The first
  probe "passed" without exercising the fault: the shim's `patch` hook writes
  the fake's board file, which an empty board hasn't created, so the shim
  crashed and design-to-board reported a `FileNotFoundError` as squadra's.
  Apply: seed the board (`seed({})`) before arming a hook, and read the
  probe's actual output before trusting its exit code.
- **Count a create's steps per row, not per suite.** T5's `CREATE_WRITES = 4`
  holds for a queue with one predecessor; `billing:I1` has none, so its create
  is three steps and j = 3 commits it. Apply: derive the crash range from the
  row under test, or the last case silently tests a complete item.
- **When a sibling gives the verdict, quote it.** `partial-items` returns the
  refusal byte for byte, so the failure line embeds it and design-to-board
  owns no wording of squadra's rule. A check that only routes on `queue` and
  quotes `refusal` can't drift from squadra's refusal.

## S9b · 2026-10-28

- **Gate a check on its own inputs, not on the Plan.** DB11 asked
  `partial-items` only once a Plan existed, which hid a board-state failure
  behind unrelated row failures and made two independent repairs
  sequential. DB-D6 already said "suppress checks whose inputs have already
  failed"; the reading skipped asking what the check's inputs were. Apply:
  before gating a check, list its inputs and gate on exactly those; if one
  is a value the Engine computes on the way to the Plan, hand it over as
  its own value (a draft) rather than waiting for the Plan.

## S10 · 2026-10-28

- **Mutate the gate to prove a fence test.** A test that asserts a read was
  never made passes just as well if the code under test can't reach that
  read for some unrelated reason. Making the Manager ask `partial-items`
  without a parent turned all five fence cases red, which shows the tests
  watch the gate and not an accident of setup. Apply: for every
  "never called" assertion, break the gate once by hand and see it fail.
- **Use the contract's constants in fixtures, not their spelling.** A
  hand-typed `"QUEUED"` made two fence cases fail on the board read
  (Lifecycle values are lower-case) instead of on the parent check. Apply:
  import `QUEUED` and friends from `contracts.py` when building snapshots.

## S11 · 2026-10-28

- **Check the line a stale note names before planning its edit.** The
  handoff carried "change the map's '(not yet built) will read' to 'reads'",
  but `GLOSSARY-MAP.md` already said "reads" (DB-G, S5); the stale wording
  had moved to `README.md:202`. Apply: grep for the quoted words across the
  repo, not only in the file the note names, before you put an edit in front
  of Rich.
- **Hand-make a partial item from a committed one.** Reading a committed
  issue (`gh issue view … --json body,labels`) showed both halves of
  squadra's GitHub encoding: the Origin as a body comment, the commit marker
  as the `squadra:committed` label. Copying the body without the label gave
  a partial item squadra recognised at once. Apply: when you need a board
  state no tool makes, copy a real item and remove exactly the part the
  contract says marks the difference.
- **Ask the ruling before the run that could change it, and say so.** Rich
  ruled on T1 before the sandbox look. The ruling held either way, but a
  "wrap up if clean" option made the dependency visible. Apply: when a
  decision and a test are in the same session, offer the option that waits
  on the test.
