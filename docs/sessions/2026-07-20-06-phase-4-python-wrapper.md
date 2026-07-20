# Phase 4 Minimal Python Wrapper Retrospective

## Outcome

- Added `scripts/make_video.py` as a thin wrapper around the verified Phase 3
  FFmpeg pipeline.
- Validated FFmpeg, ffprobe, `drawtext`, input files, and fixed font files
  before rendering.
- Replaced the fixture-specific timing constants with an audio-duration probe
  and a calculated last output frame index at 30 fps.
- Kept project YAML and the final CLI out of Phase 4.

## Decisions

- Continue to invoke the keg-only Homebrew `ffmpeg-full` executable explicitly.
- Keep the development input and output paths fixed until Phase 5 introduces
  project configuration.
- Use only the Python standard library and small functions; no packaging or
  application framework was added.
- Capture FFmpeg stderr and include it in the actionable error shown on
  rendering failure.

## Verification

- Ran `python3 -m unittest discover -s tests -v`; all four tests passed.
- Ran `python3 scripts/make_video.py` successfully.
- Confirmed H.264 video, AAC audio, 1080 × 1920, `yuv420p`, 30 fps, 150 video
  frames, and matching five-second stream and container durations with
  ffprobe.
- Played the complete output in ffplay.
- Inspected frames at 0.5, 2.5, and 4.5 seconds. The image display tool showed
  inconsistent previews for byte-identical midpoint PNG files; SHA-256 and
  byte comparison proved that this was not a render difference, so no
  speculative FFmpeg thread option was retained.
- Ran `git diff --check`.

## Next step

Implement Phase 5 project configuration containing only audio, artwork, title,
artist, and output path. Resolve relative paths from the project file and keep
all visual and encoding settings fixed.
