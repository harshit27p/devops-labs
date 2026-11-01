# 10 — Kubernetes Production Operations

A practical guide to operating Kubernetes reliably beyond initial deployment.

## Learning outcomes

- Establish production-readiness standards for clusters and workloads.
- Plan Kubernetes version upgrades and node maintenance.
- Design backup, restore, and disaster-recovery procedures.
- Operate GitOps-based delivery and controlled rollouts.
- Manage capacity, quotas, reliability, and cost.
- Handle incidents with evidence-driven runbooks.
- Plan multi-cluster, availability-zone, and regional architectures.
- Validate recovery, security, and operational readiness.

## Topic guides

| Guide | Topic |
|---|---|
| [01](01-production-readiness.md) | Production readiness checklist |
| [02](02-cluster-lifecycle-upgrades.md) | Cluster lifecycle and upgrades |
| [03](03-node-maintenance.md) | Node maintenance and disruption management |
| [04](04-backup-restore-disaster-recovery.md) | Backup, restore, and disaster recovery |
| [05](05-gitops-operations.md) | GitOps and release operations |
| [06](06-rollouts-and-release-safety.md) | Safe releases, rollback, and progressive delivery |
| [07](07-capacity-and-cost-management.md) | Capacity, quotas, and cost management |
| [08](08-reliability-and-ha.md) | High availability and reliability engineering |
| [09](09-multi-cluster-operations.md) | Multi-cluster and regional operations |
| [10](10-incident-response-runbooks.md) | Incident response and runbooks |
| [11](11-platform-governance.md) | Platform governance and operational guardrails |
| [12](12-production-validation.md) | Production validation and game days |
| [13](13-troubleshooting.md) | Production troubleshooting |
| [14](14-interview-questions.md) | Interview questions and scenarios |

## Labs

1. [Lab 01 — Pre-upgrade health assessment](labs/lab-01-pre-upgrade-assessment.md)
2. [Lab 02 — Drain and safely maintain a node](labs/lab-02-node-maintenance.md)
3. [Lab 03 — Backup and restore an application namespace](labs/lab-03-backup-restore.md)
4. [Lab 04 — Release validation and rollback drill](labs/lab-04-release-rollback.md)

## Example manifests

- `manifests/resource-quota.yaml`
- `manifests/limit-range.yaml`
- `manifests/pod-disruption-budget.yaml`
- `manifests/network-policy-baseline.yaml`

## Prerequisites

This module assumes familiarity with Kubernetes architecture, Deployments, Services, storage, scheduling, RBAC, Helm, and observability. Review Modules 00–09 as needed.

## Important operational warning

These guides are educational templates, not a substitute for your cloud provider's or Kubernetes distribution's runbooks. Cluster upgrades, node drains, backups, restores, and network-policy changes can cause outages or data loss. Practice on disposable environments, confirm backups, and obtain change approval before production operations.

## Suggested sequence

Start with readiness and lifecycle planning. Practice node maintenance and application recovery in a disposable cluster. Then implement release safety, capacity controls, incident response, and governance. Finish by running a simulated failure and reviewing the evidence.
