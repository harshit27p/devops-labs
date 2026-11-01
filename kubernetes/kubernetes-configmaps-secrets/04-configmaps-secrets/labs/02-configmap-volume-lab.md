# Lab 02 — ConfigMap Volume Update Behavior

## Objective

Mount configuration as a file and observe eventual projection updates.

## Step 1 — Create namespace and ConfigMap

```bash
kubectl create namespace config-lab
kubectl apply -f manifests/configmap-app.yaml
kubectl apply -f manifests/configmap-volume-deployment.yaml
```

## Step 2 — Read mounted file

```bash
kubectl exec deploy/config-volume-demo -n config-lab -- cat /etc/app-config/app.properties
```

## Step 3 — Change ConfigMap

```bash
kubectl edit configmap app-settings -n config-lab
```

Wait for kubelet projection to update, then read the file again. The exact delay is not immediate or fixed.

## Step 4 — Application reload

The file can update while the process continues running. Whether the application uses the new value depends on whether it watches or rereads the file.

## Step 5 — Compare with subPath

If a key is mounted using `subPath`, updates are not propagated to that mount. Avoid this pattern for live-updated configuration.

## Cleanup

```bash
kubectl delete namespace config-lab
```
