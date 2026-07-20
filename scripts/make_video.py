#!/usr/bin/env python3
"""Render the fixed MusicViz Version 0 pipeline from development inputs."""

from __future__ import annotations

import math
import os
import subprocess
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
FFMPEG = Path("/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg")
FFPROBE = FFMPEG.with_name("ffprobe")
ARTWORK = Path("input/artwork.png")
AUDIO = Path("input/audio.wav")
TITLE = Path("input/title.txt")
ARTIST = Path("input/artist.txt")
TITLE_FONT = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")
ARTIST_FONT = Path("/System/Library/Fonts/Supplemental/Arial.ttf")
OUTPUT = Path("output/phase-4-python-wrapper.mp4")
FRAME_RATE = 30


class RenderError(RuntimeError):
    """An actionable error raised before or during rendering."""


def validate_executable(path: Path, name: str) -> None:
    if not path.is_file() or not os.access(path, os.X_OK):
        raise RenderError(f"{name} executable not found or not executable: {path}")


def validate_file(path: Path, description: str) -> None:
    resolved = ROOT / path if not path.is_absolute() else path
    if not resolved.is_file():
        raise RenderError(f"{description} not found: {resolved}")


def validate_environment() -> None:
    validate_executable(FFMPEG, "FFmpeg")
    validate_executable(FFPROBE, "ffprobe")
    for path, description in (
        (ARTWORK, "Artwork"),
        (AUDIO, "Audio"),
        (TITLE, "Title text"),
        (ARTIST, "Artist text"),
        (TITLE_FONT, "Title font"),
        (ARTIST_FONT, "Artist font"),
    ):
        validate_file(path, description)

    result = subprocess.run(
        [str(FFMPEG), "-hide_banner", "-filters"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RenderError(f"Could not inspect FFmpeg filters:\n{result.stderr.strip()}")
    if "drawtext" not in result.stdout:
        raise RenderError(f"FFmpeg does not provide the required drawtext filter: {FFMPEG}")


def probe_audio_duration() -> Decimal:
    result = subprocess.run(
        [
            str(FFPROBE),
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(AUDIO),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RenderError(f"Could not read audio duration:\n{result.stderr.strip()}")
    try:
        duration = Decimal(result.stdout.strip())
    except InvalidOperation as error:
        raise RenderError(f"ffprobe returned an invalid audio duration: {result.stdout!r}") from error
    if not duration.is_finite() or duration <= 0:
        raise RenderError(f"Audio duration must be positive and finite: {duration}")
    return duration


def build_filtergraph(duration: Decimal) -> str:
    frame_count = math.ceil(duration * FRAME_RATE)
    last_frame_index = max(frame_count - 1, 1)
    return (
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,"
        f"zoompan=z='1+on/{last_frame_index}':"
        "x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        "d=1:s=1080x1920:fps=30[background];"
        "[1:a]asplit=2[audio][waveform_audio];"
        "[waveform_audio]showwaves=s=960x240:mode=cline:colors=white:"
        "r=30:scale=sqrt,format=gray[waveform_mask];"
        "color=c=white:s=960x240:r=30,format=rgba[waveform_color];"
        "[waveform_color][waveform_mask]alphamerge,"
        "colorchannelmixer=aa=0.65[waveform];"
        "[background][waveform]overlay=x=(W-w)/2:y=H-h-120:"
        "shortest=1:format=auto:alpha=straight[composited];"
        "[composited]"
        f"drawtext=fontfile='{TITLE_FONT}':textfile={TITLE}:"
        "fontcolor=white:fontsize=72:borderw=4:bordercolor=black@0.85:"
        "x=(w-text_w)/2:y=540,"
        f"drawtext=fontfile='{ARTIST_FONT}':textfile={ARTIST}:"
        "fontcolor=white:fontsize=48:borderw=3:bordercolor=black@0.85:"
        "x=(w-text_w)/2:y=640,format=yuv420p[video]"
    )


def format_duration(duration: Decimal) -> str:
    return format(duration.normalize(), "f")


def build_ffmpeg_command(duration: Decimal) -> list[str]:
    return [
        str(FFMPEG),
        "-hide_banner",
        "-nostdin",
        "-y",
        "-loop",
        "1",
        "-framerate",
        str(FRAME_RATE),
        "-i",
        str(ARTWORK),
        "-i",
        str(AUDIO),
        "-filter_complex",
        build_filtergraph(duration),
        "-map",
        "[video]",
        "-map",
        "[audio]",
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-t",
        format_duration(duration),
        str(OUTPUT),
    ]


def run_ffmpeg(command: list[str]) -> None:
    result = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RenderError(
            f"FFmpeg render failed with exit code {result.returncode}:\n{result.stderr.strip()}"
        )


def main() -> int:
    try:
        validate_environment()
        duration = probe_audio_duration()
        (ROOT / OUTPUT).parent.mkdir(parents=True, exist_ok=True)
        run_ffmpeg(build_ffmpeg_command(duration))
    except RenderError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    print(f"Rendered {ROOT / OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
