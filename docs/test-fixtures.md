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

## Rhythmic harmonics audio

Generate a five-second validation input with ten clearly separated sound
events. Each event lasts 220 ms and is followed by 280 ms of silence. The tone
combines a 110 Hz fundamental with harmonics at 220, 330, and 440 Hz, while a
smooth envelope prevents clicks at the event boundaries:

```bash
ffmpeg \
  -f lavfi \
  -i "aevalsrc=exprs='(0.55*sin(2*PI*110*t)+0.25*sin(2*PI*220*t)+0.12*sin(2*PI*330*t)+0.08*sin(2*PI*440*t))*if(lt(mod(t\,0.5)\,0.22)\,pow(sin(PI*mod(t\,0.5)/0.22)\,2)\,0)':s=44100:d=5" \
  -ac 2 \
  -c:a pcm_s16le \
  input/rhythmic-harmonics.wav
```

Use this fixture to verify that a waveform appears during each audible event,
disappears during silence, and shows more structure than the continuous
single-frequency sine fixture. It is a diagnostic input, not a target musical
sound.

## Text

Create short UTF-8 text files for the Phase 3 title and artist inputs:

```bash
printf '%s\n' 'My New Song' > input/title.txt
printf '%s\n' 'Nobuaki' > input/artist.txt
```

The verified filtergraph reads these files with `drawtext=textfile=` rather
than embedding project-provided strings in the filtergraph. This avoids FFmpeg
expression escaping problems and matches the intended later project inputs.

Do not commit large or real-song media fixtures without explicit approval.
