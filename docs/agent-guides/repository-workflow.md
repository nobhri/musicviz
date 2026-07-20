# Repository and Git Workflow

## Before changing files

1. Run `git status --short --branch`.
2. Confirm the branch belongs to the current task and identify existing work.
3. Identify the current roadmap phase.
4. Make the smallest coherent change that advances that phase.
5. Avoid unrelated refactoring and explain assumptions affecting appearance or
   file format.

## After changing files

1. Run relevant tests.
2. Run the smallest useful render check when media behavior changes.
3. Report changed files and verification commands.
4. State remaining limitations honestly.

Do not add large media fixtures without explicit approval.

## Git and GitHub

- Run networked `gh` commands and Git operations such as push, pull, and fetch
  with host/escalated permissions. A sandbox may lack keyring or network access.
- Retry sandboxed authentication or network failures with host permissions
  before asking the user to re-authenticate.
- Use a new feature branch for each independent task or session.
- Start from the latest `main` and use `main` as the pull-request base.
- Do not continue a previous session's branch unless the user asks.
- If necessary, preserve existing work before switching branches, update with
  `git pull --ff-only origin main`, create the branch, and reapply the work.
- Stage only task-related files. Never broadly stage unrelated changes.
- Never commit directly to `main` and never force-push.
- Prefer an annotated tag for a completed phase, such as `phase-1-complete`.

If the directory is not a Git repository, report that rather than pretending
the branch workflow was performed.
