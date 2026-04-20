"""Command-line interface for splitcheck."""

from __future__ import annotations

import json
import sys

import typer
from rich.console import Console

from splitcheck import __version__
from splitcheck.check import check_splits, over_threshold, worst_leakage
from splitcheck.dataset import named_splits
from splitcheck.render import render_table, results_to_json

app = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
    help="Detect row overlap and leakage between dataset splits.",
)
_out = Console()
_err = Console(stderr=True)

EXIT_OK = 0
EXIT_LEAKAGE = 1
EXIT_BAD_INPUT = 2


def _version_callback(value: bool) -> None:
    if value:
        _out.print(f"splitcheck {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    _version: bool = typer.Option(
        False,
        "--version",
        callback=_version_callback,
        is_eager=True,
        help="Show the version and exit.",
    ),
) -> None:
    """splitcheck command-line interface."""


@app.command("check")
def check(
    splits: list[str] = typer.Argument(..., help="Two or more split files."),
    on: str = typer.Option(None, "--on", help="Compare a single column instead of whole rows."),
    max_leakage: float = typer.Option(
        0.0, "--max-leakage", help="Fail above this leakage fraction."
    ),
    as_json: bool = typer.Option(False, "--json", help="Emit results as JSON."),
    fail: bool = typer.Option(
        True, "--check/--no-check", help="Exit non-zero when leakage exceeds the limit."
    ),
) -> None:
    """Compare splits and report rows that leak from one into another."""

    if len(splits) < 2:
        _err.print("splitcheck: need at least two split files")
        raise typer.Exit(EXIT_BAD_INPUT)
    try:
        data = named_splits(splits, on)
    except (OSError, ValueError) as exc:
        _err.print(f"splitcheck: {exc}")
        raise typer.Exit(EXIT_BAD_INPUT) from exc

    results = check_splits(data)
    if as_json:
        _out.print_json(json.dumps(results_to_json(results)))
    else:
        _out.print(render_table(results, max_leakage))
        _err.print(f"splitcheck: worst leakage {worst_leakage(results):.1%}")

    if fail and over_threshold(results, max_leakage):
        raise typer.Exit(EXIT_LEAKAGE)


def entrypoint() -> None:
    try:
        app()
    except KeyboardInterrupt:  # pragma: no cover - interactive only
        print("splitcheck: interrupted", file=sys.stderr)
        raise SystemExit(130) from None
