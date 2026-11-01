# 01 — Storage Fundamentals

A container's writable layer is tied to the container lifecycle. Replacing a container can discard data written only there. Kubernetes volumes provide mounted storage; persistent volumes provide storage whose lifecycle can outlast a Pod.

| Storage | Typical use | Lifecycle |
|---|---|---|
| Container writable layer | Scratch data | Container |
| `emptyDir` | Pod-local cache/shared scratch | Pod |
| ConfigMap/Secret volume | Configuration and credentials | API object/projection |
| `hostPath` | Narrow node integration | Node |
| PVC-backed volume | Durable application data | PV/backend policy |

## Design questions
- Must data survive container restart, Pod replacement, node loss, zone loss, or cluster loss?
- Does each replica need its own disk, or is shared storage required?
- What are capacity, latency, throughput, IOPS, durability, and availability requirements?
- How will encryption, backup, restore, monitoring, and deletion be handled?

## Persistence is not backup
A PVC may survive Pod deletion but can still be lost through backend failure, accidental deletion, corruption, or malicious activity. Backups must cover the failure domains that matter.

```mermaid
flowchart LR
 A[Application] --> B[Container mount] --> C[Pod volume] --> D[PVC] --> E[PV] --> F[Storage backend]
```

```bash
kubectl get pv
kubectl get pvc -A
kubectl get storageclass
kubectl describe pvc -n <namespace> <claim>
```
