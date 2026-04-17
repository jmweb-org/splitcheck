from __future__ import annotations

from splitcheck.check import check_splits, over_threshold, worst_leakage


def test_check_finds_leakage_from_train_into_test():
    splits = {
        "train": ["a", "b", "c", "d"],
        "test": ["c", "d", "e"],
    }
    results = check_splits(splits)
    # test has 2 of 3 rows present in train
    test_in_train = next(r for r in results if r.target == "test" and r.source == "train")
    assert test_in_train.normalized_overlap == 2
    assert test_in_train.normalized_fraction == 2 / 3


def test_check_clean_splits_return_nothing():
    splits = {"train": ["a", "b"], "test": ["x", "y"]}
    assert check_splits(splits) == []


def test_check_sorted_worst_first():
    splits = {
        "train": ["a", "b", "c"],
        "val": ["a"],  # 100% leak
        "test": ["a", "x", "y", "z"],  # 25% leak
    }
    results = check_splits(splits)
    assert results[0].normalized_fraction >= results[-1].normalized_fraction


def test_worst_leakage_and_threshold():
    splits = {"train": ["a", "b", "c"], "test": ["a", "x"]}
    results = check_splits(splits)
    assert worst_leakage(results) == 0.5
    assert over_threshold(results, 0.4) is True
    assert over_threshold(results, 0.6) is False


def test_threshold_with_no_results():
    assert over_threshold([], 0.0) is False
