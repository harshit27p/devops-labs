# Lab 01 — Inspect Scheduler and Resources

```bash
kubectl get nodes -o wide
kubectl describe nodes
kubectl get pods -A -o wide
kubectl get events -A --sort-by=.lastTimestamp
kubectl top nodes
kubectl top pods -A
```
`kubectl top` requires Metrics API availability. Compare node Allocatable and requested resources; do not infer scheduling capacity from instantaneous CPU usage alone.

Record node labels, taints, allocatable CPU/memory, current Pod placement, and any scheduling warnings.
