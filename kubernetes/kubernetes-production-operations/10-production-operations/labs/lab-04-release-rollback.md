# Lab 04 — Release Validation and Rollback Drill

## Objective

Perform a controlled Deployment update, observe rollout health, and roll back.

## Deploy

```bash
kubectl create namespace release-lab
kubectl create deployment web --image=nginx:1.27 -n release-lab
kubectl rollout status deployment/web -n release-lab
kubectl rollout history deployment/web -n release-lab
```

## Update

```bash
kubectl set image deployment/web nginx=nginx:1.28 -n release-lab
kubectl rollout status deployment/web -n release-lab
kubectl rollout history deployment/web -n release-lab
```

If the chosen image tag is unavailable in your environment, use a known-good alternate tag and record the change.

## Roll back

```bash
kubectl rollout undo deployment/web -n release-lab
kubectl rollout status deployment/web -n release-lab
kubectl describe deployment/web -n release-lab
```

## Discuss

- Did Kubernetes report the rollout complete?
- What application-level smoke test would you run?
- What happens if a schema migration is not backward compatible?
- Which metrics and alerts should gate a canary?

## Cleanup

```bash
kubectl delete namespace release-lab
```
