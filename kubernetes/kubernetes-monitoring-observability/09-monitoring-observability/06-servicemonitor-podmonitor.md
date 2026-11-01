# 06 — ServiceMonitor and PodMonitor

## ServiceMonitor

A `ServiceMonitor` tells Prometheus Operator how to discover and scrape endpoints associated with Kubernetes Services. It selects Services using label selectors and identifies the Service port by its **port name**, not necessarily its numeric port.

Important matching layers:

1. The Prometheus resource must select the ServiceMonitor's labels.
2. The Prometheus resource must allow the ServiceMonitor namespace.
3. The ServiceMonitor must select the intended Service labels and namespace.
4. The Service must expose a named port matching the monitor's `endpoints[].port`.
5. The target endpoint must serve metrics at the configured path and scheme.

## PodMonitor

A `PodMonitor` selects Pods directly and can be useful when a Service is not appropriate or when monitoring Pod endpoints directly. It still needs to be selected by the Prometheus resource.

## Example ServiceMonitor

See `../manifests/service-monitor.yaml`. It assumes:
- Prometheus Operator CRDs are installed.
- A Service named `sample-app` exists in namespace `observability-demo`.
- That Service has label `app: sample-app`.
- It exposes a named port `metrics` and serves `/metrics`.

## Debug in layers

```bash
kubectl get servicemonitor -A --show-labels
kubectl get prometheus -A --show-labels
kubectl get svc,endpoints,endpointslices -n observability-demo
kubectl describe servicemonitor sample-app -n observability-demo
```

Then inspect Prometheus **Status → Targets**. A missing target usually indicates discovery/selector/RBAC problems. A target marked DOWN indicates a scrape path, port, protocol, TLS, timeout, or endpoint issue.

## Relabeling

Relabeling can keep or drop targets and rewrite labels. Use it to control scrape scope and normalize target metadata. Avoid dropping labels required for meaningful aggregation, and avoid creating high-cardinality labels.

## Security

Do not scrape arbitrary endpoints from untrusted namespaces. Limit namespace selection, network reachability, and credentials. If an endpoint requires TLS or authentication, use the supported Operator fields and external secret management patterns; never commit real credentials.

## Further reading

- https://prometheus-operator.dev/docs/developer/getting-started/
- https://prometheus-operator.dev/docs/api-reference/api/
