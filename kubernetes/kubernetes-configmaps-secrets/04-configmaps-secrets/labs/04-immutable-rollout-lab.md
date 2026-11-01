# Lab 04 — Immutable ConfigMap and Versioned Rollout

## Objective

Create an immutable configuration object and update a workload by changing its reference to a new version.

## Step 1 — Apply initial version

```bash
kubectl create namespace config-lab
kubectl apply -f manifests/immutable-configmap.yaml
```

## Step 2 — Inspect immutability

```bash
kubectl get configmap app-settings-v1 -n config-lab -o yaml
```

Attempting to change its data should be rejected by the API server.

## Step 3 — Create a new version

```bash
kubectl create configmap app-settings-v2 \
  --from-literal=APP_MODE=staging -n config-lab
```

## Step 4 — Update workload reference

In a Deployment, change the referenced ConfigMap name from `app-settings-v1` to `app-settings-v2`, then apply the updated manifest. Observe the rollout.

## Step 5 — Cleanup

```bash
kubectl delete namespace config-lab
```

Retain old versions in real environments only for the planned rollback window.
