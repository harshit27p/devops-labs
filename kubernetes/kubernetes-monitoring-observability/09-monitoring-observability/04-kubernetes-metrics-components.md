# 04 — Kubernetes Metrics Components

Kubernetes monitoring uses several distinct metric sources. They solve different problems and should not be treated as interchangeable.

## Metrics Server

Metrics Server collects resource usage from kubelets and exposes a lightweight Metrics API used by `kubectl top` and resource metrics consumers such as the HorizontalPodAutoscaler.

```bash
kubectl top nodes
kubectl top pods -A
kubectl get apiservice v1beta1.metrics.k8s.io
kubectl describe apiservice v1beta1.metrics.k8s.io
```

Metrics Server is not a general historical monitoring database. It does not replace Prometheus.

## kube-state-metrics

kube-state-metrics watches Kubernetes API objects and exposes their **observed state** as metrics: Deployment desired/available replicas, Pod phase, Job state, PVC status, and many more.

It does not measure actual CPU or memory consumption. It reports Kubernetes object state, not resource usage.

## node-exporter

Prometheus node-exporter exposes host-level operating-system and hardware metrics such as CPU, memory, filesystem, and network statistics. In Kubernetes it is commonly deployed as a DaemonSet so each node is covered.

Treat host metrics as sensitive operational data. Restrict access and ensure filesystem mount handling is correct for your environment.

## Kubelet and cAdvisor metrics

Kubelet exposes node and container-related metrics, including cAdvisor-derived container resource statistics depending on Kubernetes version and configuration. Metric names and availability can change; verify against the running version.

## Comparison

| Component | Primary data | Typical consumer |
|---|---|---|
| Metrics Server | Recent Pod/node CPU and memory | `kubectl top`, HPA resource metrics |
| kube-state-metrics | Kubernetes API object state | Prometheus |
| node-exporter | Host OS/hardware metrics | Prometheus |
| kubelet/cAdvisor | Kubelet and container runtime metrics | Prometheus |
| Application `/metrics` | Business and service metrics | Prometheus |

## Troubleshooting checks

```bash
kubectl get pods -A | grep -i metrics
kubectl top nodes
kubectl top pods -A
kubectl get --raw /apis/metrics.k8s.io/v1beta1/nodes
kubectl get endpoints -A
```

If `kubectl top` fails, check Metrics Server installation, APIService condition, kubelet reachability, TLS configuration, and network paths. If Prometheus has no kube-state-metrics or node-exporter data, check Service/Endpoint discovery, scrape target status, RBAC, and selectors.

## Further reading

- https://github.com/kubernetes-sigs/metrics-server
- https://github.com/kubernetes/kube-state-metrics
- https://github.com/prometheus/node_exporter
