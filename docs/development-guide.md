# Development Guide

This guide contains implementation rules for MusicViz Version 0. Product scope,
phase order, and completion criteria live in [the roadmap](roadmap.md).

## Technical direction

Use Python to orchestrate the FFmpeg CLI. Prefer:

- `subprocess.run` with argument lists, never `shell=True`;
- `pathlib.Path` for paths;
- standard-library functionality where practical;
- small typed functions and dataclasses where they clarify data; and
- explicit, actionable errors.

Python must not implement video rendering, FFT processing, waveform drawing, or
frame-by-frame image generation.

## Intended flow

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

Initially prefer functions over classes:

```python
def load_config(path: Path) -> ProjectConfig:
    ...

def validate_inputs(config: ProjectConfig) -> None:
    ...

def build_filtergraph(config: ProjectConfig) -> str:
    ...

def build_ffmpeg_command(config: ProjectConfig) -> list[str]:
    ...

def run_ffmpeg(command: list[str]) -> None:
    ...
```

Do not introduce layer protocols, factories, registries, renderer hierarchies,
or plugin interfaces until multiple real implementations require them.

## FFmpeg rules

- Pass all arguments as `list[str]` and make paths explicit.
- Require an FFmpeg build with the filters used by the known-good pipeline,
  including `drawtext`. On the development Mac, this is the keg-only Homebrew
  `ffmpeg-full` build at `/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg`.
- Validate required filter availability and report a clear error rather than
  failing later with an opaque filtergraph error.
- Prefer `-filter_complex_script` when escaping the filtergraph becomes hard.
- Prefer `drawtext=textfile=` over embedding arbitrary project text.
- Preserve FFmpeg stderr and check the process return code.
- Fail clearly when FFmpeg or an input file is missing.
- Show the generated command and filtergraph when debugging is requested.

## Configuration

The initial Version 0 configuration should contain only project-specific data:

```yaml
version: 1

audio: audio.wav
artwork: artwork.png

title: "My New Song"
artist: "Nobuaki"

output: output/video.mp4
```

Keep width, height, frame rate, codecs, waveform position and appearance, zoom
speed, font style, and theme fixed in code until real use demonstrates a need
to configure them.

## Code quality and errors

Write code that is readable, small, directly testable, and easy to remove or
change. Avoid abstractions without a demonstrated need and avoid broad
exception handling such as `except Exception`.

External-command failures should identify what failed and preserve useful
diagnostic output.

## Python environment and development tools

Use uv to manage the Python version, runtime dependencies, development tools,
and lockfile. Phase 4 deliberately used only the standard library; uv was added
in Phase 5 when YAML parsing introduced the first runtime dependency. Keep this
usage focused on reproducible environments. It does not justify packaging the
application before the Phase 6 CLI needs it.

Use PyYAML with `safe_load` rather than maintaining a project-specific YAML
parser. The project schema remains small and is validated explicitly after
parsing.

Use pytest for both unit and integration tests. It replaced the standard
library `unittest` runner when configuration work introduced repeated invalid
inputs, temporary project directories, and generated media fixtures. Prefer
pytest's built-in fixtures and parametrization; do not add pytest plugins
without a concrete need.

Use Ruff as the single formatter and linter. Its purpose is fast, consistent
baseline checks with one tool, not adoption of a broad or highly customized
rule set. Keep its configuration small. Do not add pre-commit hooks until
missed local checks become a demonstrated workflow problem; CI should enforce
required checks when CI is introduced.

## Testing priorities

Add tests as the corresponding features appear, in this order:

1. configuration loading;
2. path resolution;
3. FFmpeg command generation;
4. a short integration render; and
5. `ffprobe` verification of the output.

Generate small integration-test artwork and audio inside pytest so a checkout
does not depend on ignored development inputs. Integration fixtures should
last only a few seconds. Do not add an extensive visual golden-master suite in
Version 0. Visual output must still be played and inspected at meaningful
render milestones.

Run the current automated checks through the locked uv environment:

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

## Visual media verification

- Do not infer continuous motion from extracted first and final frames. Those
  frames prove only that two endpoints differ.
- Play the complete output in at least one user-relevant player. When playback
  behavior is disputed, reproduce it in the same player and compare with
  `ffplay` when available.
- For frame-dependent filters, prefer expressions derived directly from an
  explicit frame or time variable. Verify that intermediate frames change, not
  only the endpoints.
- Treat encoder statistics and frame hashes as supporting evidence, not a
  substitute for full playback.
- Do not mark a visual phase complete until the user can observe the intended
  effect in their normal playback path when user verification is available.
