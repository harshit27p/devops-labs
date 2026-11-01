# Lab 04 — Snapshot and Restore (Optional)

Requires snapshot CRDs, external snapshot controller, compatible CSI driver, and a real VolumeSnapshotClass.

```bash
kubectl api-resources | grep -i volumesnapshot
kubectl get volumesnapshotclass
kubectl get pvc
```
Edit `manifests/volumesnapshot-optional.yaml` to use the actual class, then apply and inspect:
```bash
kubectl apply -f manifests/volumesnapshot-optional.yaml
kubectl get volumesnapshot
kubectl describe volumesnapshot app-data-snapshot
```
Restore a new PVC using `dataSource` pointing to the VolumeSnapshot, then mount and validate data. Do not treat snapshots as a complete backup until consistency, retention, isolation, and restore testing are covered.
