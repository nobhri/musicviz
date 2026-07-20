# Phase 2 Waveform Retrospective

Date: 2026-07-20

## What we accomplished

- Added a synchronized white semi-transparent waveform to the direct FFmpeg
  pipeline while preserving the verified Phase 1 zoom.
- Preserved H.264 and AAC output at 1080 × 1920, 30 fps, `yuv420p`, 150 video
  frames, and matching five-second stream and container durations.
- Added a generated rhythmic harmonics fixture with clear audible and silent
  intervals to make waveform synchronization observable.
- Verified the waveform with sampled intermediate frames, full `ffplay`
  playback, `ffprobe`, and user playback feedback.
- Advanced the roadmap to Phase 3 text.

## Decisions

- Use a 960 × 240 centered waveform positioned 120 pixels above the bottom
  edge for the current direct pipeline.
- Use `mode=cline`, square-root amplitude scaling, white color, and 65% alpha
  as the first accepted treatment.
- Build the visible waveform by using `showwaves` as a grayscale alpha mask for
  a white source. This avoids both a dark waveform and a visible rectangular
  waveform background on the current FFmpeg build.
- Keep visual tuning as a future publishing task instead of adding waveform
  configuration during Phase 2.

## What went wrong

- Passing `white@0.65` directly through `showwaves` and `overlay` produced a
  dark-looking waveform rather than the intended translucent white.
- Applying alpha after converting the raw `showwaves` output still retained
  incorrect color or tinted the full waveform rectangle, depending on the
  overlay alpha mode.
- The continuous sine fixture made it difficult to judge whether waveform
  motion was truly synchronized with the audio.

## What we learned

- Alpha behavior must be verified against both bright and dark image regions;
  a nominal color setting does not guarantee the expected composite.
- A grayscale waveform mask combined with an explicit white RGBA source makes
  color and transparency behavior easier to reason about.
- Diagnostic audio should contain intentional audible and silent intervals.
  The rhythmic harmonics fixture made synchronization much clearer than a
  sustained sine wave.
- Functional waveform synchronization and final visual styling are separate
  decisions. Size, placement, opacity, color, and contrast should be revisited
  with representative real artwork.

## Verification

- Rendered `output/phase-2-waveform.mp4` from the continuous sine fixture.
- Rendered `output/phase-2-rhythmic-harmonics.mp4` from ten 220 ms sound events
  separated by 280 ms silence.
- Confirmed H.264, AAC, 1080 × 1920, 30 fps, `yuv420p`, 150 video frames, and
  matching 5.000-second durations with `ffprobe`.
- Compared frames from alternating audible and silent intervals and confirmed
  that the waveform appeared and disappeared with the audio.
- Played both complete outputs in `ffplay`; the user accepted the rhythmic
  waveform result in their playback path.
- Ran `git diff --check` after the documentation changes.

## Friction and limitations

- The accepted waveform values have been tested only with generated artwork
  and audio. Real artwork may require a different fixed Version 0 treatment.
- The current waveform construction is verbose, but it remains a direct
  FFmpeg pipeline and should not be abstracted before the visual stages are
  complete.
- Generated WAV and MP4 fixtures remain local and are not committed; their
  deterministic generation commands are documented instead.

## Next action

Add title and artist text with an explicit font to the verified direct FFmpeg
pipeline. Preserve the zoom, waveform, stream properties, and playable output.
