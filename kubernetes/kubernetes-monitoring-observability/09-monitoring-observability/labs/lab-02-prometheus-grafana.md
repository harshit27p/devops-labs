# Lab 02 — Deploy Prometheus and Grafana

## Objective

Install a lab monitoring stack using the community `kube-prometheus-stack` Helm chart and inspect the resulting components.

## Prerequisites

- Helm 3 and `kubectl`.
- A disposable cluster with enough memory and storage.
- Permission to create a namespace, CRDs, and cluster-scoped resources.

## Install

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm search repo prometheus-community/kube-prometheus-stack
helm show values prometheus-community/kube-prometheus-stack > values-upstream-reference.yaml

# Review chart version and values before installing.
helm upgrade --install monitoring prometheus-community/kube-prometheus-stack   --namespace monitoring --create-namespace
```

For a repeatable installation, pin a reviewed chart version and commit your own minimal values file. The command above intentionally omits a version so the learner can inspect and select a compatible release.

## Inspect

```bash
kubectl get pods,svc -n monitoring
kubectl get crd | grep monitoring.coreos.com
kubectl get prometheus,alertmanager -n monitoring
```

Discover the Grafana Service:

```bash
kubectl get svc -n monitoring | grep -i grafana
```

Use port-forwarding rather than exposing Grafana publicly:

```bash
kubectl port-forward -n monitoring svc/<grafana-service-name> 3000:80
```

Open `http://localhost:3000` and obtain credentials using the chart's documented Secret name/key for the installed release. Do not paste credentials into Git or screenshots.

## Explore

- Open Prometheus and inspect Status → Targets.
- Query `up`.
- Explore node and Pod dashboards.
- Compare `kubectl top pods` with Prometheus time-series data.

## Cleanup

```bash
helm uninstall monitoring -n monitoring
# Remove the namespace only after reviewing retained data and resources.
```

CRDs may remain after uninstall. Do not delete shared CRDs in a cluster used by other monitoring releases.
