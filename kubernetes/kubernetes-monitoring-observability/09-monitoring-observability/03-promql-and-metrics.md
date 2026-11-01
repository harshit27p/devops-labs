# 03 — Metrics, Labels, and PromQL

## Metric types

- **Counter:** monotonically increases except on process restart; use `rate()` or `increase()` for change over time.
- **Gauge:** can increase or decrease, e.g. active connections or memory in use.
- **Histogram:** records observations in buckets plus count and sum; useful for latency distributions and quantile estimation.
- **Summary:** calculates quantiles in the instrumented process; quantiles generally cannot be aggregated across instances.

Prometheus stores float samples and label sets. Metric type semantics are important when interpreting and querying the data.

## Labels and cardinality

A series is unique for each combination of metric name and label values. Adding a label with thousands of possible values can create thousands of series per metric. Avoid user IDs, session IDs, trace IDs, raw paths, and unbounded error strings as metric labels.

Prefer normalized route labels such as `/orders/{id}` instead of `/orders/12345`.

## PromQL examples

```promql
# CPU usage by namespace (example based on container metrics)
sum by (namespace) (rate(container_cpu_usage_seconds_total[5m]))

# Memory working set by Pod
sum by (namespace, pod) (container_memory_working_set_bytes)

# Request rate by service
sum by (service) (rate(http_requests_total[5m]))

# Error ratio; adapt labels and metric names to your app
sum(rate(http_requests_total{status=~"5.."}[5m]))
/
sum(rate(http_requests_total[5m]))

# 95th percentile from a classic histogram
histogram_quantile(
  0.95,
  sum by (le, service) (rate(http_request_duration_seconds_bucket[5m]))
)

# Current unavailable replicas (metric names depend on kube-state-metrics version)
kube_deployment_status_replicas_unavailable
```

## Useful functions

- `rate()` estimates per-second counter increase over a range and handles counter resets.
- `irate()` uses the last two samples; useful for volatile graphs, often too noisy for alerts.
- `increase()` estimates total counter increase over a range.
- `sum by (...)` aggregates while retaining selected labels.
- `sum without (...)` aggregates while dropping selected labels.
- `histogram_quantile()` estimates quantiles from histogram buckets.
- `absent()` can detect a missing series, but target health and expected inventory should also be considered.

## Query design

1. Confirm the metric exists in the Prometheus expression browser.
2. Inspect its labels before writing aggregation.
3. Check units and whether it is a counter or gauge.
4. Use a range window appropriate to scrape interval and signal behavior.
5. Test queries against multiple replicas and failure cases.
6. Avoid expensive high-cardinality queries on heavily loaded systems.

## Recording rules

Recording rules precompute frequently used expressions into new time series. Name them clearly and document units and labels. Use them for expensive dashboard queries and consistent SLI calculations.

## Further reading

- https://prometheus.io/docs/prometheus/latest/querying/basics/
- https://prometheus.io/docs/prometheus/latest/querying/functions/
- https://prometheus.io/docs/practices/naming/
