# Kubernetes Workloads & Applications

Advanced, practical notes for deploying, operating, scaling, and troubleshooting application workloads on Kubernetes.

> **Prerequisite:** Complete [Architecture & Fundamentals](../00-architecture-fundamentals/README.md). This module focuses on workload APIs and application lifecycle, not cluster internals.

## Learning outcomes

- Choose the right workload controller for stateless, stateful, node-level, and batch workloads.
- Understand Pod lifecycle, templates, restart behavior, probes, and graceful shutdown.
- Deploy and safely update applications using Deployments and ReplicaSets.
- Operate StatefulSets, DaemonSets, Jobs, and CronJobs.
- Diagnose scheduling, image, startup, health-check, rollout, and batch execution failures.

## Module map

| File | Coverage |
|---|---|
| [01 Pods](01-pods.md) | Pod model, multi-container patterns, init and sidecar containers |
| [02 ReplicaSets](02-replicasets.md) | Desired replicas, selectors, ownership |
| [03 Deployments](03-deployments.md) | Rollouts, scaling, rollback, strategies |
| [04 StatefulSets](04-statefulsets.md) | Stable identity, ordered lifecycle, storage |
| [05 DaemonSets](05-daemonsets.md) | Node-local agents and placement |
| [06 Jobs](06-jobs.md) | One-off and parallel batch work |
| [07 CronJobs](07-cronjobs.md) | Scheduled batch work and concurrency |
| [08 Probes](08-health-probes.md) | Startup, readiness, liveness |
| [09 Container lifecycle](09-container-lifecycle.md) | Restart policies, hooks, termination |
| [10 Workload selection](10-workload-selection.md) | Decision guide and production patterns |

## Hands-on labs

1. [Deploy and operate a stateless application](labs/01-deployment-rollout-lab.md)
2. [Run batch workloads with Job and CronJob](labs/02-batch-workloads-lab.md)
3. [Inspect Pod health and troubleshoot failures](labs/03-pod-health-troubleshooting-lab.md)

## Manifests

- `manifests/deployment-nginx.yaml`
- `manifests/statefulset-web.yaml`
- `manifests/daemonset-node-agent.yaml`
- `manifests/job-batch.yaml`
- `manifests/cronjob-report.yaml`
- `manifests/pod-probes.yaml`

## Quick start

```bash
kubectl config current-context
kubectl get nodes -o wide
kubectl create namespace workloads-lab
kubectl apply -n workloads-lab -f manifests/deployment-nginx.yaml
kubectl get deploy,rs,pods -n workloads-lab -o wide
kubectl rollout status deployment/nginx-web -n workloads-lab
```

Run labs only in a disposable or explicitly approved cluster. Review image sources, resource settings, permissions, and namespace before applying manifests.

## Key distinction

A Pod is the execution unit; a workload controller manages Pods according to a higher-level purpose. Deployments are usually right for interchangeable stateless replicas; StatefulSets for stable identity and per-replica storage; DaemonSets for node-local agents; Jobs and CronJobs for finite tasks.

## References

- [Workloads overview](https://kubernetes.io/docs/concepts/workloads/)
- [Workload management](https://kubernetes.io/docs/concepts/workloads/controllers/)
- [Pods](https://kubernetes.io/docs/concepts/workloads/pods/)
- [Pod lifecycle](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/)
