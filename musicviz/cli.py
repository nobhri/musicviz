"""Command-line interface for MusicViz."""

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from musicviz.render import RenderError, load_config, render


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="musicviz")
    subparsers = parser.add_subparsers(dest="command", required=True)
    render_parser = subparsers.add_parser("render", help="render a project file")
    render_parser.add_argument("project", metavar="PROJECT.yaml", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)

    try:
        config = load_config(arguments.project)
        render(config)
    except RenderError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    print(f"Rendered {config.output}")
    return 0
