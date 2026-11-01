# 02 — Volumes and Volume Sources

Volumes are declared under `spec.volumes` and mounted using `volumeMounts`. Containers in one Pod can share a volume.

## `emptyDir`
Created when the Pod is assigned to a node and removed when the Pod is removed from that node. Useful for scratch data and sharing files between containers. `medium: Memory` uses tmpfs and consumes memory.

## `hostPath`
Mounts a node filesystem path. It couples workloads to a node and may expose host files. Avoid it for ordinary application persistence; prefer CSI-backed PVCs.

## Projected volumes
ConfigMaps, Secrets, Downward API values, and service-account tokens can be projected as files. They are configuration/identity inputs, not general mutable application data.

## CSI volumes
CSI drivers integrate storage systems through a standard interface. Persistent CSI storage is commonly requested through a StorageClass and PVC.

## Mount controls
- `mountPath`: path inside container.
- `readOnly`: read-only mount.
- `subPath`: mounts a subdirectory/file; projected ConfigMap/Secret updates do not propagate normally through `subPath`.
- `subPathExpr`: environment-variable expansion in subpath.

See `manifests/emptydir-shared.yaml`. Inspect actual mounts with `kubectl describe pod <pod>`, `kubectl exec <pod> -- df -h`, and `kubectl exec <pod> -- mount`.
