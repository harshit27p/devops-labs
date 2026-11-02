# Observability and the Three Pillars

The commonly used telemetry pillars are logs, metrics and traces. Events are also useful for recording discrete state changes.

- **Logs:** individual records describing what happened.
- **Metrics:** numeric measurements over time.
- **Traces:** spans showing a request's path across components.
- **Events:** notable changes such as deployment, scaling or configuration updates.

No single pillar explains every incident. A metric can show a latency spike; logs may explain the error; traces can identify the slow dependency.

## DevOps example
For a checkout API, collect request rate, latency percentiles, error rate, CPU/memory saturation, structured application logs and trace IDs.
