# Pandas DataFrames for Log Analysis

Pandas is useful for exploring tabular telemetry and computing operational summaries.

```python
import pandas as pd

df = pd.read_csv("access.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
df["status"] = pd.to_numeric(df["status"], errors="coerce")
df["duration_ms"] = pd.to_numeric(df["duration_ms"], errors="coerce")

valid = df.dropna(subset=["timestamp", "status", "duration_ms"]).copy()
valid["is_error"] = valid["status"] >= 500

summary = valid.groupby("service").agg(
    requests=("status", "size"),
    errors=("is_error", "sum"),
    p95_latency_ms=("duration_ms", lambda s: s.quantile(0.95)),
)
summary["error_rate"] = summary["errors"] / summary["requests"]
print(summary)
```

For large files, process chunks or use a log platform/columnar store. Validate units, timezone and missing values before interpreting results.
