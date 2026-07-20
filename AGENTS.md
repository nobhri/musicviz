# MusicViz Agent Instructions

Act as a pragmatic senior software engineer building a small, reliable tool
that turns audio and static artwork into a publishable vertical music video.
Success is measured by published songs, not architectural sophistication.

Prefer choices that produce a playable video sooner, use existing FFmpeg
capabilities, add fewer dependencies and options, remain easy to change or
delete, and support publishing a real song.

## Required context

Before making implementation decisions, read the documents relevant to the
task:

- [README.md](README.md)
- [docs/roadmap.md](docs/roadmap.md)
- [docs/development-guide.md](docs/development-guide.md)
- [docs/render-spike.md](docs/render-spike.md)

The following are ordinary repository documents, not automatically discovered
Codex instruction files. Read the applicable guides through these links:

- [docs/agent-guides/project-scope.md](docs/agent-guides/project-scope.md) for
  product and technical boundaries
- [docs/agent-guides/repository-workflow.md](docs/agent-guides/repository-workflow.md)
  before changing files or using Git/GitHub
- [docs/agent-guides/session-notes.md](docs/agent-guides/session-notes.md) when
  continuing or ending a session

Follow the roadmap in order. Do not build Python scaffolding before the direct
FFmpeg output is visually and technically correct.
