# 03 — Deployments

## 1. Why Deployments?

A Deployment manages a stateless application by declaring the desired Pod template and replica count. It manages ReplicaSets to support controlled rollouts and rollback. Pods are considered interchangeable; persistent per-replica identity belongs in a StatefulSet design.

## 2. Core fields

- `replicas`: desired Pod count.
- `selector`: labels identifying Pods managed by the Deployment; must match template labels.
- `template`: Pod specification used to create new Pods.
- `strategy`: update behavior (`RollingUpdate` or `Recreate`).
- `minReadySeconds`: time a Pod must remain ready before being considered available.
- `revisionHistoryLimit`: number of old ReplicaSets retained for rollback history.
- `progressDeadlineSeconds`: deadline before a stalled rollout is reported as failed progress.

## 3. RollingUpdate strategy

`maxSurge` controls how many extra Pods can be created above the desired count during an update. `maxUnavailable` controls how many Pods may be unavailable during the rollout. Values can be integers or percentages.

For a production rollout:
- Set meaningful readiness probes so unready Pods do not receive Service traffic.
- Ensure capacity for surge Pods.
- Use `minReadySeconds` where brief readiness flapping is a concern.
- Monitor application-level metrics and logs, not only rollout status.

## 4. Example production-oriented manifest

See [`manifests/deployment-nginx.yaml`](manifests/deployment-nginx.yaml). It demonstrates replicas, resource requests/limits, probes, rolling update, labels, and a non-root security context. Review compatibility of the image and security settings for your chosen application.

## 5. Rollout workflow

```bash
kubectl apply -f deployment-nginx.yaml
kubectl rollout status deployment/nginx-web -n workloads-lab
kubectl rollout history deployment/nginx-web -n workloads-lab
kubectl set image deployment/nginx-web nginx=nginx:1.28 -n workloads-lab
kubectl rollout status deployment/nginx-web -n workloads-lab
kubectl rollout undo deployment/nginx-web -n workloads-lab
```

For controlled releases, prefer updating the manifest in version control and applying it, rather than relying on an imperative image change that is not committed to source.

## 6. Scaling

```bash
kubectl scale deployment/nginx-web --replicas=4 -n workloads-lab
kubectl get deployment nginx-web -n workloads-lab
```

Manual scaling can be overwritten by a declarative source or an autoscaler. When using HorizontalPodAutoscaler, avoid competing writers for the replica count.

## 7. Recreate vs RollingUpdate

- `RollingUpdate`: gradually replaces old Pods; default and usually preferred for stateless services.
- `Recreate`: terminates old Pods before creating new ones; can cause downtime but may be required when versions cannot safely overlap.

Neither strategy guarantees zero downtime by itself. Application compatibility, readiness, capacity, and traffic management matter.

## 8. Rollout troubleshooting

```bash
kubectl describe deployment nginx-web -n workloads-lab
kubectl get rs -n workloads-lab
kubectl get pods -n workloads-lab -o wide
kubectl get events -n workloads-lab --sort-by=.metadata.creationTimestamp
kubectl rollout status deployment/nginx-web -n workloads-lab
```

Check:
- Image cannot be pulled or tag does not exist.
- Readiness probe fails, preventing availability.
- Resource requests cannot be scheduled.
- Admission policy rejects the Pod.
- Quota or limit range blocks creation.
- `progressDeadlineSeconds` exceeded.

A rollback changes the Deployment Pod template to a previous revision. It does not undo external database migrations or data changes; design backward-compatible releases.

## References

- [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Rolling updates](https://kubernetes.io/docs/tutorials/kubernetes-basics/update/update-intro/)
