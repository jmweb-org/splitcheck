from __future__ import annotations

from splitcheck.normalize import normalize_text
from splitcheck.overlap import overlap


def test_normalize_collapses_case_punct_and_space():
    assert normalize_text("Hello,  World!") == "hello world"
    assert normalize_text("  A\tB \n") == "a b"


def test_normalize_is_idempotent():
    once = normalize_text("Foo - Bar!!")
    assert normalize_text(once) == once


def test_exact_overlap_counts_identical_rows():
    result = overlap(["a", "b", "c"], ["b", "c", "d"])
    assert result.exact_overlap == 2
    assert result.target_size == 3
    assert result.exact_fraction == 2 / 3


def test_normalized_overlap_catches_cosmetic_differences():
    result = overlap(["Hello world"], ["hello, world!"])
    assert result.exact_overlap == 0
    assert result.normalized_overlap == 1
    assert result.normalized_fraction == 1.0


def test_no_overlap():
    result = overlap(["a", "b"], ["x", "y"])
    assert result.exact_overlap == 0
    assert result.normalized_overlap == 0


def test_examples_are_capped():
    source = ["dup"]
    target = ["dup"] * 10
    result = overlap(source, target, max_examples=3)
    assert result.normalized_overlap == 10
    assert len(result.examples) == 3


def test_empty_target_fraction_is_zero():
    result = overlap(["a"], [])
    assert result.normalized_fraction == 0.0
