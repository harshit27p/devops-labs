# 05 — ServiceAccounts and Workload Identity

A ServiceAccount provides an identity for a workload running in a namespace. Pods can use it to authenticate to the Kubernetes API and, with supported integrations, external cloud services.

## Assign a ServiceAccount
```yaml
spec:
  serviceAccountName: app-reader
  automountServiceAccountToken: false
```
Disable automatic token mounting when the workload does not need Kubernetes API access. If API access is required, grant a narrowly scoped Role and RoleBinding.

## Projected tokens
Kubernetes can project short-lived ServiceAccount tokens with a specific audience. Token rotation and validation behavior should be handled by supported client libraries and cluster configuration.

## External workload identity
Cloud platforms may support federated identity that maps Kubernetes ServiceAccount tokens to cloud IAM identities. This can avoid embedding static cloud credentials in Pods. Follow the exact provider's trust and audience configuration.

## Inspect
```bash
kubectl get serviceaccounts -n <namespace>
kubectl describe serviceaccount -n <namespace> <name>
kubectl get pod <pod> -o yaml
```

## Recommendations
- Use a dedicated ServiceAccount per workload or trust boundary.
- Disable token automount when unused.
- Do not use the `default` ServiceAccount for privileged application access.
- Avoid long-lived token Secrets.
- Restrict who can create Pods using privileged ServiceAccounts.
