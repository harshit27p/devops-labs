# 04 — Backup, Restore, and Disaster Recovery

## What must be protected?

A recovery plan may need:
- application data in persistent volumes and external databases;
- Kubernetes API objects and configuration;
- secrets and encryption keys;
- cluster bootstrap and infrastructure definitions;
- container images and package/chart artifacts;
- DNS, certificates, identity, and external service configuration.

A manifest export is not a complete application backup. Persistent data, external dependencies, encryption keys, and recovery ordering matter.

## Backup strategies

- Volume snapshots through CSI where supported.
- Application-consistent database dumps or native database backup.
- Kubernetes object backup tools such as Velero, configured for the environment.
- Infrastructure-as-code and GitOps repositories.
- Off-site or cross-region copies with access controls and retention.

A crash-consistent volume snapshot may not be application-consistent. Coordinate quiescing, database-native backups, or application hooks as appropriate.

## RPO and RTO

- **RPO:** maximum acceptable data loss measured in time.
- **RTO:** maximum acceptable time to restore service.

Define these with service owners. A backup schedule alone does not establish either objective.

## Restore testing

1. Select an isolated recovery environment.
2. Retrieve backup and encryption material.
3. Restore infrastructure prerequisites.
4. Restore data and Kubernetes resources in dependency order.
5. Validate data integrity and application behavior.
6. Restore DNS/traffic only after verification.
7. Measure actual RPO/RTO and document gaps.

## Velero example (conceptual)

Velero installation and storage plugin configuration vary by cloud and storage backend. After a supported installation, a namespace backup may resemble:

```bash
velero backup create payments-prechange   --include-namespaces payments   --wait

velero backup describe payments-prechange
velero backup logs payments-prechange
```

Restore into a controlled test environment only after reviewing the backup and target namespace mapping:

```bash
velero restore create payments-restore-test   --from-backup payments-prechange   --wait
```

Do not assume PV data is included unless the backup configuration and CSI/data-mover integration explicitly support it.

## Disaster-recovery patterns

- Same-region restore for localized cluster failure.
- Cross-zone recovery for zone failure.
- Cross-region recovery for regional outage.
- Active/passive or active/active application architecture where justified.

## Further reading

- https://velero.io/docs/
- https://kubernetes.io/docs/concepts/storage/volume-snapshots/
