from decimal import Decimal
from pathlib import Path

import pytest

from scripts.make_video import (
    ProjectConfig,
    RenderError,
    build_ffmpeg_command,
    build_filtergraph,
    format_duration,
    load_config,
)


def write_project(path: Path, extra: str = "") -> None:
    path.write_text(
        """\
version: 1
audio: media/audio.wav
artwork: media/artwork.png
title: My New Song
artist: Nobuaki
output: output/video.mp4
"""
        + extra,
        encoding="utf-8",
    )


def test_load_config_resolves_paths_from_project_file(tmp_path: Path) -> None:
    project_file = tmp_path / "project" / "song.yaml"
    project_file.parent.mkdir()
    write_project(project_file)

    config = load_config(project_file)

    assert config.source == project_file
    assert config.audio == project_file.parent / "media/audio.wav"
    assert config.artwork == project_file.parent / "media/artwork.png"
    assert config.output == project_file.parent / "output/video.mp4"
    assert config.title == "My New Song"
    assert config.artist == "Nobuaki"


@pytest.mark.parametrize(
    ("content", "message"),
    [
        ("version: 2\n", "'version' must be 1"),
        ("version: 1\naudio: audio.wav\n", "'artwork' must be a non-empty string"),
        (
            "version: 1\naudio: a.wav\nartwork: a.png\ntitle: ''\nartist: Artist\noutput: o.mp4\n",
            "'title' must be a non-empty string",
        ),
        (
            "version: 1\naudio: a.wav\nartwork: a.png\ntitle: T\nartist: A\n"
            "output: o.mp4\nwidth: 1080\n",
            "Unknown project field(s): width",
        ),
    ],
)
def test_load_config_rejects_invalid_projects(tmp_path: Path, content: str, message: str) -> None:
    project_file = tmp_path / "project.yaml"
    project_file.write_text(content, encoding="utf-8")

    with pytest.raises(RenderError) as caught:
        load_config(project_file)
    assert message in str(caught.value)


def test_load_config_rejects_output_that_overwrites_input(tmp_path: Path) -> None:
    project_file = tmp_path / "project.yaml"
    write_project(project_file, extra="output: media/audio.wav\n")

    with pytest.raises(RenderError, match="must not overwrite an input file"):
        load_config(project_file)


def test_five_second_audio_uses_last_frame_index_149() -> None:
    filtergraph = build_filtergraph(Decimal("5.000000"), Path("title.txt"), Path("artist.txt"))

    assert "zoompan=z='1+on/149'" in filtergraph
    assert "drawtext=" in filtergraph
    assert "showwaves=" in filtergraph


def test_fractional_duration_rounds_frame_count_up() -> None:
    filtergraph = build_filtergraph(Decimal("1.01"), Path("title.txt"), Path("artist.txt"))

    assert "zoompan=z='1+on/30'" in filtergraph


def test_command_uses_project_paths_and_preserves_output_settings(tmp_path: Path) -> None:
    config = ProjectConfig(
        source=tmp_path / "project.yaml",
        audio=tmp_path / "audio.wav",
        artwork=tmp_path / "artwork.png",
        title="Title",
        artist="Artist",
        output=tmp_path / "video.mp4",
    )

    command = build_ffmpeg_command(
        config, Decimal("5.000000"), tmp_path / "title.txt", tmp_path / "artist.txt"
    )

    assert command[-3:] == ["-t", "5", str(config.output)]
    assert str(config.artwork) in command
    assert str(config.audio) in command
    assert "libx264" in command
    assert "aac" in command


def test_duration_format_does_not_use_exponent_notation() -> None:
    assert format_duration(Decimal("0.000001")) == "0.000001"
