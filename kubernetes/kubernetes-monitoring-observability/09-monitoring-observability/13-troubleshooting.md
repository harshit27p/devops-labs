# 13 — Monitoring Troubleshooting Playbook

## First-response checklist

```bash
kubectl get pods -A
kubectl get svc,endpoints,endpointslices -A
kubectl get events -A --sort-by=.lastTimestamp
kubectl top nodes
kubectl top pods -A
```

Start with the symptom and trace the path from workload to collector to backend to visualization/alert.

## Prometheus target is missing

Check:
- Prometheus selectors for ServiceMonitor/PodMonitor labels and namespaces.
- Monitor selectors for Service labels/namespaces.
- Service port name and endpoint path.
- CRD availability and Operator reconciliation events.
- RBAC permissions and namespace restrictions.

## Target is DOWN

Check target error in Prometheus Status → Targets. Common causes:
- wrong port or path;
- Service has no ready endpoints;
- NetworkPolicy blocks traffic;
- TLS or authentication mismatch;
- endpoint returns non-Prometheus content;
- timeout or DNS failure.

## `kubectl top` fails

Check Metrics Server Pod, APIService status, kubelet connectivity, certificate configuration, and cluster network. Remember Metrics Server is separate from Prometheus.

## Grafana shows no data

- Verify data source health and URL.
- Run a simple query such as `up`.
- Confirm time range and timezone.
- Inspect dashboard variables and label filters.
- Check Prometheus query logs/limits if available.

## Alerts do not notify

- Confirm rule exists and is loaded.
- Check whether expression returns a series.
- Check `for` duration and alert state.
- Verify Alertmanager receives the alert.
- Inspect route matching, receiver configuration, silence, and inhibition.
- Check notification integration credentials and delivery errors.

## Logs are missing

- Check `kubectl logs` first.
- Verify collector DaemonSet coverage.
- Inspect tailing permissions and file paths.
- Check parser errors, buffer limits, retries, and backend ingestion.
- Verify labels and time parsing.

## Traces are fragmented

- Verify W3C trace context propagation across HTTP/RPC boundaries.
- Confirm all services export to the intended Collector endpoint.
- Check sampling configuration and Collector routing.
- Confirm clocks are reasonably synchronized.
- Inspect exporter errors and backend ingestion.

## Incident discipline

Capture timestamps, affected namespaces/services, query results, and recent changes. Prefer reversible mitigations. Do not delete monitoring PVCs, CRDs, or namespaces as a first troubleshooting action. Preserve evidence and follow the service's incident process.
