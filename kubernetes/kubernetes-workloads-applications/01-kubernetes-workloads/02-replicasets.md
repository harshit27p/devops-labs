# 02 — ReplicaSets

## Purpose

A ReplicaSet maintains a stable set of matching Pods and attempts to keep the number of replicas equal to `spec.replicas`. It uses a label selector to identify Pods and a Pod template to create replacements.

## Reconciliation model

1. Read desired replica count and selector.
2. Count matching Pods that the ReplicaSet owns.
3. Create Pods when there are too few.
4. Remove excess Pods when there are too many.
5. Repeat reconciliation as cluster state changes.

A ReplicaSet provides replication and self-healing for its Pod set. It does not provide the full rollout history and update orchestration expected for application releases.

## Why Deployments are usually preferred

A Deployment manages ReplicaSets and provides declarative updates, rollout status, history, and rollback. Create a ReplicaSet directly only when you specifically need that primitive or are studying its behavior.

## Example

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: frontend-rs
spec:
  replicas: 3
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
        - name: web
          image: nginx:1.27
          ports:
            - containerPort: 80
```

The selector must match the labels in the Pod template. Overlapping selectors between controllers can cause unexpected ownership and should be avoided.

## Commands

```bash
kubectl get rs -n <ns>
kubectl describe rs <name> -n <ns>
kubectl get pods -n <ns> -l app=frontend --show-labels
kubectl scale rs/frontend-rs --replicas=5 -n <ns>
kubectl explain replicaset.spec
```

## Troubleshooting

- **Replica count below desired:** inspect Events, scheduling constraints, quota, resource requests, and image pull errors.
- **Unexpected Pod adoption:** check selector overlap and labels.
- **Pods repeatedly replaced:** inspect container exits and Pod conditions; a ReplicaSet replaces missing Pods but does not repair faulty application code.

## References

- [ReplicaSet concept](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/)
- [Labels and selectors](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/)
