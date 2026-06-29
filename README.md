# splitcheck

[![CI](https://github.com/jmweb-org/splitcheck/actions/workflows/ci.yml/badge.svg)](https://github.com/jmweb-org/splitcheck/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/splitcheck.svg)](https://pypi.org/project/splitcheck/)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Detect rows that leak between dataset splits, and fail CI when they do.

A row that appears in both train and test inflates every metric and is easy to
introduce: a careless `concat`, a re-export, a duplicated record. `splitcheck`
compares your splits and reports how much of one appears in another, both as
exact matches and after normalization, so cosmetic differences do not hide a
leak.

```console
$ splitcheck check train.csv test.csv --on text --max-leakage 0.0
target  in source  exact  normalized  leakage
test    train          1           3     2.1%
splitcheck: worst leakage 2.1%
```

## Install

```console
$ pip install splitcheck
```

Reads CSV, Parquet, JSON Lines, and plain text (one row per line) through polars.

## Usage

```console
$ splitcheck check train.csv test.csv                 # compare whole rows
$ splitcheck check train.csv val.csv test.csv         # all pairs at once
$ splitcheck check train.csv test.csv --on text       # compare one column
$ splitcheck check train.csv test.csv --json          # machine-readable
$ splitcheck check train.csv test.csv --max-leakage 0.01   # allow 1%
$ splitcheck check train.csv test.csv --no-check      # report without failing
```

By default any leakage fails the command (`--max-leakage 0.0`). Raise the limit
to tolerate a known, small overlap.

### In CI

```yaml
- run: splitcheck check data/train.parquet data/test.parquet --on text
```

## How matching works

Each row is reduced to a string: a single column with `--on`, or the whole row
joined tab-separated. Two matches are reported:

- **exact**: identical strings.
- **normalized**: equal after case folding, punctuation removal and whitespace
  collapsing, which catches the same example re-saved with cosmetic changes.

Leakage is the fraction of the **target** split (for example test) whose rows
also appear in a **source** split (for example train). Pairs are checked in both
directions and sorted worst-first.

## Exit codes

| Code | Meaning |
| --- | --- |
| 0 | Checked; leakage within the limit (or `--no-check`) |
| 1 | Leakage exceeded `--max-leakage` |
| 2 | Fewer than two files, or a file was missing or unsupported |

## Scope

Matching is exact or normalized-exact, not fuzzy. Near-duplicates that differ in
wording (paraphrases) are not caught; see the issues for planned MinHash-based
fuzzy matching.

## License

MIT. See [LICENSE](LICENSE).
