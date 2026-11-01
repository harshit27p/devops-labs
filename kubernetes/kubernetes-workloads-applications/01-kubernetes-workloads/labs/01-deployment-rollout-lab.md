# Lab 01 — Deploy, Scale, Update, and Roll Back an Application

## Objective

Create a Deployment, inspect the ReplicaSet/Pods it owns, scale it, perform a rolling update, and roll back.

## Prerequisites

A disposable Kubernetes cluster and `kubectl`. Confirm the active context before making changes:

```bash
kubectl config current-context
kubectl get nodes
```

## Step 1 — Create a namespace

```bash
kubectl create namespace workloads-lab
```

## Step 2 — Apply the manifest

From this module directory:

```bash
kubectl apply -f manifests/deployment-nginx.yaml
kubectl get deployment,replicaset,pods -n workloads-lab -o wide
kubectl rollout status deployment/nginx-web -n workloads-lab
```

## Step 3 — Inspect ownership and desired state

```bash
kubectl describe deployment nginx-web -n workloads-lab
kubectl get rs -n workloads-lab
kubectl get pods -n workloads-lab --show-labels
kubectl get deployment nginx-web -n workloads-lab -o yaml
```

Observe how Deployment owns a ReplicaSet and the ReplicaSet owns Pods through owner references.

## Step 4 — Scale

```bash
kubectl scale deployment/nginx-web --replicas=4 -n workloads-lab
kubectl get pods -n workloads-lab -w
```

Return to two replicas through the manifest or command after observing the behavior.

## Step 5 — Update the image

```bash
kubectl set image deployment/nginx-web nginx=nginx:1.28 -n workloads-lab
kubectl rollout status deployment/nginx-web -n workloads-lab
kubectl rollout history deployment/nginx-web -n workloads-lab
```

For reproducible GitOps workflows, edit the version-controlled manifest and apply the change instead of leaving an imperative-only change.

## Step 6 — Roll back

```bash
kubectl rollout undo deployment/nginx-web -n workloads-lab
kubectl rollout status deployment/nginx-web -n workloads-lab
kubectl rollout history deployment/nginx-web -n workloads-lab
```

## Step 7 — Cleanup

```bash
kubectl delete namespace workloads-lab
```

Only run cleanup if this namespace was created for this lab and contains no other work.

## Questions

1. Which controller created the ReplicaSet?
2. What happens to existing Pods when the Pod template changes?
3. How do `maxSurge` and `maxUnavailable` affect rollout capacity?
4. Why is readiness important during a rolling update?
5. Does Deployment rollback reverse a database migration? Explain.
