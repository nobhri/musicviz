# FFmpeg Render Spike

This document records the direct FFmpeg experiments that establish the media
pipeline before a Python wrapper is introduced.

## Environment

The current development machine has:

- FFmpeg 8.1.2
- `libx264` support
- AAC encoding support
- `ffprobe`

## Synthetic smoke test

The spike keeps source media under `input/` and all generated media under
`output/`. Create those directories before running these commands.

This command generates a three-second vertical test video:

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

Verified result:

- H.264 video
- AAC mono audio at 44.1 kHz
- 1080 × 1920
- 30 fps
- 3 seconds
- `yuv420p`

## Initial static artwork and real audio

This command generates a playable video from the spike artwork and MP3:

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

Observed result from `ffprobe`:

| Property | Result |
| --- | --- |
| Video codec | H.264 |
| Audio codec | AAC stereo, 44.1 kHz |
| Dimensions | 1080 × 1920 |
| Pixel format | `yuv420p` |
| Frame rate | 25 fps |
| Audio duration | 76.50 seconds |
| Video duration | 78.72 seconds |

This output was useful evidence that the basic pipeline worked, but it missed
the 30 fps target and its video stream outlasted the audio.

## Verified Phase 0 baseline

The current artwork fixture is a deterministic 1600 × 1600 RGB test pattern.
Its square aspect ratio represents common album artwork, while its color bars,
diagonal lines, and fine pattern make crop, scale, zoom, and color problems
easy to see:

```bash
ffmpeg \
  -f lavfi \
  -i "testsrc2=size=1600x1600:rate=1" \
  -frames:v 1 \
  -update 1 \
  -c:v png \
  -pix_fmt rgb24 \
  input/artwork.png
```

The current test input is a five-second, 44.1 kHz, stereo PCM WAV. It is short
enough for quick render checks and avoids lossy-codec delay while the direct
pipeline is being established:

```bash
ffmpeg \
  -f lavfi \
  -i "sine=frequency=440:sample_rate=44100:duration=5" \
  -ac 2 \
  -c:a pcm_s16le \
  input/audio.wav
```

The source WAV reports a duration of 5.000000 seconds:

```bash
ffprobe \
  -v error \
  -show_entries format=duration \
  -of default=noprint_wrappers=1:nokey=1 \
  input/audio.wav
```

Using that duration explicitly avoids `-shortest` allowing already-buffered
video frames to extend beyond the audio. This is the verified direct command
for the current real-song input:

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

Verified result from `ffprobe`:

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

The complete output was played with `ffplay`. The artwork crop and audio played
correctly, and playback ended cleanly at 5.0 seconds.

The `-t 5` value belongs to this input. The later Python wrapper must obtain
the input duration rather than hard-code it. A trial using only `-shortest`
produced 78.27 seconds of video because libx264 had accepted buffered frames;
using `zerolatency` avoided the overrun but stopped video 0.10 seconds early.

WAV is the preferred development fixture because it keeps timing checks
predictable. MP3 remains a required real-song input format, but a duplicate MP3
fixture is unnecessary until input-format validation or automated integration
tests are introduced.

## Next experiment

Add a restrained slow zoom to the verified direct command while preserving all
of the measured Phase 0 properties. Waveform and text follow in separate,
playable increments.

## Verification template

Use `ffprobe` after every meaningful render:

```bash
ffprobe \
  -v error \
  -show_entries \
  stream=index,codec_name,codec_type,width,height,r_frame_rate,pix_fmt,duration:format=duration \
  -of default=noprint_wrappers=1 \
  output/output.mp4
```

Also play the complete output. Metadata checks do not detect cropping,
waveform placement, text readability, or undesirable zoom behavior.
