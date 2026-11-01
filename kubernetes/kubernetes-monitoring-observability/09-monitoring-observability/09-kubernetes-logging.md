# 09 — Kubernetes Logging

## Container log fundamentals

Applications should generally write logs to stdout and stderr. The container runtime and kubelet manage container log files, and `kubectl logs` provides a convenient interface.

```bash
kubectl logs deploy/sample-app -n observability-demo
kubectl logs pod/<pod-name> -n observability-demo --previous
kubectl logs pod/<pod-name> -n observability-demo -c <container-name> --since=30m
kubectl logs -f deploy/sample-app -n observability-demo
```

`--previous` retrieves logs from a previous terminated container instance when available. Logs are not guaranteed to persist indefinitely; node-level rotation and retention policies apply.

## Centralized logging pipeline

A common architecture uses a node-level collector deployed as a DaemonSet. It reads container logs, enriches records with Kubernetes metadata, applies parsing/filtering, and forwards them to a backend such as Loki, Elasticsearch/OpenSearch, or a managed logging service.

Examples of collectors include Fluent Bit, Vector, and OpenTelemetry Collector. Select one based on operational requirements, supported inputs/outputs, resource footprint, and team expertise.

## Structured logging

Prefer structured JSON logs with:
- timestamp in a consistent format;
- severity;
- service and environment;
- message;
- trace/span correlation identifiers where appropriate;
- stable error code.

Do not log passwords, tokens, session cookies, private keys, or unnecessary personal data. Redact sensitive fields before export.

## Loki concepts

Grafana Loki indexes labels and stores log content in chunks. Labels should be low-cardinality and stable, such as cluster, namespace, app, and environment. Do not use request IDs, user IDs, or arbitrary log text as Loki labels; use structured metadata or parsed fields where supported.

## Troubleshooting

1. Confirm the application writes to stdout/stderr.
2. Inspect `kubectl logs` locally.
3. Check collector DaemonSet readiness on every node.
4. Inspect collector errors, buffer pressure, and output connectivity.
5. Verify backend ingestion limits, authentication, and retention.
6. Confirm timestamps, labels, parsing, and multiline handling.
7. Check disk pressure and log rotation on nodes.

## Further reading

- https://kubernetes.io/docs/concepts/cluster-administration/logging/
- https://grafana.com/docs/loki/latest/
- https://docs.fluentbit.io/
