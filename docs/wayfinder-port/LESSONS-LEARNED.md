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
