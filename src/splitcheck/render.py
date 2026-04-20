"""Render leakage results for the terminal and as JSON."""

from __future__ import annotations

from rich.console import Group
from rich.table import Table
from rich.text import Text

from splitcheck.overlap import OverlapResult


def results_to_json(results: list[OverlapResult]) -> list[dict]:
    return [
        {
            "source": r.source,
            "target": r.target,
            "target_size": r.target_size,
            "exact_overlap": r.exact_overlap,
            "normalized_overlap": r.normalized_overlap,
            "exact_fraction": round(r.exact_fraction, 6),
            "normalized_fraction": round(r.normalized_fraction, 6),
            "examples": list(r.examples),
        }
        for r in results
    ]


def render_table(results: list[OverlapResult], threshold: float) -> Group:
    if not results:
        return Group(Text("no leakage detected", style="green"))
    table = Table(box=None, pad_edge=False)
    table.add_column("target")
    table.add_column("in source", style="cyan")
    table.add_column("exact", justify="right")
    table.add_column("normalized", justify="right")
    table.add_column("leakage", justify="right")
    for r in results:
        style = "bold red" if r.normalized_fraction > threshold else "yellow"
        table.add_row(
            r.target,
            r.source,
            f"{r.exact_overlap}",
            f"{r.normalized_overlap}",
            Text(f"{r.normalized_fraction:.1%}", style=style),
        )
    return Group(table)
