# FFmpeg Render History

This document preserves experiments that led to the current direct pipeline.
See [the current render spike](render-spike.md) for the command being extended.

## Synthetic smoke test

The first generated smoke test combined a black vertical video with a sine wave:

```bash
ffmpeg \
  -f lavfi \
  -i color=c=black:s=1080x1920:d=3:r=30 \
  -f lavfi \
  -i sine=frequency=440:duration=3 \
  -c:v libx264 \
  -c:a aac \
  -pix_fmt yuv420p \
  -shortest \
  output/test.mp4
```

It verified H.264 video, AAC audio, 1080 × 1920, 30 fps, and `yuv420p` output.

## Initial artwork and MP3 render

The first render with artwork and real audio produced playable output, but it
ran at 25 fps and its 78.72-second video outlasted the 76.50-second audio:

```bash
ffmpeg \
  -loop 1 \
  -i input/artwork.png \
  -i input/audio.mp3 \
  -c:v libx264 \
  -tune stillimage \
  -c:a aac \
  -b:a 192k \
  -pix_fmt yuv420p \
  -shortest \
  -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" \
  output/output.mp4
```

## Verified Phase 0 baseline

The Phase 0 command set the input and filter frame rates explicitly and used
the known fixture duration:

```bash
ffmpeg \
  -loop 1 \
  -framerate 30 \
  -i input/artwork.png \
  -i input/audio.wav \
  -map 0:v:0 \
  -map 1:a:0 \
  -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30" \
  -c:v libx264 \
  -preset medium \
  -tune stillimage \
  -pix_fmt yuv420p \
  -c:a aac \
  -b:a 192k \
  -t 5 \
  output/phase-0-baseline.mp4
```

It verified H.264 and AAC output at 1080 × 1920, 30 fps, `yuv420p`, and matching
five-second audio, video, and container durations. The complete output also
played correctly in `ffplay`.

Using only `-shortest` had allowed buffered video frames to outlast the audio.
The hard-coded `-t 5` belongs only to the fixture; the later Python wrapper must
obtain the real input duration.
