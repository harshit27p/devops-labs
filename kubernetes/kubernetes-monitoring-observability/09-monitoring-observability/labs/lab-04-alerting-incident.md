# Lab 04 — Configure Alerting and Investigate an Incident

## Objective

Create a controlled workload failure, observe Kubernetes state, and understand the alerting path.

## Prerequisites

- Prometheus Operator and kube-state-metrics installed.
- Prometheus selects `PrometheusRule` resources with `release: monitoring` in `observability-demo`.
- A disposable cluster.

## Deploy the demo and rule

```bash
kubectl apply -f ../manifests/namespace.yaml
kubectl apply -f ../manifests/sample-app.yaml
kubectl apply -f ../manifests/prometheus-rule.yaml
kubectl get prometheusrule -n observability-demo
```

Inspect the rule in Prometheus or query:

```promql
kube_deployment_status_replicas_unavailable{namespace="observability-demo"}
```

## Simulate an unavailable replica

In a disposable lab only, scale the Deployment to zero:

```bash
kubectl scale deployment/sample-app -n observability-demo --replicas=0
kubectl get deployment sample-app -n observability-demo -w
```

The example alert expression may not fire for scale-to-zero in every metric/version combination because zero desired replicas may mean no unavailable replicas. For a deterministic exercise, instead create a mismatch by scaling up while preventing scheduling in a disposable namespace, or temporarily use an alert expression that matches the metric state you observe.

Restore:

```bash
kubectl scale deployment/sample-app -n observability-demo --replicas=2
```

## Investigate

1. Does the PrometheusRule appear in the loaded rules page?
2. Does the expression return a series?
3. Does the alert move from inactive to pending to firing?
4. Does Alertmanager receive it?
5. Does the route match a configured receiver?
6. Is the notification delivered?

A firing alert does not guarantee a notification: route matching, silences, inhibition, and receiver delivery all matter.

## Cleanup

```bash
kubectl delete -f ../manifests/prometheus-rule.yaml
kubectl delete -f ../manifests/sample-app.yaml
kubectl delete -f ../manifests/namespace.yaml
```
