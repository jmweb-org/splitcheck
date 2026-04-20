"""Read split files and extract the rows to compare."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

import polars as pl


def read_frame(path: str | Path) -> pl.DataFrame:
    path = Path(path)
    suffix = path.suffix.lower()
    try:
        if suffix == ".csv":
            return pl.read_csv(path, infer_schema_length=0)
        if suffix in {".parquet", ".pq"}:
            return pl.read_parquet(path)
        if suffix in {".jsonl", ".ndjson"}:
            return pl.read_ndjson(path)
        if suffix == ".json":
            return pl.read_json(path)
        if suffix in {".txt", ""}:
            return pl.DataFrame({"text": path.read_text(encoding="utf-8").splitlines()})
    except pl.exceptions.PolarsError as exc:
        raise ValueError(f"could not parse {path}: {exc}") from exc
    raise ValueError(f"unsupported file type: {path.suffix or '(none)'}")


def extract_rows(frame: pl.DataFrame, on: str | None = None) -> list[str]:
    """Return one string per row: a single column if ``on`` is given, else the
    whole row joined into a stable, tab-separated string.
    """

    if on is not None:
        if on not in frame.columns:
            raise ValueError(f"column not found: {on}")
        return ["" if v is None else str(v) for v in frame.get_column(on).to_list()]
    rows: list[str] = []
    for record in frame.iter_rows():
        rows.append("\t".join("" if v is None else str(v) for v in record))
    return rows


def rows_from_file(path: str | Path, on: str | None = None) -> list[str]:
    return extract_rows(read_frame(path), on)


def named_splits(paths: Sequence[str | Path], on: str | None = None) -> dict[str, list[str]]:
    return {Path(p).stem: rows_from_file(p, on) for p in paths}
