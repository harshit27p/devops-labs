# Metrics, Labels and Cardinality

Metrics are time-stamped numeric observations. Labels add dimensions such as service, region or response class.

## Common metric types
- Counter: monotonically increasing total, such as requests.
- Gauge: value that can rise or fall, such as queue depth.
- Histogram: distribution buckets, often used for latency.
- Summary: client-side distribution statistics in some telemetry systems.

## Cardinality
A label with many possible values creates many time series. Avoid labels such as user ID, request ID or raw URL.

Prefer bounded dimensions:
- `service`
- `environment`
- `region`
- `status_class`

Use logs or traces for high-cardinality identifiers.
