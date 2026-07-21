import json
import math
import struct
import subprocess
import wave
from pathlib import Path

import pytest

from scripts.make_video import (
    ARTIST_FONT,
    FFMPEG,
    FFPROBE,
    TITLE_FONT,
    ProjectConfig,
    load_config,
    render,
)


REQUIRED_RENDER_FILES = [
    FFMPEG,
    FFPROBE,
    TITLE_FONT,
    ARTIST_FONT,
]


@pytest.mark.skipif(
    not all(path.is_file() for path in REQUIRED_RENDER_FILES),
    reason="the required FFmpeg build or fonts are unavailable",
)
def test_short_render_has_expected_media_properties(generated_project: ProjectConfig) -> None:
    config = generated_project

    render(config)

    result = subprocess.run(
        [
            str(FFPROBE),
            "-v",
            "error",
            "-count_frames",
            "-show_streams",
            "-show_format",
            "-of",
            "json",
            str(config.output),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    metadata = json.loads(result.stdout)
    streams = {stream["codec_type"]: stream for stream in metadata["streams"]}

    assert streams["video"]["codec_name"] == "h264"
    assert streams["video"]["width"] == 1080
    assert streams["video"]["height"] == 1920
    assert streams["video"]["pix_fmt"] == "yuv420p"
    assert streams["video"]["r_frame_rate"] == "30/1"
    assert streams["audio"]["codec_name"] == "aac"
    assert float(metadata["format"]["duration"]) == pytest.approx(0.5, abs=0.01)


@pytest.fixture
def generated_project(tmp_path: Path) -> ProjectConfig:
    artwork = tmp_path / "artwork.ppm"
    width = height = 64
    artwork.write_bytes(
        f"P6\n{width} {height}\n255\n".encode() + bytes([35, 70, 120]) * width * height
    )

    audio = tmp_path / "audio.wav"
    sample_rate = 8_000
    sample_count = sample_rate // 2
    with wave.open(str(audio), "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        samples = (
            struct.pack("<h", round(8_000 * math.sin(2 * math.pi * 440 * index / sample_rate)))
            for index in range(sample_count)
        )
        wav_file.writeframes(b"".join(samples))

    project_file = tmp_path / "project.yaml"
    project_file.write_text(
        """\
version: 1
audio: audio.wav
artwork: artwork.ppm
title: Integration Test
artist: MusicViz
output: video.mp4
""",
        encoding="utf-8",
    )
    return load_config(project_file)
