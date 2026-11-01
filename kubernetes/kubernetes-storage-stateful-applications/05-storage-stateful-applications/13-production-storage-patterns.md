# 13 — Production Storage Patterns

## One claim per stateful replica
Use StatefulSet `volumeClaimTemplates` for distinct replica data volumes and application-level replication for HA.

## Shared files
Use RWX only when backend and application support concurrent multi-node access. Define locking, consistency, and failure semantics.

## Zonal block storage
Use topology-aware provisioning and scheduling. A zonal disk is not automatically portable across zones.

## Operations
Monitor provisioned/consumed capacity, filesystem and inode usage, latency, throughput, IOPS, queue depth, throttling, attach/mount failures, and CSI health.

Governance: approved StorageClasses, ownership labels, quotas, reclaim policy, RBAC, expansion/deletion/recovery runbooks.

## Readiness checklist
- [ ] CSI driver and version compatibility confirmed.
- [ ] Capacity, latency, durability, and topology requirements documented.
- [ ] Access modes validated.
- [ ] Encryption and least privilege enabled.
- [ ] Expansion tested.
- [ ] Backup and restore tested.
- [ ] Reclaim/deletion behavior understood.
- [ ] Monitoring and alerting configured.
- [ ] Failure/recovery runbooks maintained.
