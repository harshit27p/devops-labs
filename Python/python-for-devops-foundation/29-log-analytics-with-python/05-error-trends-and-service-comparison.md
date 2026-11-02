# Error Trends and Service Comparison

Compare services using rates and distributions, not raw counts alone.

## Useful comparisons
- Error rate by service and environment
- p50/p95/p99 latency
- Request volume
- Timeout counts
- Retry counts
- Queue depth and age

A service receiving ten times more traffic may naturally have more errors while maintaining a lower error rate. Include sample size and time window in every summary.

## Exercise
Create a report comparing two synthetic services over hourly windows. Highlight intervals where error rate exceeds a configurable threshold and show request counts alongside the rate.
