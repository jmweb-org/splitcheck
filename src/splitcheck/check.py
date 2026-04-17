"""Check a set of named splits for leakage between every ordered pair."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from splitcheck.overlap import OverlapResult, overlap


def check_splits(
    splits: Mapping[str, Sequence[str]],
    *,
    max_examples: int = 5,
) -> list[OverlapResult]:
    """Return the overlap of every split (target) against every other (source).

    Only pairs with at least one normalized match are returned, sorted by
    leakage fraction so the worst offenders come first.
    """

    names = list(splits)
    results: list[OverlapResult] = []
    for target in names:
        for source in names:
            if source == target:
                continue
            result = overlap(
                splits[source],
                splits[target],
                source_name=source,
                target_name=target,
                max_examples=max_examples,
            )
            if result.normalized_overlap > 0:
                results.append(result)
    results.sort(key=lambda r: (-r.normalized_fraction, r.target, r.source))
    return results


def worst_leakage(results: Sequence[OverlapResult]) -> float:
    return max((r.normalized_fraction for r in results), default=0.0)


def over_threshold(results: Sequence[OverlapResult], max_leakage: float) -> bool:
    return worst_leakage(results) > max_leakage
