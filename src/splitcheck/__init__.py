"""splitcheck: detect row overlap and leakage between dataset splits."""

from splitcheck.check import check_splits, over_threshold, worst_leakage
from splitcheck.dataset import named_splits, rows_from_file
from splitcheck.normalize import normalize_text
from splitcheck.overlap import OverlapResult, overlap

__version__ = "0.1.0"

__all__ = [
    "OverlapResult",
    "__version__",
    "check_splits",
    "named_splits",
    "normalize_text",
    "over_threshold",
    "overlap",
    "rows_from_file",
    "worst_leakage",
]
