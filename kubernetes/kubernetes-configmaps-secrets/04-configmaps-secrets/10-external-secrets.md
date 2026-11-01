# 10 — External Secret Management

## Why externalize secret lifecycle?

Organizations may already use a centralized secret manager for access control, audit, rotation, and dynamic credentials. Kubernetes workloads can integrate with these systems rather than storing long-lived credentials manually in manifests.

## Common integration patterns

### External Secrets Operator

An operator reads from an external provider and synchronizes selected values into Kubernetes Secret objects. The application consumes the resulting Secret using standard Kubernetes mechanisms.

Consider:
- Provider authentication and workload identity.
- Namespace and Secret target permissions.
- Refresh interval and rotation behavior.
- What happens when the provider is unavailable.
- Whether synchronized values remain in etcd and backups.

### Secrets Store CSI Driver

A CSI driver can mount secrets from an external provider into a Pod filesystem. Depending on provider and configuration, synchronization into a Kubernetes Secret may also be possible.

Consider:
- Node plugin and provider installation.
- Secret rotation support and application reload.
- Pod restart behavior.
- Provider identity and access policy.
- File permissions and mount lifecycle.

### Direct application retrieval

An application can retrieve credentials directly from a secret manager using workload identity. This avoids copying credentials into Kubernetes Secret objects, but adds application integration, network, identity, and retry requirements.

## Workload identity

Prefer cloud workload identity or short-lived federated credentials over static cloud access keys stored in a Pod. Bind the workload identity to a narrowly scoped provider role.

## Design checklist

- [ ] Choose one approved source of truth.
- [ ] Use workload identity where supported.
- [ ] Define refresh and rotation semantics.
- [ ] Restrict provider access by workload and environment.
- [ ] Decide whether values are materialized as Kubernetes Secrets.
- [ ] Protect logs, audit trails, and backups.
- [ ] Test provider outage and credential revocation.
- [ ] Document emergency rotation and recovery.

## References

- [External Secrets Operator](https://external-secrets.io/)
- [Secrets Store CSI Driver](https://secrets-store-csi-driver.sigs.k8s.io/)
- [Kubernetes Secret good practices](https://kubernetes.io/docs/concepts/security/secrets-good-practices/)
