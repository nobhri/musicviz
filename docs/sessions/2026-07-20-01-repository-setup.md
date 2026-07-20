# Repository Setup Retrospective

Date: 2026-07-20

## What we accomplished

- Confirmed that the project is still in Phase 0, validating the direct FFmpeg
  pipeline before adding Python.
- Reduced `README.md` to a project entry point.
- Moved the original FFmpeg memo into `docs/render-spike.md` and recorded the
  verified output properties and current limitations.
- Separated the Version 0 roadmap and development rules into focused documents.
- Reduced `AGENTS.md` to the instructions agents need during repository work.
- Standardized spike paths on `input/` for local source media and `output/` for
  generated media.
- Added `.gitignore` rules for those local media directories and common macOS
  and Python artifacts.
- Initialized the Git repository, selected the MIT License, created a public
  GitHub repository, and pushed the initial commit.
- Configured protection for `main` so future changes go through pull requests.

## Decisions

- Keep real input media and generated videos out of Git.
- Treat `input/` as a temporary spike convention, not a permanent project-file
  architecture.
- Do not add more documentation or scaffolding until implementation creates a
  demonstrated need.
- Use feature branches after the initial repository bootstrap, even for a
  single-maintainer project.

## What we learned

- `gh api licenses/mit --jq .body` retrieves the MIT License template body;
  shell tools can replace its year and name placeholders before saving it.
- `gh repo create --source=. --remote=origin --push` can create a GitHub
  repository, attach it as the local remote, and push in one operation.
- Branch protection can be configured with `gh api` even though `gh` has no
  dedicated high-level branch-protection command.
- A shell heredoc continues with a `heredoc>` prompt until its delimiter is
  entered exactly at the start of a line. Piping JSON to `gh api --input -` is
  a convenient alternative for one-off commands.

## Friction and limitations

- Git checks and branch workflow were unavailable until the repository was
  initialized.
- The current real-song render is 1080 × 1920 H.264/AAC, but it is 25 fps and
  its 78.72-second video stream outlasts the 76.50-second audio stream.

## Next action

Continue the Phase 0 FFmpeg spike on a dedicated feature branch. Produce a
1080 × 1920, 30 fps, H.264/AAC render whose video ends with the audio, then
verify it with `ffprobe` and playback before adding slow zoom.
