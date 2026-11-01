# 10 — Backup, Restore, and Disaster Recovery

Define RPO (acceptable data loss) and RTO (acceptable recovery time). Plan for node, zone, cluster, region, account, corruption, and malicious-deletion failures.

## Mechanisms
- Database-native logical/physical backups.
- CSI snapshots for fast point-in-time copies where supported.
- Kubernetes-aware backup platforms for resources and persistent data.
- Backend replication for availability (replication alone is not backup).

## Recovery workflow
1. Declare incident and choose a known-good recovery point.
2. Provision a clean environment and required CSI driver.
3. Restore Kubernetes resources and data in dependency order.
4. Validate database recovery, schema, application health, and integrity.
5. Reconnect traffic only after verification.
6. Record actual RPO/RTO and lessons learned.

Anti-patterns: treating a snapshot as a full application backup; storing all backups in the production failure domain; never testing restores; snapshotting active databases without a consistency strategy; assuming replication protects against logical corruption or ransomware.

Write a runbook with owner, dependencies, backup location, restore commands, validation queries, traffic cutover, rollback, and communication plan.
