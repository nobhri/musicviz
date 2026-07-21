#!/usr/bin/env python3
"""Render the fixed MusicViz Version 0 pipeline from a project file."""

from __future__ import annotations

import math
import os
import subprocess
import sys
import tempfile
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parent.parent
FFMPEG = Path("/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg")
FFPROBE = FFMPEG.with_name("ffprobe")
TITLE_FONT = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")
ARTIST_FONT = Path("/System/Library/Fonts/Supplemental/Arial.ttf")
FRAME_RATE = 30
CONFIG_KEYS = {"version", "audio", "artwork", "title", "artist", "output"}


class RenderError(RuntimeError):
    """An actionable error raised before or during rendering."""


@dataclass(frozen=True)
class ProjectConfig:
    """Project-specific values loaded from a YAML file."""

    source: Path
    audio: Path
    artwork: Path
    title: str
    artist: str
    output: Path


def _required_string(data: Mapping[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise RenderError(f"Project field '{key}' must be a non-empty string")
    return value


def load_config(path: Path) -> ProjectConfig:
    """Load and validate a Version 1 project file."""
    source = path.expanduser().resolve()
    if not source.is_file():
        raise RenderError(f"Project file not found: {source}")

    try:
        loaded = yaml.safe_load(source.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        raise RenderError(f"Could not read project file {source}: {error}") from error

    if not isinstance(loaded, Mapping):
        raise RenderError(f"Project file must contain a YAML mapping: {source}")

    unknown_keys = set(loaded) - CONFIG_KEYS
    if unknown_keys:
        names = ", ".join(sorted(str(key) for key in unknown_keys))
        raise RenderError(f"Unknown project field(s): {names}")
    if loaded.get("version") != 1 or isinstance(loaded.get("version"), bool):
        raise RenderError("Project field 'version' must be 1")

    audio = _required_string(loaded, "audio")
    artwork = _required_string(loaded, "artwork")
    title = _required_string(loaded, "title")
    artist = _required_string(loaded, "artist")
    output = _required_string(loaded, "output")
    project_dir = source.parent
    audio_path = (project_dir / audio).resolve()
    artwork_path = (project_dir / artwork).resolve()
    output_path = (project_dir / output).resolve()
    if output_path in {audio_path, artwork_path}:
        raise RenderError("Project output must not overwrite an input file")

    return ProjectConfig(
        source=source,
        audio=audio_path,
        artwork=artwork_path,
        title=title,
        artist=artist,
        output=output_path,
    )


def validate_executable(path: Path, name: str) -> None:
    if not path.is_file() or not os.access(path, os.X_OK):
        raise RenderError(f"{name} executable not found or not executable: {path}")


def validate_file(path: Path, description: str) -> None:
    if not path.is_file():
        raise RenderError(f"{description} not found: {path}")


def validate_environment(config: ProjectConfig) -> None:
    validate_executable(FFMPEG, "FFmpeg")
    validate_executable(FFPROBE, "ffprobe")
    for path, description in (
        (config.artwork, "Artwork"),
        (config.audio, "Audio"),
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


def probe_audio_duration(audio: Path) -> Decimal:
    result = subprocess.run(
        [
            str(FFPROBE),
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(audio),
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
        raise RenderError(
            f"ffprobe returned an invalid audio duration: {result.stdout!r}"
        ) from error
    if not duration.is_finite() or duration <= 0:
        raise RenderError(f"Audio duration must be positive and finite: {duration}")
    return duration


def _filter_path(path: Path) -> str:
    escaped = str(path).replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")
    return f"'{escaped}'"


def build_filtergraph(duration: Decimal, title_file: Path, artist_file: Path) -> str:
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
        f"drawtext=fontfile={_filter_path(TITLE_FONT)}:textfile={_filter_path(title_file)}:"
        "fontcolor=white:fontsize=72:borderw=4:bordercolor=black@0.85:"
        "x=(w-text_w)/2:y=540,"
        f"drawtext=fontfile={_filter_path(ARTIST_FONT)}:textfile={_filter_path(artist_file)}:"
        "fontcolor=white:fontsize=48:borderw=3:bordercolor=black@0.85:"
        "x=(w-text_w)/2:y=640,format=yuv420p[video]"
    )


def format_duration(duration: Decimal) -> str:
    return format(duration.normalize(), "f")


def build_ffmpeg_command(
    config: ProjectConfig,
    duration: Decimal,
    title_file: Path,
    artist_file: Path,
) -> list[str]:
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
        str(config.artwork),
        "-i",
        str(config.audio),
        "-filter_complex",
        build_filtergraph(duration, title_file, artist_file),
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
        str(config.output),
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


def render(config: ProjectConfig) -> None:
    validate_environment(config)
    duration = probe_audio_duration(config.audio)
    config.output.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="musicviz-") as temp_dir:
        text_dir = Path(temp_dir)
        title_file = text_dir / "title.txt"
        artist_file = text_dir / "artist.txt"
        title_file.write_text(config.title, encoding="utf-8")
        artist_file.write_text(config.artist, encoding="utf-8")
        run_ffmpeg(build_ffmpeg_command(config, duration, title_file, artist_file))


def main(argv: Sequence[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    if len(arguments) != 1:
        print("usage: python scripts/make_video.py PROJECT.yaml", file=sys.stderr)
        return 2

    try:
        config = load_config(Path(arguments[0]))
        render(config)
    except RenderError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    print(f"Rendered {config.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
