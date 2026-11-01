# 11 — Storage Security and Permissions

Persistent data may contain sensitive business or customer information. Protect it during provisioning, transport, mounting, use, backup, and deletion.

## Controls
- Least-privilege RBAC for PV, PVC, StorageClass, snapshots, and related objects.
- Backend/KMS encryption at rest; protect keys separately.
- Encrypted transport where supported.
- Restrict privileged Pods and `hostPath` mounts.
- Apply quotas and admission policies.
- Protect snapshots/backups with access controls and retention.
- Use workload-specific filesystem identities.

Example Pod security context:
```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 10001
  runAsGroup: 10001
  fsGroup: 20001
  fsGroupChangePolicy: OnRootMismatch
```
`fsGroup` behavior depends on volume type and CSI driver. Read-only mounts should be used where possible. Avoid `chmod 777` as a permissions workaround.

A writable `hostPath` can expose node files. Kubernetes deletion does not guarantee physical secure erasure; follow provider sanitization, encryption-key destruction, and compliance processes.
