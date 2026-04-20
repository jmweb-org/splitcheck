from __future__ import annotations

import json

import polars as pl
import pytest
from typer.testing import CliRunner

from splitcheck import __version__
from splitcheck import cli as cli_module
from splitcheck.dataset import extract_rows, read_frame, rows_from_file

runner = CliRunner()


def _csv(tmp_path, name, frame):
    path = tmp_path / name
    frame.write_csv(path)
    return path


def test_extract_rows_whole_row():
    frame = pl.DataFrame({"a": [1, 2], "b": ["x", "y"]})
    assert extract_rows(frame) == ["1\tx", "2\ty"]


def test_extract_rows_single_column():
    frame = pl.DataFrame({"text": ["hello", "world"], "label": [0, 1]})
    assert extract_rows(frame, on="text") == ["hello", "world"]


def test_extract_rows_unknown_column_raises():
    frame = pl.DataFrame({"a": [1]})
    with pytest.raises(ValueError):
        extract_rows(frame, on="missing")


def test_read_txt_lines(tmp_path):
    path = tmp_path / "data.txt"
    path.write_text("one\ntwo\nthree\n")
    assert read_frame(path).height == 3


def test_read_unsupported_extension(tmp_path):
    path = tmp_path / "data.bin"
    path.write_bytes(b"\x00\x01")
    with pytest.raises(ValueError):
        read_frame(path)


def test_rows_from_file(tmp_path):
    path = _csv(tmp_path, "t.csv", pl.DataFrame({"text": ["a", "b"]}))
    assert rows_from_file(path, on="text") == ["a", "b"]


def test_version():
    result = runner.invoke(cli_module.app, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.stdout


def test_cli_detects_leakage_and_exits_nonzero(tmp_path):
    train = _csv(tmp_path, "train.csv", pl.DataFrame({"text": ["a", "b", "c"]}))
    test = _csv(tmp_path, "test.csv", pl.DataFrame({"text": ["c", "x"]}))
    result = runner.invoke(
        cli_module.app, ["check", str(train), str(test), "--on", "text", "--json"]
    )
    assert result.exit_code == cli_module.EXIT_LEAKAGE
    payload = json.loads(result.stdout)
    leak = next(r for r in payload if r["target"] == "test" and r["source"] == "train")
    assert leak["normalized_overlap"] == 1


def test_cli_clean_splits_pass(tmp_path):
    train = _csv(tmp_path, "train.csv", pl.DataFrame({"text": ["a", "b"]}))
    test = _csv(tmp_path, "test.csv", pl.DataFrame({"text": ["x", "y"]}))
    result = runner.invoke(cli_module.app, ["check", str(train), str(test), "--on", "text"])
    assert result.exit_code == 0


def test_cli_no_check_does_not_fail(tmp_path):
    train = _csv(tmp_path, "train.csv", pl.DataFrame({"text": ["a", "b"]}))
    test = _csv(tmp_path, "test.csv", pl.DataFrame({"text": ["a"]}))
    result = runner.invoke(
        cli_module.app, ["check", str(train), str(test), "--on", "text", "--no-check"]
    )
    assert result.exit_code == 0


def test_cli_needs_two_files(tmp_path):
    train = _csv(tmp_path, "train.csv", pl.DataFrame({"text": ["a"]}))
    result = runner.invoke(cli_module.app, ["check", str(train)])
    assert result.exit_code == cli_module.EXIT_BAD_INPUT
