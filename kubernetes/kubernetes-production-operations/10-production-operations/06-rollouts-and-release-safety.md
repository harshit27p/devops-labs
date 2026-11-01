# 06 — Safe Releases, Rollback, and Progressive Delivery

## Release safety fundamentals

A release is safe when it is observable, reversible, and constrained in blast radius. A successful Kubernetes rollout does not necessarily mean the application is healthy from a user perspective.

## Deployment strategies

- **Rolling update:** incrementally replaces old Pods; configure `maxSurge` and `maxUnavailable`.
- **Recreate:** terminates old Pods before creating new ones; may cause downtime.
- **Blue/green:** deploys a second environment and shifts traffic after validation.
- **Canary:** sends a small share of traffic to the new version and increases exposure based on health signals.

Blue/green and canary traffic shifting generally require application routing, a service mesh, gateway, ingress controller, or progressive delivery controller.

## Deployment inspection

```bash
kubectl rollout status deployment/<name> -n <namespace>
kubectl rollout history deployment/<name> -n <namespace>
kubectl describe deployment/<name> -n <namespace>
kubectl get rs,pods -n <namespace> -l app=<label>
```

Rollback:

```bash
kubectl rollout undo deployment/<name> -n <namespace>
kubectl rollout status deployment/<name> -n <namespace>
```

A rollback restores a prior Pod template; it does not reverse database schema changes or external side effects.

## Release gates

- image digest and provenance verified;
- manifest and policy checks passed;
- readiness and startup probes reflect actual service readiness;
- smoke tests pass;
- error rate and latency remain within agreed thresholds;
- dependency and data migration compatibility confirmed;
- rollback path tested.

## Database migration safety

Use expand-and-contract migrations where possible: add backward-compatible schema, deploy compatible application versions, migrate data, then remove obsolete schema only after old versions are gone. Avoid assuming application rollback can reverse a destructive migration.

## Progressive delivery

Use small increments and automated analysis only when metrics are trustworthy and traffic volume is sufficient. Define an automatic pause/rollback threshold and a human override process.
