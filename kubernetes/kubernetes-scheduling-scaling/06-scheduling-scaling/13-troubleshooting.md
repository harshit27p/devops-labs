# 13 — Scheduling and Scaling Troubleshooting

## Pod Pending
```bash
kubectl describe pod <pod>
kubectl get events -A --sort-by=.lastTimestamp
kubectl get nodes
kubectl describe node <node>
```
Common causes:
- Insufficient CPU/memory requests.
- Untolerated taint.
- Node selector/affinity mismatch.
- Pod anti-affinity or topology spread cannot be satisfied.
- PVC/volume topology constraints.
- Pod quota or admission rejection.
- No suitable node architecture or runtime.

## Insufficient resources
Compare requests, allocatable capacity, and existing requested resources—not only live utilization:
```bash
kubectl describe node <node>
kubectl top nodes
kubectl get pods -A -o wide
```

## HPA shows unknown metrics
Check Metrics Server/APIService, Pod resource requests, target selector, and metric adapter for custom metrics:
```bash
kubectl get hpa
kubectl describe hpa <name>
kubectl get apiservices
kubectl top pods
```

## HPA does not scale
Check metric availability, target reference, min/max replicas, stabilization/behavior settings, and whether current metric exceeds target. Verify the controller can update the scale subresource.

## Cluster does not scale up
Check unschedulable Pod events, autoscaler logs, node group min/max, cloud quotas, instance availability, and whether any node group can satisfy Pod constraints.

## Common anti-patterns
- Setting CPU requests to zero/omitting them for HPA CPU utilization.
- Using impossible hard affinity rules.
- Tolerating every taint.
- Setting all workloads to highest priority.
- Scaling replicas without checking database/queue capacity.
