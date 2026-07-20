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

## Static artwork and real audio

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

The output is useful evidence that the basic pipeline works, but it is not yet
the known-good Version 0 command. It misses the 30 fps target and the video
stream outlasts the audio.

## Next experiment

Update the direct command so that it:

1. explicitly produces 30 fps;
2. ends the video stream with the audio;
3. retains 1080 × 1920, H.264, AAC, and `yuv420p`; and
4. is verified with `ffprobe` and visual playback.

After that baseline is confirmed, add slow zoom to the same direct command.
Waveform and text follow in separate, playable increments.

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
