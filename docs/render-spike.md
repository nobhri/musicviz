# Current FFmpeg Render Spike

This document records the current direct FFmpeg pipeline. Historical
experiments and fixture creation are kept separately:

- [Render history](render-history.md)
- [Test fixtures](test-fixtures.md)

## Environment

The current development machine has FFmpeg 8.1.2 with `libx264`, AAC encoding,
`ffprobe`, and `ffplay` support.

## Verified Phase 1 slow zoom

The current command scales and crops the artwork, then derives a centered zoom
directly from the output-frame number. It increases from 1.0 to 2.0 over the
five-second, 150-frame fixture:

```bash
ffmpeg \
  -loop 1 \
  -framerate 30 \
  -i input/artwork.png \
  -i input/audio.wav \
  -map 0:v:0 \
  -map 1:a:0 \
  -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,zoompan=z='1+on/149':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,format=yuv420p" \
  -c:v libx264 \
  -preset medium \
  -pix_fmt yuv420p \
  -c:a aac \
  -b:a 192k \
  -t 5 \
  output/phase-1-slow-zoom.mp4
```

Verified result:

| Property | Result |
| --- | --- |
| Video codec | H.264 |
| Audio codec | AAC stereo, 44.1 kHz |
| Dimensions | 1080 × 1920 |
| Pixel format | `yuv420p` |
| Frame rate | 30 fps |
| Video duration | 5.00 seconds (150 frames) |
| Audio duration | 5.00 seconds |
| Container duration | 5.00 seconds |

The complete output was played in both QuickTime Player and `ffplay`. The zoom
was smooth and clearly visible, the image remained centered without exposing an
empty edge, and playback ended cleanly at 5.0 seconds.

The denominator `149` belongs to this fixture. The later Python wrapper must
calculate the last output-frame index from the input duration and fixed 30 fps.

## Known limitation

An expression based on accumulated `zoom` state did not produce visible
continuous motion with `d=1`, even though extracted endpoint frames differed.
Use the output-frame variable `on` so that each frame's zoom is explicit.

## Next experiment

Add a white semi-transparent waveform near the bottom using FFmpeg filters.
Preserve the measured Phase 1 properties and keep the waveform readable without
obscuring the artwork excessively.

## Verification

Use `ffprobe` after every meaningful render:

```bash
ffprobe \
  -v error \
  -count_frames \
  -show_entries \
  stream=index,codec_name,codec_type,width,height,r_frame_rate,pix_fmt,duration,nb_read_frames:format=duration \
  -of default=noprint_wrappers=1 \
  output/phase-1-slow-zoom.mp4
```

Also play the complete output. Metadata checks do not detect cropping, motion,
waveform placement, or text readability.
