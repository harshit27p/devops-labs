# 03 — Node Maintenance and Disruption Management

## Cordon, drain, and uncordon

- `cordon` marks a node unschedulable for new Pods.
- `drain` evicts eligible Pods so workloads can be recreated elsewhere.
- `uncordon` allows new scheduling again.

Example workflow (only on a lab or approved maintenance window):

```bash
kubectl get nodes
kubectl cordon <node-name>
kubectl drain <node-name> --ignore-daemonsets
# Perform provider-approved maintenance and validate node health.
kubectl uncordon <node-name>
kubectl get pods -A -o wide
```

Do not add `--delete-emptydir-data` or `--force` reflexively. Understand exactly which data or unmanaged Pods could be lost. DaemonSet Pods are not evicted by a normal drain.

## PodDisruptionBudget

A PDB limits voluntary disruptions for selected Pods. It does not protect against every involuntary failure, and it does not guarantee availability if the application has insufficient replicas or all replicas share one failure domain.

See `../manifests/pod-disruption-budget.yaml`.

## Maintenance checklist

- Verify spare capacity and autoscaler behavior.
- Inspect PDBs and workload replica counts.
- Check local ephemeral data and local PV constraints.
- Check StatefulSet and storage topology constraints.
- Confirm critical services have healthy replicas elsewhere.
- Drain one node or a small batch at a time.
- Verify workloads recover before proceeding.
- Record maintenance and validation evidence.

## Common drain blockers

PDB constraints, unmanaged Pods, local storage, finalizers, insufficient cluster capacity, and stuck termination. Diagnose each cause; do not bypass protections without a reviewed exception.

## Further reading

- https://kubernetes.io/docs/tasks/administer-cluster/safely-drain-node/
- https://kubernetes.io/docs/concepts/workloads/pods/disruptions/
