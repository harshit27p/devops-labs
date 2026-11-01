# 14 — Kubernetes Monitoring & Observability Interview Questions

## Fundamentals

**1. What is observability?**  
The ability to infer internal system state from emitted telemetry, especially when investigating unknown problems.

**2. What are the three common telemetry pillars?**  
Metrics, logs, and traces. Profiles and events can add further context.

**3. Monitoring vs observability?**  
Monitoring checks known conditions; observability supports investigation of system behavior, including unexpected failure modes.

**4. Explain RED and USE.**  
RED covers Rate, Errors, Duration for request services. USE covers Utilization, Saturation, Errors for resources.

## Prometheus

**5. How does Prometheus collect metrics?**  
Usually by discovering targets and periodically scraping their HTTP metrics endpoints.

**6. What is a time series?**  
A metric name plus a unique label set, with timestamped samples.

**7. Counter vs gauge?**  
A counter increases monotonically except reset; a gauge can rise and fall.

**8. Why use `rate()` on counters?**  
It estimates per-second increase over a range and accounts for counter resets.

**9. What is cardinality?**  
The number of distinct time series. Unbounded labels can create expensive series growth.

**10. What is Alertmanager responsible for?**  
Grouping, deduplication, routing, silencing, and inhibition of alerts.

## Kubernetes components

**11. Metrics Server vs Prometheus?**  
Metrics Server supplies recent resource metrics to the Metrics API and `kubectl top`; Prometheus provides broader time-series scraping, querying, and alerting.

**12. kube-state-metrics vs node-exporter?**  
kube-state-metrics exposes Kubernetes object state; node-exporter exposes host OS/hardware metrics.

**13. What is a ServiceMonitor?**  
A Prometheus Operator custom resource that selects Services and describes scrape endpoints.

**14. Why might a ServiceMonitor not be discovered?**  
Prometheus selectors may not match its labels/namespace, or its Service selector/port configuration may be wrong.

## Grafana, logs, and traces

**15. Is Grafana a metrics database?**  
No. It visualizes data from backends such as Prometheus and Loki.

**16. Why use structured logs?**  
They are easier to parse, filter, correlate, and analyze consistently.

**17. What is a trace span?**  
A timed operation within a trace, with parent/child relationships and attributes.

**18. What is OpenTelemetry?**  
A vendor-neutral set of APIs, SDKs, conventions, and collectors for telemetry generation and export.

**19. Why should trace IDs not be metric labels?**  
They create very high cardinality and can overwhelm a metrics backend.

## Reliability

**20. Define SLI, SLO, and SLA.**  
SLI is a measured indicator; SLO is its target; SLA is an external agreement, often contractual.

**21. What is an error budget?**  
The allowed unreliability implied by an SLO over its measurement window.

**22. What makes an alert actionable?**  
It indicates meaningful risk or impact, has an owner, clear response steps, and a runbook.

**23. How do you reduce alert fatigue?**  
Alert on user impact, use sustained conditions and grouping, tune thresholds, remove duplicate alerts, and review false positives.

**24. How would you investigate high API latency?**  
Check RED metrics, compare service and dependency latency, inspect traces for slow spans, correlate logs, and inspect saturation/resource metrics.

**25. How do you monitor the monitoring stack?**  
Track scrape health, ingestion/drop rates, rule evaluation, TSDB capacity, notification failures, collector queues, and backend query/ingestion health.

## Scenario practice

- Prometheus target is DOWN but the Pod is Ready. What do you check?
- `kubectl top pods` works but Grafana has no container metrics. Why?
- A ServiceMonitor exists but no target appears. Explain the selector chain.
- A notification is not delivered although an alert is firing. Trace the Alertmanager route.
- A service's p99 latency rises while CPU remains low. Which signals do you inspect?
