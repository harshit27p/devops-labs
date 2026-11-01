# 03 — Authorization and RBAC

Authorization determines whether an authenticated identity may perform an API operation. Kubernetes supports authorization modes including RBAC and, depending on configuration, other authorizers.

## RBAC request dimensions
An authorization decision evaluates attributes such as:
- Subject: user, group, or ServiceAccount.
- Verb: get, list, watch, create, update, patch, delete, and others.
- API group and resource.
- Namespace.
- Resource name and subresource where applicable.

## Least privilege
Grant only the minimum verbs and resources needed. Prefer namespace-scoped permissions for application teams. Avoid `*` wildcards and broad access to Secrets, Pods/exec, Roles, RoleBindings, or cluster-scoped resources.

## Check permissions
```bash
kubectl auth can-i get pods -n dev
kubectl auth can-i create deployments -n dev
kubectl auth can-i list secrets -n dev
kubectl auth can-i --list -n dev
```

To test as a ServiceAccount:
```bash
kubectl auth can-i get pods -n dev --as=system:serviceaccount:dev:app-reader
```
The caller needs permission to impersonate the tested identity.

## RBAC does not control everything
RBAC governs Kubernetes API requests. It does not directly control Linux syscalls inside a container, traffic between Pods, or access to an external cloud API. Use workload security, NetworkPolicy, and cloud IAM/workload identity for those layers.
