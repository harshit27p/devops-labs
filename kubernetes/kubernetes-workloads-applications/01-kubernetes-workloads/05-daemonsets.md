# 05 — DaemonSets

## Purpose

A DaemonSet ensures that a Pod runs on each eligible node, or on a selected subset of nodes. When eligible nodes are added, the DaemonSet controller creates Pods for them; when nodes are removed, associated Pods are garbage-collected.

## Common use cases

- Node-level log collection.
- Host metrics and monitoring agents.
- Storage or networking node plugins.
- Security and compliance agents.
- GPU or hardware-specific node services.

## Example

See [`manifests/daemonset-node-agent.yaml`](manifests/daemonset-node-agent.yaml). It is a simple illustrative node agent. Host access is deliberately not enabled; production agents may require carefully scoped host mounts and privileges.

## Placement controls

DaemonSet Pods can use node selectors, node affinity, and tolerations. Kubernetes automatically adds certain tolerations for DaemonSet Pods so node-level agents can be scheduled in situations where ordinary Pods may not be.

Do not assume every node will run a Pod: selectors, affinity, taints, architecture, OS, and resource availability all affect eligibility.

## Commands

```bash
kubectl get daemonsets -A
kubectl describe daemonset node-agent -n workloads-lab
kubectl get pods -n workloads-lab -o wide
kubectl rollout status daemonset/node-agent -n workloads-lab
```

## Operational cautions

DaemonSets can have broad node-level impact. Avoid privileged mode and hostPath mounts unless required. Restrict host paths, use read-only mounts where possible, apply least privilege, and test upgrades on a subset of nodes first.

## DaemonSet vs static Pod

Static Pods are managed directly by kubelet from local manifest files and are useful for bootstrapping control-plane components. DaemonSets are API-managed workloads and are preferable for ordinary node agents that need standard rollout and scheduling controls.

## Reference

- [DaemonSet](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/)
- [Static Pods](https://kubernetes.io/docs/concepts/workloads/pods/static-pods/)
