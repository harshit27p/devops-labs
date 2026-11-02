# Time-Window Aggregation

Time-window aggregation reveals patterns that individual log records hide.

```python
import pandas as pd

df = pd.read_csv("access.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
df = df.dropna(subset=["timestamp"]).set_index("timestamp")

requests_per_5m = df["status"].resample("5min").count()
errors_per_5m = df["status"].ge(500).resample("5min").sum()
```

## Considerations
- Use consistent timezones.
- Choose a window appropriate to traffic volume.
- Distinguish zero events from missing telemetry.
- Account for late-arriving records.
- Avoid interpreting small samples as stable rates.
