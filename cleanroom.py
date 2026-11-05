"""Validate, deduplicate and aggregate timestamped CSV observations."""
import argparse
import collections
import csv
import datetime as dt
import json
import math


def parse_timestamp(value):
    parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timezone required")
    return parsed.astimezone(dt.timezone.utc)


def clean(rows):
    accepted = {}
    errors = []
    for index, row in enumerate(rows, start=2):
        try:
            timestamp = parse_timestamp(row["timestamp"])
            value = float(row["value"])
            if not math.isfinite(value):
                raise ValueError("value must be finite")
            key = timestamp.isoformat().replace("+00:00", "Z")
            if key in accepted:
                errors.append({"row": index, "reason": "duplicate timestamp"})
                continue
            accepted[key] = value
        except (KeyError, TypeError, ValueError, AttributeError) as error:
            errors.append({"row": index, "reason": str(error)})
    return sorted(accepted.items()), errors


def daily_summary(observations):
    buckets = collections.defaultdict(list)
    for timestamp, value in observations:
        buckets[timestamp[:10]].append(value)
    return [{"date": date, "count": len(values), "min": min(values),
             "max": max(values), "mean": round(sum(values) / len(values), 4)}
            for date, values in sorted(buckets.items())]


def run(source, output):
    with open(source, newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    accepted, errors = clean(rows)
    report = {"accepted": len(accepted), "rejected": len(errors),
              "daily": daily_summary(accepted), "errors": errors}
    text = json.dumps(report, indent=2)
    if output:
        with open(output, "w", encoding="utf-8") as file:
            file.write(text + "\n")
    else:
        print(text)
    return report


def main():
    parser = argparse.ArgumentParser(description="Clean time series CSV data")
    parser.add_argument("source")
    parser.add_argument("--output")
    args = parser.parse_args()
    run(args.source, args.output)


if __name__ == "__main__":
    main()
