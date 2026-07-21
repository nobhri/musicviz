# MusicViz

MusicViz is a small tool for turning a song and static artwork into a
social-media-ready vertical video. The goal is to reduce the work required to
publish original music, not to build a general-purpose video editor.

## Version 0 target

Given an audio file, artwork, a title, and an artist name, MusicViz will
generate `output.mp4` with:

- 1080 × 1920 video at 30 fps
- H.264 video and AAC audio
- static artwork with a slow zoom
- a white semi-transparent waveform near the bottom
- title and artist text

FFmpeg performs all media processing. Python will eventually provide a thin
layer for validation, configuration, command construction, and execution.

## Project status

The known-good FFmpeg pipeline now reads its five project-specific values from
a small YAML file. It resolves paths relative to that file, validates the local
tools and inputs, obtains the audio duration, and renders the verified slow
zoom, waveform, title, and artist treatment. Phase 5 is complete. The project
is ready to add its single Version 0 CLI operation in Phase 6.

See:

- [FFmpeg render spike](docs/render-spike.md) for commands, observed output,
  and the next experiment
- [Test fixtures](docs/test-fixtures.md) for generating the development artwork
  and audio inputs
- [Render history](docs/render-history.md) for completed direct FFmpeg
  experiments
- [Version 0 roadmap](docs/roadmap.md) for development order, scope, and the
  definition of done
- [Development guide](docs/development-guide.md) for implementation, FFmpeg,
  configuration, and testing rules

## Intended usage

Install the locked dependencies and render a project with:

```bash
uv sync
uv run python scripts/make_video.py project.yaml
```

The checked-in `project.yaml` reads the development inputs under `input/` and
writes `output/phase-5-project-config.mp4`. See
[Test fixtures](docs/test-fixtures.md) for creating those ignored local inputs.

The later Version 0 CLI is intended to support:

```bash
musicviz render project.yaml
```

With a small project file:

```yaml
version: 1

audio: audio.wav
artwork: artwork.png

title: "My New Song"
artist: "Nobuaki"

output: output/video.mp4
```

## Technical direction

- Python dependencies and development tools are managed with uv.
- Python orchestrates FFmpeg through `subprocess.run` with argument lists.
- FFmpeg handles rendering, audio processing, and waveform generation.
- The current text pipeline requires a `drawtext`-capable FFmpeg build. On the
  development Mac, use Homebrew `ffmpeg-full` explicitly.
- Paths use `pathlib.Path` and errors remain explicit.
- Fixed visual settings are preferred until real publishing work demonstrates
  a need for configuration.
- Functions are preferred over framework-style abstractions in Version 0.

The intended flow is:

```text
CLI
  ↓
Config Loader
  ↓
Validation
  ↓
FFmpeg Filtergraph Builder
  ↓
FFmpeg Runner
  ↓
output.mp4
```

Repository structure will be introduced only as each phase needs it. The
working render pipeline takes priority over scaffolding.
