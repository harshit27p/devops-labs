# 09 — Kubernetes Monitoring & Observability

A practical, production-oriented guide to observing Kubernetes clusters and the applications running on them.

## Learning outcomes

By completing this module, you should be able to:

- Distinguish monitoring, observability, telemetry, metrics, logs, and traces.
- Explain Prometheus collection, PromQL, service discovery, and alert evaluation.
- Understand the roles of Metrics Server, kube-state-metrics, and node-exporter.
- Configure Prometheus Operator monitoring resources such as `ServiceMonitor` and `PodMonitor`.
- Build Grafana dashboards and provision data sources safely.
- Design actionable alerts and route them through Alertmanager.
- Understand Kubernetes logging pipelines and centralized log aggregation.
- Instrument services with OpenTelemetry and correlate metrics, logs, and traces.
- Define useful SLIs, SLOs, and error budgets.
- Troubleshoot missing telemetry, noisy alerts, and monitoring-stack failures.

## Module map

| Guide | Topic |
|---|---|
| [01](01-observability-fundamentals.md) | Observability fundamentals and the three pillars |
| [02](02-prometheus-architecture.md) | Prometheus architecture and scrape model |
| [03](03-promql-and-metrics.md) | Metrics, labels, and PromQL |
| [04](04-kubernetes-metrics-components.md) | Metrics Server, kube-state-metrics, node-exporter |
| [05](05-prometheus-operator.md) | Prometheus Operator and kube-prometheus-stack |
| [06](06-servicemonitor-podmonitor.md) | ServiceMonitor and PodMonitor |
| [07](07-grafana-dashboards.md) | Grafana dashboards and provisioning |
| [08](08-alertmanager-and-rules.md) | Alert rules and Alertmanager |
| [09](09-kubernetes-logging.md) | Container logging and log aggregation |
| [10](10-opentelemetry-tracing.md) | OpenTelemetry and distributed tracing |
| [11](11-sli-slo-error-budgets.md) | SLIs, SLOs, and error budgets |
| [12](12-production-observability.md) | Production architecture and operational practices |
| [13](13-troubleshooting.md) | Troubleshooting playbook |
| [14](14-interview-questions.md) | Interview questions and answers |

## Labs

1. [Lab 01 — Inspect Kubernetes resource metrics](labs/lab-01-resource-metrics.md)
2. [Lab 02 — Deploy a Prometheus and Grafana stack](labs/lab-02-prometheus-grafana.md)
3. [Lab 03 — Scrape an application using ServiceMonitor](labs/lab-03-servicemonitor.md)
4. [Lab 04 — Configure alerting and investigate an incident](labs/lab-04-alerting-incident.md)

## Example manifests

- `manifests/namespace.yaml`
- `manifests/sample-app.yaml`
- `manifests/service-monitor.yaml`
- `manifests/prometheus-rule.yaml`
- `manifests/grafana-dashboard-configmap.yaml`

> **Important:** Prometheus Operator custom resources (`ServiceMonitor`, `PrometheusRule`) are not built into Kubernetes. Install a compatible Prometheus Operator and its CRDs before applying those examples. Adapt namespace selectors, labels, ports, and API versions to your installed chart/operator release.

## Prerequisites

- A working Kubernetes cluster and `kubectl`.
- Familiarity with Pods, Deployments, Services, namespaces, labels, and RBAC.
- Helm for the optional `kube-prometheus-stack` lab.
- A cluster with sufficient CPU, memory, and storage for monitoring components.
- Optional: a sample application exposing a Prometheus-compatible `/metrics` endpoint.

Recommended revision: Modules [00](../00-architecture-fundamentals/README.md), [01](../01-workloads-applications/README.md), [02](../02-networking-services/README.md), [04](../04-configmaps-secrets/README.md), [06](../06-scheduling-scaling/README.md), [07](../07-security-rbac/README.md), and [08](../08-helm-package-management/README.md).

## Suggested learning sequence

1. Read guides 01–04 to understand telemetry and Kubernetes metric sources.
2. Deploy the stack in Lab 02 and inspect targets and dashboards.
3. Configure application discovery in Lab 03.
4. Create an alert and walk through an incident in Lab 04.
5. Study logging, tracing, and SLO design before adapting the architecture to production.

## Safety and cost notes

Monitoring systems can consume substantial memory, CPU, disk, and network bandwidth. Start with a small lab configuration, set retention and resource requests/limits, and avoid exposing Prometheus or Grafana publicly without authentication and network controls. Do not put credentials or tokens in dashboards, labels, annotations, or committed manifests.
