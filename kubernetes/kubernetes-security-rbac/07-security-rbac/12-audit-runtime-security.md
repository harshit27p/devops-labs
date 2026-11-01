# 12 — Audit Logging and Runtime Detection

## Audit logging
Kubernetes API audit logs record API activity according to an audit policy configured on the API server. Managed clusters may expose audit configuration and logs through provider-specific services.

Audit policy levels commonly include:
- `None`
- `Metadata`
- `Request`
- `RequestResponse`

Avoid logging sensitive request/response bodies unless there is a reviewed requirement; audit logs can themselves contain secrets or personal data.

## Detection signals
- Unexpected RoleBinding/ClusterRoleBinding changes.
- New privileged Pods or hostPath mounts.
- Use of `pods/exec` or port-forward.
- Secret reads by unusual identities.
- Workloads using unexpected images or registries.
- Repeated authentication failures.
- Unexpected service account token use.

## Runtime detection
Runtime security tools may monitor process execution, syscalls, file changes, and network behavior. They complement—not replace—RBAC, admission, and network controls.

## Incident evidence
Capture timestamps, identity, source IP where available, namespace, object name, audit event ID, relevant Pod/node, image digest, and recent changes. Preserve evidence securely and avoid modifying compromised resources before evidence collection unless containment requires it.
