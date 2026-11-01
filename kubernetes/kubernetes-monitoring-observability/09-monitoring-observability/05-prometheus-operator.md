# 05 — Prometheus Operator and kube-prometheus-stack

## Why an Operator?

The Prometheus Operator uses Kubernetes custom resources to manage Prometheus, Alertmanager, and related configuration. It turns monitoring configuration into declarative Kubernetes objects.

Common resources include:

- `Prometheus`: desired Prometheus deployment and selectors.
- `Alertmanager`: desired Alertmanager deployment.
- `ServiceMonitor`: describes Services and endpoints to scrape.
- `PodMonitor`: describes Pods to scrape directly.
- `PrometheusRule`: recording and alerting rules.
- `Probe`: black-box probing configuration where supported.

The exact APIs and behavior depend on the installed Operator version. Inspect CRDs rather than assuming a version.

## kube-prometheus-stack

The community Helm chart commonly bundles Prometheus Operator, Prometheus, Alertmanager, Grafana, node-exporter, and kube-state-metrics. It is a convenient lab starting point, not a universal production sizing profile.

Example installation:

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm search repo prometheus-community/kube-prometheus-stack
helm show values prometheus-community/kube-prometheus-stack
helm install monitoring prometheus-community/kube-prometheus-stack   --namespace monitoring --create-namespace
```

For repeatable environments, pin a chart version and maintain a reviewed values file:

```bash
helm upgrade --install monitoring prometheus-community/kube-prometheus-stack   --namespace monitoring --create-namespace   --version <REVIEWED_CHART_VERSION>   -f values-monitoring.yaml
```

Do not copy a random chart version into production. Check chart compatibility, image versions, Kubernetes version, CRD upgrade notes, and release notes.

## Inspect resources

```bash
kubectl get pods,svc -n monitoring
kubectl get crd | grep monitoring.coreos.com
kubectl get prometheus,alertmanager,servicemonitor,podmonitor,prometheusrule -A
kubectl describe prometheus -n monitoring
```

## CRD lifecycle

CRDs are cluster-scoped APIs. Helm chart upgrades may require special handling for CRDs, depending on chart design. Read the chart's upgrade documentation and back up important custom resources before changing versions.

## Operational checklist

- Pin chart and image versions.
- Configure persistent storage and retention.
- Set resource requests/limits.
- Configure selectors deliberately; overly restrictive selectors cause missing targets.
- Restrict UI access and configure authentication.
- Set alert routing and notification receivers.
- Monitor Prometheus ingestion, rule evaluation, and TSDB health.
- Back up configuration and document recovery procedures.

## Further reading

- https://prometheus-operator.dev/
- https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack
