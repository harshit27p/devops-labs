# 04 — Roles, ClusterRoles, and Bindings

## Objects
- **Role:** grants permissions within one namespace.
- **ClusterRole:** grants permissions at cluster scope or can be bound within a namespace.
- **RoleBinding:** grants a Role or ClusterRole to subjects within one namespace.
- **ClusterRoleBinding:** grants a ClusterRole across the cluster.

## Namespace-scoped example
See `manifests/rbac-reader.yaml`.

A Role defines rules; a RoleBinding connects the Role to a user, group, or ServiceAccount. A RoleBinding that references a ClusterRole still grants permissions only in the RoleBinding's namespace.

## Cluster-scoped caution
ClusterRoleBindings can grant access across namespaces and to cluster-scoped resources. Review them carefully:
```bash
kubectl get clusterrolebindings
kubectl describe clusterrolebinding <name>
kubectl get clusterroles
```

## Subresources
Some sensitive operations use subresources, such as `pods/exec`, `pods/log`, `pods/portforward`, and `deployments/scale`. Permission to read Pods is not the same as permission to execute commands in them.

## Review permissions
```bash
kubectl get roles,rolebindings -A
kubectl get clusterroles,clusterrolebindings
kubectl describe role -n <namespace> <role>
kubectl auth can-i --list -n <namespace>
```

## Avoid privilege escalation
Do not grant users the ability to create or modify Roles/RoleBindings unless required. Kubernetes RBAC includes safeguards around granting permissions the caller does not possess, but administrative permissions and escalation-related verbs must still be tightly controlled.
