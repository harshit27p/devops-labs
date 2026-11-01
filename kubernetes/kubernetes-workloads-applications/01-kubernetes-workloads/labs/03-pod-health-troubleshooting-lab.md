# Lab 03 — Probe Behavior and Pod Troubleshooting

## Objective

Inspect a Pod with health probes and practice a repeatable troubleshooting sequence.

## Step 1 — Apply probe example

```bash
kubectl create namespace workloads-health-lab
kubectl apply -n workloads-health-lab -f manifests/pod-probes.yaml
kubectl get pods -n workloads-health-lab -w
```

## Step 2 — Inspect probe status and Events

```bash
kubectl describe pod probe-demo -n workloads-health-lab
kubectl get events -n workloads-health-lab --sort-by=.metadata.creationTimestamp
```

## Step 3 — Inspect logs and restart count

```bash
kubectl logs probe-demo -n workloads-health-lab
kubectl logs probe-demo -n workloads-health-lab --previous
kubectl get pod probe-demo -n workloads-health-lab -o json
```

`--previous` is useful only when a prior container instance exists.

## Troubleshooting decision sequence

1. Confirm namespace and context.
2. Check Pod phase, conditions, and node assignment.
3. Read Events for scheduling, image, mount, and probe errors.
4. Read current and previous container logs.
5. Check container exit code, reason, and restart count.
6. Verify probe path/port and application bind address.
7. Check resource requests, limits, and node pressure.
8. Check referenced ConfigMaps, Secrets, volumes, and service accounts.

## Cleanup

```bash
kubectl delete namespace workloads-health-lab
```
