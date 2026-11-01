# 13 — Production Troubleshooting Playbook

## Cluster-wide symptoms

```bash
kubectl get nodes
kubectl get pods -A
kubectl get events -A --sort-by=.lastTimestamp
kubectl get componentstatuses  # Deprecated/removed in modern Kubernetes; do not rely on it.
```

Use distribution-specific control-plane health checks rather than relying on deprecated component status APIs.

## Pods remain Pending

Inspect `kubectl describe pod`. Look for insufficient CPU/memory, taints, node selectors, affinity, topology constraints, PVC binding, quota, and admission rejection.

## Pods repeatedly restart

Inspect previous logs, termination reason, events, probes, OOMKilled status, and dependency health:

```bash
kubectl logs <pod> -n <namespace> --previous
kubectl describe pod <pod> -n <namespace>
```

## Node NotReady

Check provider/node health, kubelet, runtime, disk and memory pressure, CNI, certificates, and network reachability. Follow the distribution's node recovery process.

## Service unreachable

Verify Service selectors, EndpointSlices, Pod readiness, port/targetPort, DNS, NetworkPolicy, ingress/gateway configuration, and external load balancer health. See Modules 02 and 03.

## PVC not bound or mount fails

Inspect PVC, PV, StorageClass, CSI controller/node Pods, events, topology, access modes, and storage backend health. Do not delete claims as a diagnostic shortcut. See Module 05.

## Rollout stuck

Inspect Deployment conditions, ReplicaSets, Pods, image pulls, admission failures, readiness probes, quotas, and PDB interactions. Use rollout history and release records before rollback.

## Incident hygiene

Record what was changed and why. Prefer narrow, reversible actions. Verify the user journey after mitigation. Do not run broad delete, drain, or policy commands copied from the internet without understanding their impact.
