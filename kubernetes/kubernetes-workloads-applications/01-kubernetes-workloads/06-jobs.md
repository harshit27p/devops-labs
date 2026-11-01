# 06 — Jobs

## Purpose

A Job creates one or more Pods and tracks successful completion. Use it for finite work such as data migration, report generation, batch processing, or one-time maintenance.

## Important fields

- `completions`: number of successful completions required.
- `parallelism`: maximum number of Pods running concurrently.
- `backoffLimit`: retry limit before the Job is considered failed.
- `activeDeadlineSeconds`: overall time limit for the Job.
- `ttlSecondsAfterFinished`: optional cleanup delay after completion.

A Job's Pods commonly use `restartPolicy: Never` or `OnFailure`. Choose based on whether the kubelet should restart the container in the same Pod or let the Job controller create a replacement Pod.

## Example

See [`manifests/job-batch.yaml`](manifests/job-batch.yaml).

```bash
kubectl apply -f manifests/job-batch.yaml
kubectl get jobs,pods -n workloads-lab
kubectl logs job/batch-report -n workloads-lab
kubectl describe job batch-report -n workloads-lab
```

## Parallel jobs

For independent work items, configure `parallelism` and `completions`. For work queues, the application must coordinate which worker processes which item; Kubernetes does not automatically provide exactly-once business processing.

Design batch tasks to be idempotent. A retry may execute work again after partial failure. Use durable checkpoints, unique job identifiers, and transactional writes where needed.

## Failure handling

- Image pull or scheduling failure: inspect Pod Events.
- Non-zero exit: inspect logs and exit code.
- Repeated retries: review `backoffLimit`, transient dependency failures, and idempotency.
- Long-running task: set a sensible `activeDeadlineSeconds`.
- Completed Job accumulation: use TTL cleanup where appropriate, while retaining required audit evidence elsewhere.

## Reference

- [Jobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/)
