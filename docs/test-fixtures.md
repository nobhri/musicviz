# Test Fixtures

The direct FFmpeg experiments use short generated fixtures under `input/`.
Generated renders belong under `output/`. Create both directories when needed:

```bash
mkdir -p input output
```

## Artwork

Generate a deterministic 1600 × 1600 RGB test pattern:

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

The square shape represents common album artwork. Its color bars, diagonals,
and fine pattern make crop, scale, zoom, and color problems visible.

## Audio

Generate a five-second, 44.1 kHz, stereo PCM WAV:

```bash
ffmpeg \
  -f lavfi \
  -i "sine=frequency=440:sample_rate=44100:duration=5" \
  -ac 2 \
  -c:a pcm_s16le \
  input/audio.wav
```

Confirm its duration:

```bash
ffprobe \
  -v error \
  -show_entries format=duration \
  -of default=noprint_wrappers=1:nokey=1 \
  input/audio.wav
```

WAV avoids lossy-codec delay and keeps timing checks predictable. MP3 remains
a required real-song input, but a duplicate MP3 fixture is not yet needed.

Do not commit large or real-song media fixtures without explicit approval.
