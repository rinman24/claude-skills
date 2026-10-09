# Lessons learned

Append-only. One entry per lesson: what happened, and how to apply it next
time. Newest at the bottom.

design-to-board's lessons (`docs/design-to-board/LESSONS-LEARNED.md` on
`feat/design-to-board`) apply here too, especially: `/ask-juval` is typed by
Rich, and an advisor consultation costs ~25–30K of a session.

## H1

- **Separate artifacts by lifetime before choosing a location.** Juval
  settled HQ1 by asking how long each artifact must live: the ledger is the
  record (permanent), the handoff a message (lives as long as the effort's
  worktree). Apply: when a file's home is in question, match its lifetime
  first, and don't mix lifetimes in one directory (the template left
  `handoffs/` so the whole directory could be ignored).
- **A root `.gitignore` rule reaches other efforts' branches.** Ignoring
  `docs/*/handoffs/` on `main` will ignore new handoffs on
  `feat/design-to-board` once it merges `main`. Apply: when a repo-wide
  rule changes another effort's behaviour, put a follow-up in Rich's queue
  rather than editing that branch.
- **`claude-skills` installs from GitHub's default branch.** An unmerged
  plugin can't be installed as `<plugin>@claude-skills`; try it with
  `claude --plugin-dir plugins/<plugin>`, headless with
  `--permission-mode bypassPermissions` from a scratch dir (default
  permissions block a headless skill's reads and writes). Apply: plan
  "install from the marketplace" as a post-merge unit.
- **The advisor relay plus three rulings fit comfortably.** Juval's
  consultation cost ~28K inside the agent and little here; HQ2 and HQ3 took
  one question each because Juval's answer had already framed them.
- **The skill's ledger check earns its keep.** Writing H2 by following
  SKILL.md, step 3 caught that the ledger said "PR opened" without the PR
  number. Apply: run `/handoff` after the PR exists, so the ledger can name it.
