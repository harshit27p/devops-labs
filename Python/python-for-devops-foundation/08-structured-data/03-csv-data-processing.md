# CSV Data Processing

CSV is common for inventory exports, audit reports and operational summaries. Values are generally read as strings and need validation and conversion.

## Read records
```python
import csv

with open("instances.csv", newline="", encoding="utf-8") as handle:
    for row in csv.DictReader(handle):
        print(row["instance_id"], row["state"])
```

## Validate and convert
```python
def parse_disk_percent(value):
    try:
        number = float(value)
    except ValueError as exc:
        raise ValueError(f"invalid disk percentage: {value!r}") from exc
    if not 0 <= number <= 100:
        raise ValueError("disk percentage must be 0..100")
    return number
```

## Write a report
```python
import csv

rows = [
    {"host": "web-01", "status": "healthy", "disk_used_pct": 61.2},
    {"host": "db-01", "status": "warning", "disk_used_pct": 84.7},
]
with open("health-report.csv", "w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)
```

Validate headers, define how blank cells are handled, report malformed row numbers and keep source data unchanged. When exporting data for spreadsheet users, consider formula injection from cells beginning with `=`, `+`, `-` or `@`.

Exercises: count hosts by state, identify invalid records and export hosts above a disk threshold.
