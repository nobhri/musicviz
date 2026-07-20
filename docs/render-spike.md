# Current FFmpeg Render Spike

This document records the current direct FFmpeg pipeline. Historical
experiments and fixture creation are kept separately:

- [Render history](render-history.md)
- [Test fixtures](test-fixtures.md)

## Environment

The current development machine has FFmpeg 8.1.2 with `libx264`, AAC encoding,
`ffprobe`, and `ffplay` support.

## Verified Phase 2 waveform

The current command preserves the centered Phase 1 zoom and adds a 960 × 240
white waveform 120 pixels above the bottom edge. The waveform uses square-root
amplitude scaling so that quieter input remains visible.

`showwaves` produces a white-on-black image rather than a usable transparent
overlay on this FFmpeg build. The command therefore converts that image to a
grayscale alpha mask, applies it to a white source, reduces the resulting alpha
to 65%, and overlays only the waveform pixels:

```bash
ffmpeg \
  -loop 1 \
  -framerate 30 \
  -i input/artwork.png \
  -i input/audio.wav \
  -filter_complex "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,zoompan=z='1+on/149':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30[background];[1:a]asplit=2[audio][waveform_audio];[waveform_audio]showwaves=s=960x240:mode=cline:colors=white:r=30:scale=sqrt,format=gray[waveform_mask];color=c=white:s=960x240:r=30,format=rgba[waveform_color];[waveform_color][waveform_mask]alphamerge,colorchannelmixer=aa=0.65[waveform];[background][waveform]overlay=x=(W-w)/2:y=H-h-120:shortest=1:format=auto:alpha=straight,format=yuv420p[video]" \
  -map "[video]" \
  -map "[audio]" \
  -c:v libx264 \
  -preset medium \
  -pix_fmt yuv420p \
  -c:a aac \
  -b:a 192k \
  -t 5 \
  output/phase-2-waveform.mp4
```

Observed result:

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

The complete output played to completion in `ffplay`. Frames sampled at 0.5,
1.5, 2.5, 3.5, and 4.5 seconds showed a changing waveform, continuous zoom,
no opaque waveform rectangle, and no exposed artwork edge.

The same pipeline was also rendered as
`output/phase-2-rhythmic-harmonics.mp4` using the rhythmic harmonics fixture
documented in [Test fixtures](test-fixtures.md). Full playback and alternating
frames from audible and silent intervals confirmed that the waveform appears
with each 220 ms sound event and disappears during the following 280 ms silence.
This provides clearer synchronization evidence than the continuous sine input.

The user confirmed that the waveform was visible and that the rhythmic fixture
made its synchronization with the audio clear. Phase 2 is complete; visual
tuning remains deliberately separate from the functional milestone.

## Remaining visual tuning

The waveform is functionally synchronized with the audio, but its visual
balance is not final. Revisit these choices with representative real artwork
before treating them as publishing defaults:

- waveform width, height, and distance from the bottom edge;
- opacity relative to detailed, bright, and dark artwork;
- whether white remains the most reliable fixed color;
- contrast handling when the artwork has similar brightness behind the
  waveform; and
- how much of the artwork the waveform may cover without becoming distracting.

Prefer one fixed Version 0 treatment that works across real projects. Do not
add per-project visual configuration until repeated publishing tests show that
a fixed treatment is insufficient.

## Next experiment

Add readable title and artist text with an explicit font while preserving the
verified zoom, waveform, output properties, and five-second duration. Keep the
direct FFmpeg pipeline playable before introducing the Python wrapper.

## Fixture-specific values

The denominator `149` and `-t 5` belong to the five-second fixture. The later
Python wrapper must obtain the input duration and calculate the last output
frame index at the fixed 30 fps.

## Verification

Use `ffprobe` after every meaningful render:

```bash
ffprobe \
  -v error \
  -count_frames \
  -show_entries \
  stream=index,codec_name,codec_type,width,height,r_frame_rate,pix_fmt,duration,nb_read_frames:format=duration \
  -of default=noprint_wrappers=1 \
  output/phase-2-waveform.mp4
```

Also play the complete output. Metadata checks do not detect cropping, motion,
waveform placement, transparency, or text readability.
