# 07 — CronJobs

## Purpose

A CronJob creates Jobs on a repeating schedule using cron syntax. It is suitable for periodic tasks such as reports, cleanup, synchronization, and backups.

## Example

See [`manifests/cronjob-report.yaml`](manifests/cronjob-report.yaml).

```bash
kubectl apply -f manifests/cronjob-report.yaml
kubectl get cronjobs -n workloads-lab
kubectl get jobs -n workloads-lab
kubectl describe cronjob report-generator -n workloads-lab
```

## Scheduling and concurrency

- `schedule`: cron expression, interpreted using the configured time zone behavior supported by the cluster version.
- `concurrencyPolicy: Allow`: overlapping Jobs are allowed.
- `Forbid`: skips a new run while a previous Job is active.
- `Replace`: replaces an active Job with a new one.
- `startingDeadlineSeconds`: maximum delay for starting a missed schedule.
- `successfulJobsHistoryLimit` and `failedJobsHistoryLimit`: retained Job history counts.
- `suspend`: prevents future Job creation while true.

Use `.spec.timeZone` when supported by the Kubernetes version and explicitly required. Otherwise schedules are interpreted in the controller manager's local time zone; verify the cluster's behavior rather than assuming UTC.

## Reliability patterns

- Make tasks idempotent.
- Set resource requests and limits.
- Add a timeout (`activeDeadlineSeconds`) to the Job template.
- Decide whether overlapping executions are safe.
- Alert on failed or missed runs.
- Store output in durable storage or an external system, not only in Pod logs.
- Set retention limits to avoid unbounded Job accumulation.

Cron scheduling is not a precision real-time scheduler. Controller downtime, missed schedules, and concurrency policy can affect execution timing.

## Reference

- [CronJobs](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/)
