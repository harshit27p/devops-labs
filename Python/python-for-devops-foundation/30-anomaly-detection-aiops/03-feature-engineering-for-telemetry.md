# Feature Engineering for Telemetry

Models learn from features, not raw operational meaning. Choose features that represent the behavior you want to detect.

## Candidate features
- Counts of INFO/WARNING/ERROR/CRITICAL events per interval
- Error ratio and request volume
- p95 latency
- CPU and memory utilization
- Restart count
- Queue depth and oldest-message age

## Preparation
- Aggregate into consistent time buckets.
- Scale or transform skewed features when appropriate.
- Handle missing intervals deliberately.
- Avoid leaking future information into training.
- Exclude identifiers that merely memorize individual events.

Document feature definitions, units and aggregation windows.
