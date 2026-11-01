# Lab 03 — Secret Injection and Access Control

## Safety

This lab uses only a fake credential. Do not substitute a production password, token, or private key.

## Step 1 — Create namespace and demo Secret

```bash
kubectl create namespace config-lab
kubectl apply -f manifests/secret-demo.yaml
```

## Step 2 — Deploy a Pod that consumes the Secret

```bash
kubectl apply -f manifests/secret-env-deployment.yaml
kubectl rollout status deployment/secret-demo -n config-lab
```

## Step 3 — Verify key presence without printing value

```bash
kubectl exec deploy/secret-demo -n config-lab -- sh -c 'test -n "$DEMO_TOKEN" && echo token-present'
```

Do not print the token.

## Step 4 — Inspect metadata only

```bash
kubectl describe secret demo-credentials -n config-lab
```

Avoid `kubectl get secret -o yaml` in shared environments.

## Step 5 — RBAC discussion

Review [`07-secret-security.md`](../07-secret-security.md). Create a narrowly scoped Role and RoleBinding only if your lab account has permission. Verify with `kubectl auth can-i`.

## Cleanup

```bash
kubectl delete namespace config-lab
```
