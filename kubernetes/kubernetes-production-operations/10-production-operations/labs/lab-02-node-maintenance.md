# Lab 02 — Drain and Safely Maintain a Node

## Warning

Use a disposable multi-node cluster. Draining a single-node cluster may evict workloads with nowhere to reschedule.

## Inspect

```bash
kubectl get nodes
kubectl get pods -A -o wide
kubectl get pdb -A
```

Select a worker node and identify its workloads, DaemonSets, local storage, and PDB constraints.

## Maintenance workflow

```bash
kubectl cordon <worker-node>
kubectl drain <worker-node> --ignore-daemonsets
```

If drain is blocked, inspect the reported Pod and PDB. Do not bypass PDBs or delete Pods until you understand the availability and data impact.

After simulated maintenance:

```bash
kubectl get nodes
kubectl uncordon <worker-node>
kubectl get pods -A -o wide
```

## Validate

Confirm workloads are Ready, Services have endpoints, and no critical alerts remain. Record drain duration and any blocked eviction.
