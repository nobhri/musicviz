# Version 0 Roadmap

Version 0 is organized around playable outputs. Each phase builds on a direct,
verified FFmpeg pipeline; automation comes only after the visual result works.

## Scope

Version 0 includes:

- audio and static artwork inputs
- 1080 × 1920 output at 30 fps
- H.264 video and AAC audio
- slow artwork zoom
- white semi-transparent waveform near the bottom
- title and artist text
- a small project configuration
- a single render command

Version 0 excludes GUI and web applications, custom FFT or frame rendering,
beat detection, lyric synchronization, particles, 3D rendering, social-media
APIs, plugin systems, databases, render queues, and cloud rendering.

## Phases

### Phase 0 — FFmpeg baseline (complete)

Generate and verify a direct FFmpeg render.

Completion criteria:

- video plays correctly
- output is 1080 × 1920 at 30 fps
- video ends with the audio
- output contains H.264 video and AAC audio

### Phase 1 — Slow zoom (complete)

Add image scaling, cropping, and a clearly visible slow zoom while preserving
the verified output properties.

### Phase 2 — Waveform (current)

Add a white semi-transparent waveform near the bottom using FFmpeg filters.

### Phase 3 — Text

Add readable title and artist text with an explicit font. Prefer
`drawtext=textfile=` when project-provided text is introduced.

### Phase 4 — Minimal Python wrapper

Preserve the known-good FFmpeg behavior in a small Python script using
`pathlib.Path`, `subprocess.run`, and a `list[str]` command. Validate FFmpeg and
input-file availability and preserve useful stderr on failure.

### Phase 5 — Project configuration

Move only audio, artwork, title, artist, and output path into a small YAML file.
Keep visual and encoding settings fixed until real projects require otherwise.

### Phase 6 — CLI

Support one primary operation:

```bash
musicviz render project.yaml
```

### Phase 7 — Real-song validation

Render three real song projects without code changes. Fix recurring publishing
problems, not hypothetical extension points.

## Version 0 definition of done

Version 0 is complete when:

- three real song projects render without code changes;
- generated videos do not routinely need correction in an editor;
- creating a video requires only a project file and one command; and
- at least one generated video has been published.

## Working rules

- End every phase with a playable video.
- Prefer FFmpeg capabilities over Python media processing.
- Use short generated fixtures for integration checks.
- Add tests for configuration, path resolution, command generation, a short
  render, and `ffprobe` verification as those features appear.
- Avoid speculative directories, abstractions, and configuration options.
- Add future visual features only after Version 0 supports real publishing.
