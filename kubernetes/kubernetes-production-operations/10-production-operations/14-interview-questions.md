# 14 — Kubernetes Production Operations Interview Questions

## Fundamentals

**1. What does production readiness mean?**  
A verifiable set of reliability, security, observability, capacity, recovery, and ownership controls.

**2. What is the difference between cordon and drain?**  
Cordon prevents new scheduling on a node; drain evicts eligible Pods so workloads can be rescheduled.

**3. What is a PodDisruptionBudget?**  
A policy that limits voluntary disruptions for selected Pods; it does not prevent all involuntary failures.

**4. Why is a successful rollout not proof of application health?**  
Kubernetes rollout conditions may pass while user-facing requests, dependencies, or business transactions fail.

## Upgrades and recovery

**5. How do you plan a Kubernetes upgrade?**  
Check version skew, deprecated APIs, add-on compatibility, backups, disruption capacity, staging validation, and rollback/abort criteria.

**6. What is RPO vs RTO?**  
RPO is the maximum acceptable data loss in time; RTO is the maximum acceptable recovery time.

**7. Is exporting YAML a complete backup?**  
No. It omits or fails to protect persistent data, external systems, encryption keys, and recovery dependencies.

**8. Why must restores be tested?**  
A backup is only useful if it can be restored with integrity within the required objectives.

## Releases and GitOps

**9. Explain GitOps.**  
A reconciliation model where version-controlled declarative state is continuously compared with and applied to the cluster.

**10. What is configuration drift?**  
A difference between intended declarative state and live state.

**11. Does `kubectl rollout undo` reverse a database migration?**  
No. Application rollback does not reverse external side effects or schema changes.

**12. What is canary deployment?**  
A controlled release that exposes a small portion of traffic to a new version before expanding based on health.

## Reliability and cost

**13. How do you make a workload highly available?**  
Use appropriate replicas, spread across failure domains, readiness and graceful shutdown, disruption budgets, resilient dependencies, and tested recovery.

**14. What is the difference between ResourceQuota and LimitRange?**  
ResourceQuota caps aggregate namespace consumption; LimitRange defines per-object defaults and bounds.

**15. Why can under-requesting CPU/memory be dangerous?**  
It can cause contention, throttling, OOM kills, and unreliable scheduling.

**16. Why are multiple clusters operationally expensive?**  
They add lifecycle, networking, identity, policy, observability, data replication, and consistency complexity.

## Scenarios

- A node drain is blocked by a PDB. How do you investigate safely?
- A cluster upgrade succeeds but CoreDNS fails. What is your validation sequence?
- A restore completes but the application cannot start. What dependencies do you check?
- GitOps repeatedly reverts a manual incident change. How should break-glass operations work?
- A canary has low traffic and noisy metrics. How do you avoid false release decisions?
- One region fails. Which application, data, DNS, and identity dependencies must be validated?
