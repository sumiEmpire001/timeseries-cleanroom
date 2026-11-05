# Time Series Cleanroom

A Python standard-library CLI that validates timestamped CSV observations, rejects malformed or non-finite values, removes duplicate timestamps, sorts data, and generates daily count, minimum, maximum, and mean summaries. Rejected records include row numbers and reasons.

## Run

```bash
python cleanroom.py examples/observations.csv
python cleanroom.py examples/observations.csv --output report.json
```

Input columns: `timestamp,value`. Timestamps must be timezone-aware ISO 8601 values, such as `2026-11-05T09:00:00Z`. Duplicate detection uses normalized UTC timestamps and keeps the first valid occurrence.

## Tests

```bash
python -m unittest discover -s tests -v
```

Seven tests run in GitHub Actions on Python 3.10, 3.12, and 3.13. This tool does not impute missing readings or infer units; use its output as an initial quality report rather than a scientific validation.
