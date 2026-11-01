# 04 — StatefulSets

## 1. When to use a StatefulSet

Use a StatefulSet when Pods need stable, predictable identities and/or stable per-replica storage. Examples include clustered databases, distributed brokers, and systems that depend on stable peer identities.

A StatefulSet does not make an application stateful by magic. The application must still implement replication, consistency, failover, and recovery correctly.

## 2. Key characteristics

- Stable ordinal identity: `app-0`, `app-1`, `app-2`.
- Stable network identity when paired with a headless Service.
- PersistentVolumeClaim templates can provide a dedicated claim for each Pod.
- Ordered creation and termination by default.
- Update behavior controlled by `updateStrategy`.

## 3. Example

See [`manifests/statefulset-web.yaml`](manifests/statefulset-web.yaml). It uses a headless Service and `volumeClaimTemplates`. StorageClass availability and dynamic provisioning are cluster-dependent.

```bash
kubectl apply -f manifests/statefulset-web.yaml
kubectl get statefulset,pods,pvc -n workloads-lab
kubectl describe statefulset web -n workloads-lab
```

## 4. Ordered lifecycle

With the default `OrderedReady` Pod management policy, Pods are created in ordinal order and the next Pod waits for the previous Pod to become Ready. Deletion is generally in reverse ordinal order. `Parallel` relaxes ordered creation/deletion where the application can tolerate it.

## 5. Storage and recovery

PVCs created from `volumeClaimTemplates` are associated with individual ordinals. Deleting a StatefulSet does not normally delete its associated PVCs automatically. Confirm retention policy and backup requirements before changing or deleting stateful resources.

A rescheduled Pod with the same ordinal can reattach its corresponding claim, subject to storage topology and volume attachment constraints.

## 6. Update strategy

- `RollingUpdate`: updates Pods in ordinal order, respecting readiness.
- `OnDelete`: only updates Pods after they are manually deleted.

Partitioned rolling updates can stage an update to only a subset of ordinals. Validate carefully; stateful rollouts can have application-specific quorum and compatibility constraints.

## 7. StatefulSet vs Deployment

| Requirement | Deployment | StatefulSet |
|---|---|---|
| Interchangeable replicas | Yes | Usually no |
| Stable ordinal name | No | Yes |
| Per-replica PVC identity | Not built-in | Yes |
| Typical use | Web/API tier | Databases, brokers |
| Scaling semantics | General replica count | Ordered identity-aware replicas |

## References

- [StatefulSets](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/)
- [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
