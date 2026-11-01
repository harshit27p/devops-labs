# Lab 01 — Inspect Kubernetes Resource Metrics

## Objective

Understand the Metrics API and distinguish recent resource metrics from historical Prometheus monitoring.

## Prerequisites

A disposable or learning cluster, `kubectl`, and Metrics Server installed. Installation is cluster-specific; use the official Metrics Server instructions for your environment.

## Steps

```bash
kubectl get apiservice v1beta1.metrics.k8s.io
kubectl describe apiservice v1beta1.metrics.k8s.io
kubectl top nodes
kubectl top pods -A
kubectl top pods -n kube-system --containers
```

Inspect the raw API:

```bash
kubectl get --raw /apis/metrics.k8s.io/v1beta1/nodes
kubectl get --raw /apis/metrics.k8s.io/v1beta1/pods
```

## Questions

1. Which node is using the most memory?
2. Which Pods consume the most CPU?
3. Why do these commands not provide a long-term historical graph?
4. Which component supplies the Metrics API?

## Troubleshooting

If the APIService is unavailable, inspect Metrics Server Pod logs and events, kubelet connectivity, certificates, and network policy. Do not treat a missing Metrics API as a Prometheus failure.

## Cleanup

No resources are created by this lab.
