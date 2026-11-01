# Lab 01 — Pre-upgrade Health Assessment

## Objective

Create a repeatable pre-upgrade inventory and identify blockers before changing a cluster.

## Commands

```bash
kubectl version
kubectl get nodes -o wide
kubectl get pods -A
kubectl get pdb -A
kubectl get pvc -A
kubectl get storageclass
kubectl get crd
kubectl get events -A --sort-by=.lastTimestamp
```

Record:
- Kubernetes and node versions;
- unhealthy Pods and nodes;
- PDBs with zero allowed disruptions;
- PVCs not Bound;
- installed CRDs and operators;
- CNI, CSI, DNS, ingress/gateway, metrics, and policy add-on versions.

## Research task

Choose your cluster distribution and target version. Read its upgrade guide and build a compatibility matrix for add-ons. Check API deprecations in manifests and Helm charts.

## Exit criteria

Do not proceed until critical workloads are healthy, backup/recovery is understood, capacity supports node rotation, and add-on compatibility is confirmed.
