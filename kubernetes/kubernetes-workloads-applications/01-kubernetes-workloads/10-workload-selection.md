# 10 — Choosing the Right Workload API

## Decision guide

| Requirement | Recommended API | Reason |
|---|---|---|
| Stateless HTTP/API service | Deployment | Interchangeable replicas and controlled rollout |
| Stable identity and per-replica storage | StatefulSet | Ordinal identity and PVC association |
| One agent on each eligible node | DaemonSet | Node-scoped placement |
| Run a finite task to completion | Job | Completion and retry semantics |
| Run a task on a schedule | CronJob | Creates Jobs on a recurring schedule |
| Simple one-off diagnostic Pod | Pod | Direct Pod lifecycle is acceptable for temporary work |

## Application architecture examples

### Three-tier web application

- Frontend: Deployment.
- API: Deployment.
- Database: managed database service or an appropriately designed StatefulSet.
- Scheduled cleanup: CronJob.
- Node telemetry agent: DaemonSet.

### Data processing pipeline

- Event consumer: Deployment when workers are interchangeable.
- Finite backfill: Job with bounded parallelism.
- Daily aggregation: CronJob that creates a Job.
- Shared persistent state: external durable storage or a carefully designed StatefulSet.

## Anti-patterns

- Running production services as naked Pods without a controller.
- Using a StatefulSet solely because an app uses a database; choose based on identity and storage requirements.
- Using a Deployment for a clustered system that requires stable per-member identity.
- Using a CronJob for sub-minute or real-time scheduling.
- Treating Job retries as exactly-once execution.
- Making liveness depend on every downstream dependency.
- Assuming replicas automatically make a single-writer database highly available.

## Production readiness checklist

- [ ] Correct controller selected for workload semantics.
- [ ] Images pinned to approved versions or immutable digests.
- [ ] CPU and memory requests configured.
- [ ] Limits reviewed against workload behavior.
- [ ] Readiness, liveness, and startup probes have distinct purposes.
- [ ] Graceful shutdown and termination window tested.
- [ ] Security context and service account follow least privilege.
- [ ] Rolling update capacity and rollback process tested.
- [ ] Stateful data has backup and restore procedures.
- [ ] Batch work is idempotent and observable.
- [ ] Logs, metrics, and alerts cover application behavior.

## References

- [Workloads overview](https://kubernetes.io/docs/concepts/workloads/)
- [Workload controllers](https://kubernetes.io/docs/concepts/workloads/controllers/)
