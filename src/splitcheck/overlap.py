"""Compute exact and normalized overlap between two collections of rows.

Leakage is asymmetric: what matters is the fraction of the *target* split
(typically test) that also appears in the *source* split (typically train).
Both an exact match and a normalized match are reported.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field

from splitcheck.normalize import normalize_text


@dataclass(frozen=True, slots=True)
class OverlapResult:
    source: str
    target: str
    target_size: int
    exact_overlap: int
    normalized_overlap: int
    examples: tuple[str, ...] = field(default_factory=tuple)

    @property
    def exact_fraction(self) -> float:
        return self.exact_overlap / self.target_size if self.target_size else 0.0

    @property
    def normalized_fraction(self) -> float:
        return self.normalized_overlap / self.target_size if self.target_size else 0.0


def overlap(
    source_rows: Sequence[str],
    target_rows: Sequence[str],
    *,
    source_name: str = "source",
    target_name: str = "target",
    max_examples: int = 5,
) -> OverlapResult:
    source_exact = set(source_rows)
    source_norm = {normalize_text(r) for r in source_rows}

    exact = 0
    normalized = 0
    examples: list[str] = []
    for row in target_rows:
        is_exact = row in source_exact
        is_norm = normalize_text(row) in source_norm
        if is_exact:
            exact += 1
        if is_norm:
            normalized += 1
            if len(examples) < max_examples:
                examples.append(row)
    return OverlapResult(
        source=source_name,
        target=target_name,
        target_size=len(target_rows),
        exact_overlap=exact,
        normalized_overlap=normalized,
        examples=tuple(examples),
    )
