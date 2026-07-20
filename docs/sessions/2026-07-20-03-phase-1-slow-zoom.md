# Phase 1 Slow Zoom Retrospective

Date: 2026-07-20

## What we accomplished

- Added a centered FFmpeg `zoompan` effect to the verified five-second pipeline.
- Preserved H.264 and AAC output at 1080 × 1920, 30 fps, `yuv420p`, 150 video
  frames, and matching five-second stream and container durations.
- Verified the corrected zoom in both QuickTime Player and `ffplay`.
- Advanced the roadmap to Phase 2 waveform.
- Split current render evidence, historical experiments, and fixture-generation
  commands into focused documents.
- Split the root agent instructions into a short entry point and scoped files
  under `.agents/`.

## Decisions

- Use `zoompan=z='1+on/149'` for the five-second fixture. Deriving zoom from the
  output-frame number makes the intended value explicit for every frame.
- Keep the strong 1.0-to-2.0 zoom for now because it is clearly observable and
  was explicitly accepted during playback validation.
- Keep fixture generation in `docs/test-fixtures.md`, completed experiments in
  `docs/render-history.md`, and only the current pipeline in
  `docs/render-spike.md`.
- Put reusable verification rules in the required development guide rather than
  relying on this retrospective to influence future sessions.

## What went wrong

- The first implementation accumulated `zoom` state while using `d=1`. Extracted
  first and final frames differed, but the complete video showed no visible
  motion in QuickTime Player, Safari, or `ffplay` on the user's machine.
- The agent incorrectly treated endpoint differences, metadata, and its own
  playback attempt as sufficient evidence and declared Phase 1 complete.
- Investigation initially focused on player caching and Apple decoding even
  after the user had reopened the exact file. That delayed checking the filter
  expression itself.

## What we learned

- Endpoint images cannot prove continuous animation. Intermediate behavior and
  complete playback are separate requirements.
- User-observed playback outweighs indirect evidence such as frame hashes,
  nominal frame counts, or a successful encoder exit status.
- Frame-dependent FFmpeg expressions are easier to reason about when based on
  explicit variables such as `on` instead of accumulated filter state.
- A diagnostic effect should be deliberately unmistakable. The 1.0-to-2.0 test
  made it immediately clear whether the pipeline was moving.

## Verification

- Rendered `output/phase-1-slow-zoom.mp4` with `z='1+on/149'`.
- Confirmed H.264, AAC, 1080 × 1920, 30 fps, `yuv420p`, 150 video frames, and
  matching 5.000-second durations with `ffprobe`.
- Confirmed visible continuous zoom in both QuickTime Player and `ffplay` with
  the user.
- Ran `git diff --check` after the documentation changes.

## Friction and limitations

- The denominator `149` and `-t 5` are specific to this fixture. The later
  Python wrapper must derive duration and the final frame index.
- A 2× zoom over five seconds is intentionally strong. Real-song validation may
  show that a duration-aware, slower effect is preferable for publishing.
- Quick Look's `qlmanage -p` crashed because its AVKit host did not support
  `highlightedTimeRanges`; this was unrelated to the video content.

## Next action

Add a white semi-transparent waveform near the bottom of the verified Phase 1
pipeline. Preserve its output properties and validate the complete result in a
user-relevant player before marking Phase 2 complete.
