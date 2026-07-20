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

The direct FFmpeg pipeline now includes a verified slow zoom and synchronized
white semi-transparent waveform using five-second WAV fixtures at 1080 × 1920
and 30 fps, with matching video and audio stream durations. The project is now
in the text phase. Text will be added to the direct command as another playable
increment before the pipeline is wrapped in Python.

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

The first Python wrapper may be run as:

```bash
python scripts/make_video.py
```

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

- Python orchestrates FFmpeg through `subprocess.run` with argument lists.
- FFmpeg handles rendering, audio processing, and waveform generation.
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
