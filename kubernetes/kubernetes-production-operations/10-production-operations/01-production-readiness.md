# 01 — Production Readiness Checklist

Production readiness is a set of verifiable operational controls, not simply a cluster that reports `Ready`.

## Cluster foundation

- Choose a supported Kubernetes distribution and version.
- Define control-plane and worker-node failure domains.
- Size nodes for workload requests plus system and operational headroom.
- Configure API endpoint availability, authentication, authorization, and audit logging.
- Define CNI, DNS, ingress/gateway, storage, and load-balancer dependencies.
- Document ownership, support boundaries, and escalation paths.

## Workload readiness

- Set CPU and memory requests; set limits intentionally.
- Configure startup, readiness, and liveness probes for actual application behavior.
- Use multiple replicas for services that require availability.
- Spread replicas across nodes/zones where possible.
- Add PodDisruptionBudgets for critical replicated workloads.
- Define graceful shutdown and termination handling.
- Use immutable image tags or digests and a controlled image supply chain.
- Keep configuration and secrets separate from container images.

## Security readiness

- Apply least-privilege RBAC.
- Use dedicated ServiceAccounts and disable token automount when not needed.
- Enforce Pod Security Standards or an equivalent admission policy.
- Apply network segmentation and egress controls.
- Scan images and manage patching.
- Encrypt secrets at rest and use an external secret manager where appropriate.
- Restrict administrative access and audit privileged operations.

## Operations readiness

- Dashboards, actionable alerts, and runbooks exist.
- Backups are automated and restore tests are recorded.
- Upgrade and node replacement procedures are tested.
- Capacity, quotas, and cost ownership are visible.
- Release and rollback procedures are documented.
- Incident contacts and communication channels are defined.

## Evidence

A checklist item should have evidence: a policy, test result, dashboard, runbook, or recorded drill. “Configured” is weaker than “tested and verified.”

## Cross references

- Workload probes and lifecycle: Module 01.
- Network policy and access: Modules 02 and 07.
- Storage and snapshots: Module 05.
- Scheduling and disruption: Module 06.
- Helm releases: Module 08.
- Monitoring and alerting: Module 09.
