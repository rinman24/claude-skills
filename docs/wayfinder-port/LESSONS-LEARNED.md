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
