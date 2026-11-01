# Lab 02 — Apply and Inspect a Declarative Workload

## Objective

Create a dedicated namespace, apply a Deployment manifest, inspect the API object and controller-created Pods, and remove the lab resources safely.

## Prerequisites

- A development cluster.
- `kubectl` access to create Namespaces and Deployments.
- `nginx:1.27` image access from the cluster nodes.

## Step 1 — Confirm cluster context

```bash
kubectl config current-context
kubectl cluster-info
```

Do not proceed if this is not your intended lab cluster.

## Step 2 — Create the namespace

```bash
kubectl create namespace learning
```

## Step 3 — Inspect the manifest

Use [nginx-deployment.yaml](../manifests/nginx-deployment.yaml). It defines two replicas, a label selector, a container port, resource requests/limits and a basic readiness probe.

## Step 4 — Validate without persisting

```bash
kubectl apply --dry-run=client -f ../manifests/nginx-deployment.yaml
kubectl apply --dry-run=server -f ../manifests/nginx-deployment.yaml
kubectl diff -f ../manifests/nginx-deployment.yaml
```

Server-side dry-run requires cluster connectivity and the necessary permissions.

## Step 5 — Apply

```bash
kubectl apply -f ../manifests/nginx-deployment.yaml
```

## Step 6 — Observe reconciliation

```bash
kubectl get deployment web -n learning
kubectl get replicasets -n learning
kubectl get pods -n learning -o wide
kubectl rollout status deployment/web -n learning
```

Observe how the Deployment controller creates a ReplicaSet and the ReplicaSet controller creates Pods. The scheduler assigns eligible Pods to nodes; kubelets then coordinate container creation.

## Step 7 — Inspect object details

```bash
kubectl describe deployment web -n learning
kubectl get deployment web -n learning -o yaml
kubectl describe pods -n learning
kubectl get events -n learning --sort-by=.lastTimestamp
```

Compare `spec.replicas` with status fields such as `readyReplicas` and `availableReplicas`.

## Step 8 — Test declarative idempotency

Apply the same manifest again:

```bash
kubectl apply -f ../manifests/nginx-deployment.yaml
```

An unchanged manifest should not create duplicate Deployments. Kubernetes updates the existing object as required.

## Step 9 — Cleanup

```bash
kubectl delete -f ../manifests/nginx-deployment.yaml
kubectl delete namespace learning
```

The second command deletes all namespaced resources remaining in `learning`. Confirm that the namespace is dedicated to this lab before running it.

## Expected learning outcomes

- API acceptance is different from workload readiness.
- A Deployment manages a ReplicaSet, which manages Pods.
- `spec` declares desired state; `status` reports observed state.
- Reapplying a declarative manifest is a normal workflow.
- Events and controller status help explain failures.

## Troubleshooting

| Symptom | Checks |
|---|---|
| Deployment not found | Confirm manifest namespace and apply result |
| Pod Pending | `describe pod`; inspect scheduling events and resources |
| ImagePullBackOff | Image name, registry reachability and pull credentials |
| Readiness probe failing | Pod logs, container port and probe path |
| Permission denied | `kubectl auth can-i create deployments -n learning` |
