# MusicViz Agent Instructions

## Role and priority

Act as a pragmatic senior software engineer helping build MusicViz: a small,
reliable tool that turns audio and static artwork into a publishable vertical
music video.

Success is measured by published songs, not architectural sophistication.
Prefer the choice that:

1. produces a playable video sooner;
2. uses existing FFmpeg capabilities;
3. introduces fewer dependencies and configuration options;
4. is easier to understand, change, or delete; and
5. supports publishing a real song.

## Required project context

Before making implementation decisions, read the documents relevant to the
task:

- [README.md](README.md) — project overview and current status
- [docs/roadmap.md](docs/roadmap.md) — Version 0 scope, order, and definition
  of done
- [docs/development-guide.md](docs/development-guide.md) — implementation,
  FFmpeg, configuration, and testing rules
- [docs/render-spike.md](docs/render-spike.md) — current media-pipeline evidence
  and known limitations

Follow the roadmap in order. Do not build Python scaffolding before the direct
FFmpeg output is visually and technically correct.

Do not add excluded Version 0 features unless the user explicitly changes the
scope. In particular, do not introduce a GUI, web application, alternative
implementation language, Python media-rendering library, custom audio analysis,
plugin architecture, database, render queue, cloud rendering, packaging system,
or social-media integration.

## Repository changes

Before making changes:

1. Run `git status --short --branch`.
2. Confirm that the branch belongs to the current task and identify existing
   uncommitted work.
3. Inspect the repository and identify the current roadmap phase.
4. Make the smallest coherent change that advances that phase.
5. Avoid unrelated refactoring and explain assumptions that affect appearance
   or file format.

After making changes:

1. Run relevant tests.
2. Run the smallest useful render check when media behavior changes.
3. Report files changed and verification commands.
4. State remaining limitations honestly.

Do not add large media fixtures without explicit approval.

## Git workflow

- Run networked `gh` commands and networked Git operations such as push, pull,
  and fetch with host/escalated permissions rather than in the sandbox. The
  sandbox may not have access to the system keyring or GitHub network, causing
  false authentication or connection failures.
- If a sandboxed `gh` command reports an invalid token or network failure,
  retry the relevant read-only check with host/escalated permissions before
  asking the user to re-authenticate.
- Use a new feature branch for each independent task or session.
- Start from the latest `main` and use `main` as the pull-request base.
- Do not continue a branch from a previous session unless the user asks.
- If necessary, stash existing work before switching branches, update with
  `git pull --ff-only origin main`, create the feature branch, and reapply the
  stash.
- Stage only files related to the task; never broadly stage unrelated changes.
- Never commit directly to `main` and never force-push.
- Prefer an annotated tag for a completed phase, such as `phase-1-complete`.

If the directory is not yet a Git repository, report that clearly rather than
pretending the branch workflow was performed.

## Session notes

- At the end of each session, offer to create or update a short retrospective
  under `docs/sessions/`.
- Name it `YYYY-MM-DD-NN-topic.md`, where `NN` is a two-digit sequence for that
  date, for example `2026-07-08-01-step-0-offline-sine.md`.
- Do not read all retrospectives by default. Read only the latest when the user
  asks to continue a previous session or when context is unclear.
