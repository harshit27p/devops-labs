# Lab 01 — Inspect a Kubernetes Cluster

## Objective

Inspect a Kubernetes cluster using `kubectl`, identify its nodes and core system resources, discover API resources, and collect a basic health snapshot.

## Prerequisites

- Access to a development Kubernetes cluster.
- `kubectl` installed and configured.
- Permission to read Nodes, Namespaces, Pods and Events.

## Step 1 — Confirm the active target

```bash
kubectl config current-context
kubectl config get-contexts
kubectl cluster-info
```

**Expected observation:** The active context and API endpoint should match your intended lab cluster. Stop if the context points to production or an unknown cluster.

## Step 2 — Inspect nodes

```bash
kubectl get nodes -o wide
kubectl describe nodes
```

Record each node's status, role, Kubernetes version, internal IP, capacity and allocatable resources.

## Step 3 — Inspect namespaces and system Pods

```bash
kubectl get namespaces
kubectl get pods -n kube-system -o wide
kubectl get daemonsets -n kube-system
kubectl get deployments -n kube-system
```

System components differ by Kubernetes distribution. A managed service may hide control-plane Pods from users.

## Step 4 — Discover API resources

```bash
kubectl api-resources
kubectl api-resources --namespaced=true
kubectl api-resources --namespaced=false
kubectl api-versions
```

Identify five namespaced resources and five cluster-scoped resources.

## Step 5 — Inspect API health endpoints

```bash
kubectl get --raw='/readyz'
kubectl get --raw='/livez'
```

A `Forbidden` response may mean your identity lacks permission to access the non-resource URL; it does not necessarily mean the API server is unhealthy.

## Step 6 — Capture a diagnostic snapshot

```bash
kubectl get nodes -o wide
kubectl get pods -A -o wide
kubectl get events -A --sort-by=.lastTimestamp
kubectl get --raw='/version'
```

Do not publish output containing internal hostnames, IP addresses, usernames, tokens or other sensitive environment details.

## Deliverables

Create a short `cluster-inspection.md` containing:

1. Cluster context name (redact sensitive identifiers if publishing).
2. Number of nodes and their Ready status.
3. Namespaces present.
4. Important system components observed.
5. Examples of namespaced and cluster-scoped resources.
6. Any warnings or events and your interpretation.

## Cleanup

This lab creates no Kubernetes resources. No cleanup is required.

## Troubleshooting

| Problem | Suggested check |
|---|---|
| `kubectl` cannot connect | Context, kubeconfig, endpoint, VPN and cluster status |
| Unauthorized | Credential or identity provider configuration |
| Forbidden | Required RBAC permission |
| No system Pods visible | Managed control plane or restricted namespace access |
| Metrics unavailable | Metrics Server or Metrics API installation and health |
