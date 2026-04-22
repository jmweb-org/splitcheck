# Changelog

All notable changes to this project are documented here. The format is based
on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-04-24

### Added
- Docker image and a published container entry point.
- Continuous integration across Python 3.10, 3.11 and 3.12.
- Expanded documentation, including scope and limitations.

## [0.1.0] - 2026-04-20

### Added
- `check` command: detect exact and normalized row overlap between two or more
  splits, with leakage as a fraction of the target split and a CI gate.
- Whole-row or single-column comparison (`--on`).
- CSV, Parquet, JSON Lines and plain-text input through polars, with clean
  errors on malformed files.
- `--max-leakage`, `--json` and `--no-check` to tune gating and output.

[0.2.0]: https://github.com/jmweb-org/splitcheck/releases/tag/v0.2.0
[0.1.0]: https://github.com/jmweb-org/splitcheck/releases/tag/v0.1.0
