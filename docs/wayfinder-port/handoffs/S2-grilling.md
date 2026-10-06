# Handoff: S2 · Grilling skill (outline, issues, feedback, then build)

Rich starts a fresh `claude` session in the worktree and pastes this whole file
as the first message.

## Context

You are continuing the wayfinder + domain-modeling port on branch
`feat/wayfinder-domain-modeling` in `rinman24/claude-skills`. Work in the
existing worktree for that branch at
`.claude/worktrees/wayfinder-domain-modeling` (or create one from the branch);
never commit to main.
The marketplace is `claude-skills` (renamed from `my-skills` in PR #2); see
the ledger's "Repo facts" for install, update and validate commands.

Grilling comes first because wayfinder and domain-modeling both build on it:
wayfinder's default ticket type is "call grilling + domain-modeling", and
upstream `grill-with-docs` is literally those two skills chained.

Read first, in order:
1. `docs/wayfinder-port/LEDGER.md` (status, budget, session protocol)
2. `docs/wayfinder-port/LESSONS-LEARNED.md`
3. `plugins/local-backlog/` and `docs/local-backlog-plugin-install-runbook.md`
   (the house conventions a new plugin must match)
4. `.claude-plugin/marketplace.json` and `README.md`

Upstream reference: https://github.com/mattpocock/skills, pinned at commit
`6fd9479` (2026-10-06). Shallow-clone it into your job temp dir; don't vendor it
into the repo. Upstream files for this unit:

- `skills/productivity/grilling/SKILL.md`: the core skill
- `skills/productivity/grill-me/SKILL.md`: user-invoked wrapper (one line)
- `skills/engineering/grill-with-docs/SKILL.md`: grilling + domain-modeling
- `docs/productivity/grilling.md`, `docs/productivity/grill-me.md`,
  `docs/engineering/grill-with-docs.md`: human docs; their "Common questions"
  sections hold the author's known issues
- `.out-of-scope/question-limits.md`, `.out-of-scope/native-question-tool.md`:
  requests the author rejected, with his reasons
- `CHANGELOG.md`: grep for `grill` for behaviour changes over time
- `.agents/invocation.md`: user-invoked vs model-invoked convention

## This session's unit

Ledger items: G1, G2
Estimated work: ~75K tokens (budget: under 100K total, hard stop at 120K)

Work in this order and do not skip the stop in step 3.

1. **Outline Matt's approach to grilling.** Cover how it works: the design
   tree, rounds, the frontier, numbered questions with a recommended answer
   each, facts found by subagents and never asked of the user, decisions left
   to the user, done when the frontier is empty, and confirm before acting.
   Also cover how `grill-me` and `grill-with-docs` wrap it and how each one is
   invoked. Keep it short; Rich already has the gist from S1.
2. **List the issues the author raised.** Pull them from the docs pages'
   "Common questions", the two `.out-of-scope/` files, and the CHANGELOG. For
   each one give a single line and its source path. Separate "known defect" from
   "request the author rejected", because Rich may want the rejected ones.
3. **Stop and ask Rich for feedback.** Ask what to keep, change, add or drop
   before you write any skill file. Questions worth raising, without deciding
   them:
   - Name and namespace. A claude.ai-synced `anthropic-skills:grill-me` is
     already installed; a plugin skill here would be `grilling:grilling`.
   - Do we want a `grill-me`-style user-invoked wrapper, or only the
     model-invocable core?
   - The known complaint about verbose questions (decision fatigue).
   - Question caps and the native `AskUserQuestion` UI, which the author ruled
     out.
   Record Rich's answers as decisions in the ledger before building.
4. **Build it**, only after Rich has responded, and only if the session is under
   ~70K at that point (otherwise go straight to wrap-up and write an S3 handoff
   for this step). Match `local-backlog`:
   `plugins/grilling/.claude-plugin/plugin.json`,
   `plugins/grilling/skills/grilling/SKILL.md`, a marketplace entry, a README
   section, and `docs/grilling-plugin-install-runbook.md` (install commands use
   `grilling@claude-skills`, mirroring the local-backlog runbook). Run
   `claude plugin validate .`. Credit upstream (MIT) in the SKILL.md or README.
   The installed `claude-skills` marketplace reads from GitHub, so branch-only
   changes won't show up through it. Find a way to load the plugin from the
   working tree for a smoke test (check `claude --help` for a plugin-directory
   flag), and record what worked in `LESSONS-LEARNED.md`.

## Decisions already made

- No dependency on `setup-matt-pocock-skills` (ledger: Goal).
- Handoffs are plain prompt files; there is no `/handoff` plugin (ledger: How
  sessions hand off). The handoff plugin was removed on main in PR #1.
- One plugin per skill in this marketplace (existing repo convention).
- Marketplace name is `claude-skills` (PR #2); `my-skills` is gone.

## Out of scope for this session

- domain-modeling, wayfinder, grill-with-docs (grilling only; note anything
  that affects them in the ledger's "Inputs to triage").
- research, prototype, to-spec, to-tickets.

## Suggested skills

- `anthropic-skills:skill-creator` (when writing the SKILL.md in step 4)

## Wrap-up

Follow the "End" steps of the session protocol in the ledger, including writing
the next handoff prompt and telling Rich its path.
