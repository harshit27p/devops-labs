# Lab 03 — Scrape an Application with ServiceMonitor

## Objective

Understand the complete ServiceMonitor discovery chain.

## Important prerequisite

The included sample Nginx container does not expose Prometheus metrics. This lab first deploys it to inspect the Service, then asks you to substitute an application/exporter that exposes a real `/metrics` endpoint and a named Service port `metrics`. Do not expect a successful scrape from the sample Nginx workload as written.

## Deploy sample workload

```bash
kubectl apply -f ../manifests/namespace.yaml
kubectl apply -f ../manifests/sample-app.yaml
kubectl get svc,endpoints -n observability-demo
```

## Add a metrics-enabled application

Use an application or exporter appropriate to your environment. Ensure its Service has:
- label `app: sample-app` (or adjust the monitor selector);
- a named port `metrics`;
- a target port where the process serves `/metrics`.

Update the ServiceMonitor if the labels, namespace, port name, path, or scheme differ.

## Apply and inspect

```bash
kubectl apply -f ../manifests/service-monitor.yaml
kubectl get servicemonitor -n observability-demo --show-labels
kubectl describe servicemonitor sample-app -n observability-demo
```

In Prometheus, inspect Status → Targets. If no target appears, verify Prometheus selects the monitor namespace and `release: monitoring` label. If the target is DOWN, inspect endpoint port/path, network policy, TLS, and application response.

## Cleanup

```bash
kubectl delete -f ../manifests/service-monitor.yaml
kubectl delete -f ../manifests/sample-app.yaml
kubectl delete -f ../manifests/namespace.yaml
```
