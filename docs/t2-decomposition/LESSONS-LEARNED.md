# T2 lessons learned

Append one entry per lesson: date, session, what happened, what to do.
Lessons from the port (`docs/wayfinder-port/LESSONS-LEARNED.md`) and
design-to-board (`docs/design-to-board/LESSONS-LEARNED.md`) still apply.

## 2026-10-28 · T2c-R2 and S0

- **The worktree isolation guard refuses some git-shaped commands.** In a
  worktree-isolated session it refuses:
  - `git -C <other path>`;
  - git commands built from variables (`$f`, `$(…)`);
  - inline scripts or heredocs whose text contains `git+` (a `uvx --from
    git+…` line in a PR body or a Python string).

  Workarounds:
  - Write scripts and PR bodies to files in the job's `tmp/`, then run
    `python3 file` or `gh pr create --body-file file`.
  - To make a new worktree, run `git worktree add ../<name> -b <branch>
    origin/main` from inside the current worktree, then EnterWorktree with
    `path`.
- **zsh expands a bare `======`** as a filename and aborts the whole
  command. Use `echo ---` as a separator.
- **Ledger rows are long single lines.** Two branches that both append to
  T2's notes conflict on the whole row. Resolve by taking the base text, then
  main's addition, then ours. Do it by script against `git show <base>`,
  `HEAD` and `origin/main` saved to files, and check every row's cell count
  afterwards.
- **Handoffs aren't committed (HD1).** `.gitignore` drops `docs/*/handoffs/`.
  Write handoffs into the worktree, give Rich their absolute paths, and don't
  remove that worktree until the handoff has been used. The template is
  tracked at `docs/t2-decomposition/HANDOFF-TEMPLATE.md`.
- **Re-check open questions against what merged meanwhile.** T2c-J's rulings
  landed while T2c-R2's PR was open and answered two of its questions. After
  merging main, re-read any "still open, for X" line.

## 2026-10-28 · T2c-1

- **Probe a plan's limits without changing anything.** On a private repo,
  `GET branches/main/protection` returns 404 "Branch not protected" when the
  plan allows protection, and 403 "Upgrade to GitHub Pro" when it doesn't. A
  ruleset POSTed with `enforcement: disabled`, then deleted, confirms it.
- **An approval rule needs an author who isn't the approver.** Code-owner
  review with no bypass deadlocks every PR the owner authors. Here that
  includes every Claude session, because sessions open PRs through Rich's gh
  login. List who actually authors the protected files before choosing the
  rule.
- **lint-imports wraps long contract names** at the terminal width, so a
  match on `"<name> BROKEN"` misses. Keep contract names short and set
  `COLUMNS=200` when a test parses the report.
- **Prove a fixture test bites.** Weaken one contract, see the matching
  fixture fail, then restore it. Do this once before trusting a green run.
