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

- **Board `/ask-<advisor>` skills are user-invoke-only.** They set
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
