# 06 — Reclaim Policy and Data Lifecycle

- `Retain`: released PV and backend data are retained for manual recovery.
- `Delete`: PV and backing storage are deleted through the provisioner workflow.
- `Recycle`: deprecated; do not use for new designs.

Reclaim policy is not a backup policy. StatefulSet PVC retention behavior is a separate control and must be considered alongside PV reclaim policy.

Before deleting:
```bash
kubectl get pvc -n <namespace>
kubectl get pv
kubectl get pv <pv> -o yaml
kubectl describe pv <pv>
kubectl get sts -n <namespace> <statefulset> -o yaml
```

Safe workflow: identify owner, verify backup/restore, record PV/backend identifiers, inspect reclaim and StatefulSet retention policies, obtain approval, delete in a controlled window, and verify backend state.

An administrator can patch a PV:
```bash
kubectl patch pv <pv-name> -p '{"spec":{"persistentVolumeReclaimPolicy":"Retain"}}'
```
This is not retroactive protection for data already deleted.
