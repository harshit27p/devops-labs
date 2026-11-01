# 02 — Cluster Lifecycle and Upgrades

## Lifecycle stages

A cluster lifecycle includes provisioning, configuration, upgrades, scaling, certificate rotation, node replacement, backup, and eventual decommissioning. Automate repeatable steps and keep the desired configuration version-controlled.

## Upgrade planning

Before upgrading:

1. Identify current and target Kubernetes versions.
2. Read release notes, deprecated API guidance, and distribution-specific upgrade documentation.
3. Check add-on compatibility: CNI, CSI, DNS, ingress/gateway, metrics, admission webhooks, and operators.
4. Scan manifests and Helm charts for removed APIs.
5. Review control-plane and node upgrade order.
6. Verify etcd or provider-managed control-plane backup/recovery options.
7. Confirm application replicas, PodDisruptionBudgets, and capacity allow node rotation.
8. Test the process in staging and define abort/rollback criteria.

## Version-skew awareness

Kubernetes components have supported version-skew rules. Do not independently upgrade kubelet, control plane, kubectl, or add-ons without checking the version-skew policy for the target release.

## Managed vs self-managed clusters

Managed services may operate the control plane and provide supported node upgrade workflows, but customers remain responsible for workload compatibility, add-ons, disruption planning, and application recovery. Self-managed clusters require explicit control-plane, etcd, certificate, and node lifecycle ownership.

## Safe upgrade pattern

- Upgrade a non-production environment first.
- Upgrade control plane using the provider/distribution procedure.
- Upgrade node pools in controlled batches.
- Cordon/drain nodes according to workload disruption policy.
- Validate DNS, networking, storage, ingress, autoscaling, and application health after each batch.
- Observe telemetry and stop if error budgets or health checks deteriorate.

## Commands for inspection

```bash
kubectl version
kubectl get nodes -o wide
kubectl get pods -A
kubectl get pdb -A
kubectl get events -A --sort-by=.lastTimestamp
```

These commands inspect state; they do not perform an upgrade. Use your provider's official upgrade mechanism.

## Decommissioning

Inventory workloads, persistent data, DNS, certificates, identities, secrets, external dependencies, and monitoring. Confirm data retention and backups before deleting infrastructure.
