import json
import subprocess
from dataclasses import replace
from pathlib import Path

import pytest

from scripts.make_video import (
    ARTIST_FONT,
    FFMPEG,
    FFPROBE,
    ROOT,
    TITLE_FONT,
    load_config,
    render,
)


REQUIRED_LOCAL_FILES = [
    FFMPEG,
    FFPROBE,
    TITLE_FONT,
    ARTIST_FONT,
    ROOT / "input/audio.wav",
    ROOT / "input/artwork.png",
]


@pytest.mark.skipif(
    not all(path.is_file() for path in REQUIRED_LOCAL_FILES),
    reason="local FFmpeg integration fixtures are unavailable",
)
def test_short_render_has_expected_media_properties(tmp_path: Path) -> None:
    config = replace(load_config(ROOT / "project.yaml"), output=tmp_path / "video.mp4")

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
    assert float(metadata["format"]["duration"]) == pytest.approx(5.0, abs=0.01)
