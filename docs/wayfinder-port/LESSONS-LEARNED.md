# Lessons learned

Append-only. One entry per lesson: what happened, and how to apply it next time.
Newest at the bottom.

## S1 · 2026-10-06

- **Matt's skills get their per-repo config from `setup-matt-pocock-skills`.**
  Wayfinder reads "Wayfinding operations" from `docs/agents/issue-tracker.md`;
  other skills read `docs/agents/domain.md`. Apply: when porting a skill, grep
  it for `docs/agents/` and `/setup-matt-pocock-skills` and replace each
  reference with something this repo owns.
- **Upstream docs pages are the best source of known defects.** Each
  `docs/engineering/<skill>.md` has a "Common questions" section listing real
  user-reported failures. Apply: read the docs page, not just `SKILL.md`,
  before designing changes.
- **`EnterWorktree` auto-names the branch `worktree-<name>`.** Apply: rename
  with `git branch -m` straight after creating it.
- **Budget numbers need reconciling up front.** "Stay under 100K" and "120K
  units" conflict. Apply: 100K target, 120K hard ceiling, ~80K of planned work
  per unit.
- **Plain `git push` fails here (HTTPS origin, no git credential helper).**
  `gh` is logged in with protocol `ssh`, but `origin` is HTTPS. Apply: push with
  `git -c credential.helper= -c credential.helper='!gh auth git-credential' push`.
- **Worktree-isolated sessions refuse commands that `cd` outside the worktree.**
  A compound command that wrote to the memory dir and then ran git was rejected.
  Apply: write files outside the worktree with the Write tool, and run git as a
  separate command from the worktree root.
- **This session can't touch the main checkout's git.** `git -C <main repo>` is
  refused by the worktree guard, so local `main` can't be fast-forwarded from
  here. Apply: rebase onto `origin/main` after a fetch, and ask Rich to run
  `git pull --ff-only` in his main checkout.
- **Rebasing a pushed branch needs a force-push, which sessions don't do.**
  Apply: after a rebase, hand Rich the `git push --force-with-lease` command,
  or avoid rebasing once a branch is pushed and merge `origin/main` instead.
- **The install `@` suffix is the marketplace `name` field, not the repo name.**
  PR #2 renamed it from `my-skills` to `claude-skills` so the two match, but
  they are set independently. Apply: any install or update command, runbook or
  handoff uses `<plugin>@claude-skills`; check `marketplace.json` if in doubt.
- **`main` moved twice during S1 (PRs #1 and #2).** Rich hadn't force-pushed
  the branch between them, so rebasing again was cheap. Apply: fetch and check
  `git log <old-base>..origin/main` at the start of every session, and rebase
  (or merge) before writing anything that describes the repo.
- **Scripts whose text mentions git get blocked by the worktree guard.** Apply:
  make multi-file doc edits with the Edit tool, then commit in a separate,
  git-only command.
- **Rich's `!` commands run under the same worktree guard.** A `!` git command
  aimed at the main checkout was refused. Apply: anything touching
  `~/Code/claude-skills` itself (e.g. `git pull --ff-only` on main) goes to Rich
  as a command for a normal terminal outside Claude, and any push command handed
  to him includes the `gh` credential helper form above.

## S2 · 2026-10-06

- **`claude --plugin-dir <path>` loads a plugin from the working tree for one
  session.** Headless works too: `claude -p --plugin-dir plugins/grilling
  "/grilling <topic>"` invoked the skill and printed round 1. Apply: smoke-test
  every branch-only plugin this way before asking Rich to install it.
- **The worktree guard refuses a nested `claude` inside any compound
  construct.** `cd <scratch> && claude …`, `> file` redirects and pipes were
  all rejected as "might run git"; so was `git -C <scratch>`. Only the plain
  command from the worktree root ran. Apply: run headless smoke tests as one
  bare `claude -p …` from the worktree root and check `git status` afterwards
  as a separate command.
- **Headless `-p` covers one turn only.** Behaviour that needs a reply
  (clarification, the confirmation gate) can't be checked that way. Apply:
  list those as interactive runbook steps for Rich instead of marking them
  verified.
- **The session started outside the branch's worktree.** The handoff's
  `.claude/worktrees/wayfinder-domain-modeling` didn't exist; the session
  opened in another checkout on `planning-skills`. Apply: the handoff's first
  step is `git worktree list`; if the branch has no worktree, run
  `git worktree add .claude/worktrees/wayfinder-domain-modeling
  feat/wayfinder-domain-modeling` and then EnterWorktree with that path.
- **Rich's installed `anthropic-skills:grill-me` is upstream's old
  one-at-a-time text.** Apply: when porting, check `~/.claude/skills/synced/`
  for an older synced copy of the same skill and plan its retirement.

## S3 · 2026-10-06

- **The advisors' `/ask-<advisor>` skills are user-invoke-only.** They set
  `disable-model-invocation: true` (board Phase 2 decision) and are generated
  from `~/Code/board` templates, so editing `~/.claude/skills/ask-*/SKILL.md`
  gets overwritten. Apply: when Rich asks for an advisor mid-session, follow
  the skill's steps by hand (Agent with `subagent_type: board-<slug>`, relay
  verbatim, write the session file with the Write tool). A skill that needs an
  advisor calls the `board-<slug>` agent directly.
- **Advisor consults are expensive in context.** Each verbatim relay plus its
  session file cost ~8–10K tokens in the main session, and a decision round
  with two consults pushed S3 past the build line. Apply: when a handoff plans
  "outline, decide, build" in one session, budget ~10K per expected advisor
  consult, or plan the build for the next session from the start.
- **Advisor answers can change a design's structure, not just its wording.**
  Juval split lookup from provenance (a new file); Eric found that Juval's
  Retire verb conflated two concepts and removed it. Apply: put a design to the
  structural advisor first, then the result to the language advisor, and
  record both session files in the ledger next to the decision.

## S4 · 2026-10-06

- **A headless smoke test that needs a write must use `--permission-mode
  acceptEdits`.** It is still one bare `claude -p …` from the worktree root, so
  the worktree guard accepts it. Apply: add the flag for any skill whose smoke
  test checks for files written.
- **An advisor in the loop makes smoke tests non-deterministic.** The first
  run's terms (Site, Campus) collided with GenShift's real vocabulary, so Eric
  objected and, correctly, nothing was written. Apply: smoke-test the write
  path with a term from this repo's own domain, and pre-accept wording-only
  changes in the prompt ("if Eric only sharpens the wording, I accept it").
  Keep the refusal run too: it tests a different branch.
- **The nested `claude -p` sees this repo's CLAUDE.md and memory.** It knew it
  was the S4 smoke test and said so in its reply. Apply: harmless, but don't
  read its meta-commentary as evidence the skill told it to.

## S5 · 2026-10-06

- **A skill with no advisor in the loop smoke-tests deterministically.** Both
  `adr` runs did exactly what the skill says on the first try, and the
  gate-pass case needed only `--permission-mode acceptEdits`. Apply: when a
  handoff budgets a build at ~35K, a plugin without advisor calls really does
  fit; save the slack for the interactive cases the runbook hands to Rich.
- **Write the smoke-test decision so every gate is visibly answered.** The
  passing prompt named the alternatives, the reason, the cost of reversal and
  why a reader would be surprised; the failing one said "nobody suggested
  anything else". Apply: smoke-test prompts for gated skills should leave the
  model nothing to infer, so a pass or fail is the skill's doing.
- **The generated ADR ran to six sentences against upstream's "1-3".** Not
  wrong (no padded sections), but the template's sentence count is a soft
  guide to the model. Apply: if Rich wants ADRs tighter, make the limit a rule
  in SKILL.md rather than leaving it in the template comment.

## S6 · 2026-10-06

- **Three verbatim advisor relays filled the session.** Each consult cost
  ~10K (answer read, session file written, answer relayed), and S6 ran three,
  so Rich stopped it before the layout. Apply: plan at most two consults per
  session; if a third is needed, record the decisions and hand it to the next
  session with the exact prompt context listed.
- **Check the user's framing words against upstream before consulting.** Rich's
  "no Work mode; squadra implements Work" read as "never build", but
  upstream's Work mode is HITL deciding. Both advisors spent their first
  blocking question on it, and Rich's clarification then reversed round-1 Q1
  (GitHub → local board). Apply: when an answer reuses an upstream term in a
  new sense, ask one clarifying question before spending an advisor consult.
- **A later answer can supersede an earlier one in the same session.** WD2
  supersedes round-1 Q1. Apply: record the supersession in the decision
  itself so S7 doesn't build the stale answer.
- **A `cd` outside the worktree persisted the shell's cwd.** A Bash call that
  started with `cd ~/Code/board-knowledge/...` left the session there (earlier
  `cd`s into the scratch dir were reset). Apply: use absolute paths for
  out-of-worktree reads; never lead a command with `cd` outside the worktree.
- **Facts an advisor asks for are often a grep away.** Eric's "which word does
  Juval use" was settled by counting terms in `board-knowledge/raw/juval-lowy`.
  Apply: answer an advisor's factual blocking question yourself before putting
  the decision to Rich.

## S7 · 2026-10-06/07

- **A `cd` into board-knowledge moved the session's cwd again, despite the S6
  lesson.** It was hidden inside a `for` loop. Apply: in any command touching
  another repo, use only absolute paths; no `cd` anywhere in the command.
- **Background advisor consults overlap with grilling rounds.** Launching
  Juval (Q18) as soon as the round went out meant his answer was ready before
  Rich replied. Two consults launched in parallel on the same question (Q10)
  cost no extra wall-clock. Apply: start a consult the moment its question is
  fixed, and present the rest of the round while it runs.
- **Parallel consults on one question surface conflicts worth a round.** Juval
  and Eric agreed on most of Q10 but differed on row identity (Q15), which
  became Rich's decision. Apply: give both the same verbatim inputs, then
  present "where they agree" plus one question per difference.
- **Four consults pushed the session well past the two-consult guideline.**
  Rich asked for the extra two. Checkpointing the ledger (commit `662cfe8`)
  before launching them kept confirmed decisions safe. Apply: when the user
  asks for consults beyond the budget, commit a ledger checkpoint first.
- **Advisors' factual blocking questions were answered with `gh` in one
  call.** squadra PR #41 merged state and its glossary on origin settled
  Eric's question; a read-only subagent reading squadra answered Juval's.
  Apply: same as S6, and note the answer under the question in the session
  file.
- **Parallel sessions on one branch would conflict in `LEDGER.md`.** S8 and
  S11 run in parallel, so S11 works on its own branch and worktree and touches
  only its W5 row and one session-log row. Apply: give every parallel
  session its own branch, and keep shared-file edits to its own rows.

## S8 · 2026-10-07

- **A handoff's glossary plan can predate the format's own rules.** The plan
  had "context: architecture" and a squadra copy row at the root. Both broke
  the one-context-per-`GLOSSARY.md` rule. They also failed Eric's test,
  because later decisions (WD17, WD21, WD26) had put those words into
  wayfinder. Apply: before a Settle, check each row's context against where
  the term is actually used today, not where an older ruling put it.
- **Eric's Lookup test makes a good acceptance check, and awk can run it.**
  The test is that every rejected form returns exactly one enforced answer in
  the context that uses it. Apply: after any write to `GLOSSARY-SETTLED.md`,
  simulate Lookup over the relevant forms with a short awk loop over the table.
- **Context descriptions and `GLOSSARY-MAP.md` lines are glossary writes too.**
  They needed a second, short Eric consult, and he corrected a fact (squadra
  builds from the board, not from the design document). Apply: send the
  description lines in the same consult as the terms.
- **Two consults (one resumed with SendMessage) kept S8 well under budget.**
  Apply: continue the same `board-eric` agent for follow-ups rather than start
  a new one; it keeps its context, and the follow-up was cheap.

## S11 · 2026-10-07

- **Under `--plugin-dir`, a plugin's skill is `/<plugin>:<skill>`, and a bare
  `/<skill>` may not resolve.** The first headless run of `/prototype` came
  back "not a command" and answered from the model alone; a settled-design
  refusal looked right but wasn't the skill's doing. Two writing runs found
  `prototype:prototype` by themselves. Apply: smoke-test with the namespaced
  form (`/prototype:prototype …`), and read the nested reply for "isn't a
  command" before counting a pass.
- **A `cat >> … <<EOF` plus a `python3` heredoc in one Bash call was refused
  by the worktree guard** (it couldn't verify the call stays in the worktree).
  Apply: append to docs and JSON with the Edit tool, as S1 said; keep Bash for
  single plain commands.
- **Smoke runs that write prototype files drop them into the worktree**
  (`docs/…prototype.html`, `prototypes/…`). Apply: check `git status
  --untracked-files=all` after each run, inspect, then delete them before
  committing.
- **A nested headless run can't execute shell checks or open a browser** (no
  approval in `acceptEdits`), so it reviews its prototype by reading it.
  Apply: grep the generated file for the structural rules (switcher keys,
  `replaceState`, input guard, pure module, no external URLs), and leave
  "opens and renders" to Rich's interactive steps.
- **A plugin with no advisor ran three parallel headless smoke runs in about
  the time of one.** Apply: launch independent smoke runs in the background
  together, and read the results as they arrive.

## S9 · 2026-10-07

- **A plain `cd plugins/wayfinder && grep …` moved the session's cwd too.**
  This was the third time, and this one stayed inside the worktree. Apply: no
  `cd` at all; use `grep -r … plugins/wayfinder` from the root.
- **Launching the Eric consult first, in the background, cost no
  wall-clock.** The format files were written while he reviewed, and Rich's
  answer took one AskUserQuestion with three questions. Apply: when a build
  needs new terms, consult at the start with every term batched, and write
  the parts that don't depend on the wording in the meantime.
- **A proposed `_Avoid_` form can collide with an existing rejected form.**
  "Task" was already rejected for Errand. A second row would make Lookup
  return two answers, and domain-modeling's step 2 refuses to settle it.
  Apply: run the Lookup awk test on every proposed Rejected form *before*
  writing the rows, and drop any form already settled.
- **Eric checks a context's own intro line against new terms.** Settling
  Cleared made "clears the fog" in `GLOSSARY.md` ambiguous. Apply: when
  settling a verb or state, grep the context's prose for other senses of the
  same word and send those lines in the same consult.
- **The handoff's budget held.** One consult and the build fit well under
  80K. Apply: a plugin build of three skill files plus the standard
  manifest, README and runbook is about 60–70K with one consult.

## S10 · 2026-10-07

- **A hand-seeded "should pass" map is what found the real defect.** The
  failing map failed for the seeded reasons, plus check 4. Only the clean map
  showed that check 4 refused everything. Apply: whenever a skill has a
  gate, smoke-test one input that should obviously pass as well as one that
  should fail. A gate that also rejects the clean input is broken.
- **A gate worded "in settled terms" needs both a source and a context.**
  `GLOSSARY-SETTLED.md` holds only contested rulings, and a map's destination
  may sit outside every listed context. Apply: when a skill checks words
  against the glossary, name the operation (`Lookup`), the outcome that fails,
  and how the context is chosen.
- **Give the first ticket on the frontier a research Kind so Resolve fits in
  one headless turn.** A grilling ticket would stop at its questions. Apply:
  when the Begin prompt lists tickets, make the first one research, and leave
  grilling-ticket Resolve for an interactive check.
- **The map format has nowhere to record a service's Layer or Encapsulates.**
  Publish found them in a ticket Resolution because the seed put them there.
  Apply: W6 or a later revision might give the map a Services list. Until
  then, a grilling ticket that introduces a service should state its layer
  and what it encapsulates in the Resolution.
- **Running headless smoke runs in parallel held up again (S11).** Four ran
  side by side; dependent runs (Resolve on Begin's map) went once their input
  existed. Reading each run's reply and the files it wrote is what costs
  context, not waiting. Apply: the ~40K estimate for a smoke unit holds only
  if replies are read once and files are listed with `tail -n +1`, not
  re-read.
- **A "stop early" exit placed after an expensive step isn't early.** Begin's
  "no map needed" check sat after two grilling rounds, so Rich's tiny ideas
  were grilled first. The headless smoke plan skipped D2 as needing a second
  turn, but D2's correct behaviour is a one-turn stop, so headless could
  have caught it. Apply: when listing checks as "interactive only", ask
  whether the *expected* behaviour fits in one turn; if so, run it headless
  too.
- **A real map found what toy maps didn't.** Rich's Costco map had increments
  decided by the revised ticket, so Revise's missing `Decided by` repoint
  showed up. Fixing it and re-running then showed a second gap (replacement as
  an errand). Apply: for an operation that rewrites cross-references, test on
  a map where the target is referenced from every kind of place (`Blocked
  by`, `Decided by`, Decisions so far), and re-run after each fix: one fix can
  uncover the next. Copy the real map into the worktree's `.scratch/` for the
  headless re-run, then delete it.

## S12 · 2026-10-08

- **Two `--plugin-dir` flags load two branch plugins in one headless run.**
  `claude -p --plugin-dir plugins/wayfinder --plugin-dir plugins/prototype
  --permission-mode acceptEdits "/wayfinder:wayfinder <map>"` let wayfinder's
  Skill call find `prototype` from the working tree. Apply: when one skill
  calls another, load both with `--plugin-dir` so the test exercises the
  branch versions, not whatever is installed.
- **A skill that waits for the user is easy to test headless.** The correct
  behaviour, a hand-over that stops, fits in one turn, so the headless run
  checked exactly the part that matters (no pick, no close). Apply: for
  "hand over and wait" skills, test the hand-over headless and leave only
  the reply half to Rich.
- **"Next to what it prototypes" meant the map folder.** With no app in the
  repo, `prototype` put its HTML file in `.scratch/wayfinder/<map>/`, inside
  the committed map. Apply: when a called skill places its own files, check
  where they landed against the caller's write rules; record the gap rather
  than editing the called plugin (out of scope without Rich's say).
- **The unit came in under its ~25K estimate.** It was one skill edit, one
  format line, the runbook, the README and one headless run. Apply: a wiring
  unit between two built plugins is ~20–25K with a single smoke run.

## Q1 · 2026-10-08

- **A queue walk with pasted transcripts costs far more than its estimate.**
  Q1 was planned at ~45–65K (W7 plus the walk) and reached ~150K after W7
  and three queue items; the bootstrap paste alone was several thousand
  tokens. Apply: plan two or three interactive items per session, and ask
  Rich to paste only the reply that decides the check.
- **Check the skill's order before failing a runbook step.** Step D 2
  expected Eric's objection, but the skill's own challenge steps run first
  and caught the collision before Eric was called. The behaviour was right
  and the runbook was too narrow (W8.1). Apply: when an expected actor
  doesn't appear, read the skill's sequence before calling it a defect.
- **"That's the only batch" exercises a whole bootstrap cheaply.** Trimming
  the batch list to one batch and then asking for the final pass and Settle
  covered every BOOTSTRAP step in one session. Apply: for multi-stage
  skills, cut the input to the smallest case that still reaches every stage.
- **Test an agent's absence by moving its file aside.** `board-eric` is a
  user agent (`~/.claude/agents/board-eric.md`); `--bare` would drop it but
  needs API-key auth. Apply: `mv` the file out of `~/.claude/agents/` for
  the check and put it back right after.
- **Read the written files, not only the announcement.** The billet
  bootstrap's summary said every wording was one Rich accepted; the
  transcript showed two writes he never approved (W8.2). Apply: verify a
  check against the files and the transcript, not the skill's own summary.

## Q2 · 2026-10-08

- **Asking for only the deciding reply kept a five-check walk near ~95K.**
  Rich pasted the final reply of each check, and the session read the
  written files and `git status` itself. Apply: keep doing this; it is the
  main cost lever in a queue walk.
- **A runbook prompt can fail a repo-fit judgement that is correct.** The adr
  step 1 decision (an event store) was refused in billet, which has none.
  Apply: when a runbook step reuses another step's prompt in a different
  repo, check that the prompt fits that repo before handing it over (W8.5).
- **Build the missing test bed instead of deferring the check.** prototype
  Step D 6 had waited since S11 for "a repo with a web UI"; a ~60-line Flask
  app with an `APP_ENV` switch, smoke-tested with Flask's test client, took
  one short chunk. Apply: when a check is deferred for lack of a fixture,
  price building a toy one before deferring again. With no Node on the Mac,
  `uv` + Flask was the shortest path.
- **Toy sample data gets audited by the skill under test.** prototype flagged
  that site-dash's hourly export and cycle count contradict its daily totals.
  Apply: make toy data internally consistent, or the check spends words on it.
- **A user-invoked advisor skill can't be called by the session.**
  `ask-juval` sets `disable-model-invocation`, so a consult has to be Rich
  typing it, after the session has read the facts into context (the skill
  passes conversation facts verbatim). Apply: write consult handoffs as "load
  these facts, then Rich types this exact line".
- **zsh trips on unquoted globs and `=word`.** `--include=*.md` and `echo
  =====` both failed. Apply: quote globs, prefer `rg -g`, and don't lead a
  word with `=`.

## Q3 · 2026-10-08

- **A pasted slash command is plain text.** Rich's first `/ask-juval` arrived
  as pasted content, so the skill didn't load; he then typed it and it ran.
  Apply: when a consult line arrives as a paste, say so in one line and ask
  him to type it; don't run the skill's steps by hand.
- **The user's factual answer can reframe the advisor question.** The handoff's
  `/ask-juval` line predated Rich's answer (never run, several GitHub boards,
  ADO dropped, a possible second VM), and those facts drove Juval's "now".
  Apply: after the pre-consult question, add the answer to the consult line
  as facts only, with no opinion.
- **Read the consumer, not only the config.** The scope config looked like a
  claim filter, but `supervisor.py:486` folds it into `_predecessors_done`
  as `BLOCKED`. Quoting that code gave Juval his item 4. Apply: when tracing a
  setting for a consult, grep where it is read and quote that too.
- **Answer the advisor's caveat in the session file.** Juval couldn't see
  whether anything outside squadra sets `FLEET_EPIC_IDS`; one grep of
  `~/Code` settled it. Apply: same as S6/S7, and put the answer under
  "Blocking questions".

## S13 · 2026-10-08

- **Tightening a rule can break a runbook step that relied on the old slack.**
  W8.2's first draft ("approved after seeing Eric's verdict") would have
  turned Step D 1's one-turn write, which accepts Eric's sharpening in
  advance, into two turns. Apply: after tightening a skill rule, re-read
  every runbook step for that skill against it, and re-run the one-turn steps
  headless (here Step D 1 still passed, now announcing `you approved in
  advance`). Record the reading as a build interpretation (MD-B6).
- **Three headless checks in parallel kept a seven-item fix unit near ~40K.**
  The two that needed Eric ran side by side in separate scratch repos under
  the job temp dir; the no-Eric one ran after them, with `board-eric.md`
  moved aside under a `trap` that put it back. Apply: run independent
  headless checks concurrently, and isolate the agent-absence check so it
  can't overlap a run that needs the agent.
- **A concrete example in the skill fixes a length problem better than an
  adjective.** "One line" was already in adr's `SKILL.md`; Q2 still got ~8
  lines. Spelling out what the line holds, what it leaves out, and a sample
  gave a one-line offer on the first headless run. Apply: when output
  overruns a stated limit, show the target shape, not a stronger word.

## W9 · 2026-10-08

- **A handoff's "already on main" can be wrong.** W9's handoff said
  `prototype` shipped to main via PR #3; `gh pr list` showed PRs #3 and #4
  had base `feat/wayfinder-domain-modeling`. The diff against `origin/main`
  was the first sign. Apply: before writing a PR body or install commands,
  check `gh pr list --state all --json number,baseRefName` and
  `claude plugin list`, not the handoff's history.

## Q4 · 2026-10-08

- **A scripted line can land at the wrong prompt when the skill asks a
  multiple-choice question.** The bootstrap showed its batch list as a
  question with a recommended option, so Rich's "that's the only batch" line
  arrived at the batch 1 approval prompt instead, and the skill took it as
  approval (W8.11). Apply: script interactive lines as "when you see X, say
  Y, or pick 'Other' and type it", and expect a question widget to take the
  turn the script assumed.
- **A short script beats reading a settled table by eye.** Matching every
  `GLOSSARY.md` `_Avoid_` line to its row's Rejected column took one Python
  heredoc and covered all 27 rows. Apply: verify bulk writes with a
  cross-check script, then read only the entries that changed after approval.
- **A bootstrap test in a real repo finds real things.** The billet run
  surfaced an ADR-0005 gap (`az vm create`'s implicit NSG, VNet, NIC) and an
  `Up` code gap. Apply: before dropping a scratch branch, copy any finding
  about the target repo into Rich's queue so it outlives the branch.
- **Ask for the deciding reply, accept the whole transcript.** Rich pasted
  the full bootstrap (~10K) instead of two parts; it still fit, and it showed
  W8.11, which the two parts would have hidden. Apply: for a multi-stage
  check, the full transcript is worth its cost once; keep single-reply pastes
  for single-turn checks.
