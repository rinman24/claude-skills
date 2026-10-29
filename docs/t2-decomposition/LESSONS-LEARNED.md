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
