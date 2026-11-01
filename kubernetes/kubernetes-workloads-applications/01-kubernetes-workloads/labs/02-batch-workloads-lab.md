# Lab 02 — Execute a Job and Schedule a CronJob

## Objective

Run a finite task, inspect its completion, and create a scheduled task.

## Step 1 — Create namespace

```bash
kubectl create namespace workloads-lab
```

## Step 2 — Apply Job

```bash
kubectl apply -f manifests/job-batch.yaml
kubectl get jobs,pods -n workloads-lab
```

The manifests create the `workloads-lab` namespace if it does not already exist.

## Step 3 — Inspect completion and logs

```bash
kubectl describe job batch-report -n workloads-lab
kubectl logs job/batch-report -n workloads-lab
```

## Step 4 — Apply CronJob

```bash
kubectl apply -f manifests/cronjob-report.yaml
kubectl get cronjob -n workloads-lab
kubectl get jobs -n workloads-lab --watch
```

The example uses a frequent schedule for lab observation. Do not copy a frequent schedule into production without a clear need.

## Step 5 — Trigger a one-off Job from the CronJob

```bash
kubectl create job manual-report --from=cronjob/report-generator -n workloads-lab
kubectl get jobs -n workloads-lab
kubectl logs job/manual-report -n workloads-lab
```

## Step 6 — Cleanup

```bash
kubectl delete namespace workloads-lab
```

## Questions

1. What distinguishes Job completion from Deployment availability?
2. Why should batch tasks be idempotent?
3. Compare CronJob concurrency policies `Allow`, `Forbid`, and `Replace`.
4. Which fields limit retries and total execution time?
5. Where should important batch output be stored?
