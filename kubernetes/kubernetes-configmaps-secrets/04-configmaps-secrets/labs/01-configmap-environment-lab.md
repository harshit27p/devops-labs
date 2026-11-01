# Lab 01 — ConfigMap Environment Variables

## Objective

Create a ConfigMap, inject values into a Deployment, and observe update behavior.

## Step 1 — Create namespace and ConfigMap

```bash
kubectl create namespace config-lab
kubectl apply -f manifests/configmap-app.yaml
kubectl get configmap -n config-lab
```

## Step 2 — Deploy application

```bash
kubectl apply -f manifests/configmap-env-deployment.yaml
kubectl rollout status deployment/config-demo -n config-lab
kubectl get pods -n config-lab
```

## Step 3 — Inspect environment

```bash
kubectl exec deploy/config-demo -n config-lab -- printenv APP_MODE
kubectl exec deploy/config-demo -n config-lab -- printenv LOG_LEVEL
```

## Step 4 — Update ConfigMap

Change `LOG_LEVEL` in the ConfigMap:

```bash
kubectl edit configmap app-settings -n config-lab
```

Inspect the existing Pod environment again. It will still have the value captured when its container started.

## Step 5 — Restart Deployment

```bash
kubectl rollout restart deployment/config-demo -n config-lab
kubectl rollout status deployment/config-demo -n config-lab
kubectl exec deploy/config-demo -n config-lab -- printenv LOG_LEVEL
```

## Cleanup

```bash
kubectl delete namespace config-lab
```
