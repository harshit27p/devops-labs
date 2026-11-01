# 08 — Stateful Applications and Per-Pod Storage

StatefulSets provide stable identity and can create one PVC per replica through `volumeClaimTemplates`. For StatefulSet identity, ordering, and rollout semantics, see Module 01; this guide focuses on storage.

The manifest `manifests/statefulset-with-pvc.yaml` creates separate claims such as `data/stateful-demo-0` and `data/stateful-demo-1`.

## Design considerations
- Each replica generally owns its own data volume; database replicas should not casually share one writable data directory.
- Storage topology may constrain where a Pod can run.
- Application replication is not the same as storage replication.
- A StatefulSet does not automatically make a database highly available.
- Understand PVC retention on scale-down and StatefulSet deletion.
- Plan WAL/binlog/journal handling, point-in-time recovery, and consistency.

Verify:
```bash
kubectl get sts
kubectl get pods -l app=stateful-demo -o wide
kubectl get pvc
kubectl describe pod stateful-demo-0
```
