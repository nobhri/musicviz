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

Also read the applicable split instructions:

- [.agents/project-scope.md](.agents/project-scope.md) for product and technical
  boundaries
- [.agents/repository-workflow.md](.agents/repository-workflow.md) before
  changing files or using Git/GitHub
- [.agents/session-notes.md](.agents/session-notes.md) when continuing or ending
  a session

Follow the roadmap in order. Do not build Python scaffolding before the direct
FFmpeg output is visually and technically correct.
