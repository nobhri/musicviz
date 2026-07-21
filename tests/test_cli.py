from pathlib import Path
from unittest.mock import Mock

import pytest

from musicviz import cli
from musicviz.render import ProjectConfig, RenderError


def test_render_command_loads_and_renders_project(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    project = tmp_path / "project.yaml"
    config = ProjectConfig(
        source=project,
        audio=tmp_path / "audio.wav",
        artwork=tmp_path / "artwork.png",
        title="Title",
        artist="Artist",
        output=tmp_path / "video.mp4",
    )
    load_config = Mock(return_value=config)
    render = Mock()
    monkeypatch.setattr(cli, "load_config", load_config)
    monkeypatch.setattr(cli, "render", render)

    result = cli.main(["render", str(project)])

    assert result == 0
    load_config.assert_called_once_with(project)
    render.assert_called_once_with(config)
    assert capsys.readouterr().out == f"Rendered {config.output}\n"


def test_render_error_is_reported(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(cli, "load_config", Mock(side_effect=RenderError("broken project")))

    result = cli.main(["render", "project.yaml"])

    assert result == 1
    assert capsys.readouterr().err == "error: broken project\n"


@pytest.mark.parametrize("arguments", [[], ["unknown"], ["render"]])
def test_invalid_arguments_exit_with_usage_error(arguments: list[str]) -> None:
    with pytest.raises(SystemExit) as caught:
        cli.main(arguments)

    assert caught.value.code == 2
