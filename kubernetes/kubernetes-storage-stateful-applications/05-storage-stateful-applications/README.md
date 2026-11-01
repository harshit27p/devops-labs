# Kubernetes Storage & Stateful Applications

Advanced module covering persistent volumes, claims, StorageClasses, CSI, StatefulSet storage, snapshots, recovery, security, and troubleshooting.

## Learning path
1. [Storage fundamentals](01-storage-fundamentals.md)
2. [Volumes and volume sources](02-volumes-and-volume-sources.md)
3. [PV and PVC lifecycle](03-pv-pvc-lifecycle.md)
4. [StorageClasses and dynamic provisioning](04-storageclasses-dynamic-provisioning.md)
5. [Access modes and volume modes](05-access-modes-volume-modes.md)
6. [Reclaim policy and data lifecycle](06-reclaim-policy-data-lifecycle.md)
7. [CSI architecture and drivers](07-csi-architecture-drivers.md)
8. [Stateful applications](08-stateful-applications.md)
9. [Expansion, topology, snapshots and clones](09-expansion-topology-snapshots-clones.md)
10. [Backup, restore and disaster recovery](10-backup-restore-disaster-recovery.md)
11. [Storage security and permissions](11-storage-security-permissions.md)
12. [Storage troubleshooting](12-storage-troubleshooting.md)
13. [Production storage patterns](13-production-storage-patterns.md)
14. [Interview questions](14-interview-questions.md)

## Labs
- [01 — Inspect storage capabilities](labs/01-inspect-storage.md)
- [02 — Create and use a PVC](labs/02-pv-pvc-dynamic-provisioning.md)
- [03 — StatefulSet per-Pod storage](labs/03-statefulset-per-pod-storage.md)
- [04 — Snapshot and restore (optional)](labs/04-snapshot-restore.md)

## Manifests and diagrams
See `manifests/` and `diagrams/`. Some examples require a working default StorageClass; snapshot examples require snapshot CRDs, controller, a compatible CSI driver, and a real VolumeSnapshotClass.

## Prerequisites
A working Kubernetes cluster and `kubectl`. Inspect available storage rather than assuming a default class exists. For StatefulSet identity and update semantics, see [Module 01 — StatefulSets](../01-workloads-applications/04-statefulsets.md).

## Safety
A Bound PVC is not proof of backup, mount health, or durability against every failure. Check reclaim policy before deleting claims. Never commit real credentials or use production data in these labs. `hostPath` is node-local and should not be treated as general-purpose persistent storage.

## Official references
- https://kubernetes.io/docs/concepts/storage/
- https://kubernetes.io/docs/concepts/storage/volumes/
- https://kubernetes.io/docs/concepts/storage/persistent-volumes/
- https://kubernetes.io/docs/concepts/storage/storage-classes/
- https://kubernetes-csi.github.io/docs/
- https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/
- https://kubernetes.io/docs/concepts/storage/volume-snapshots/
