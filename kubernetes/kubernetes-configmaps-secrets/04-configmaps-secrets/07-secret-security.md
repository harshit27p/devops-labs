# 07 — Secret Security: Encoding, RBAC, and Encryption

## Base64 is encoding, not encryption

Kubernetes Secret `data` values are base64-encoded for representation and transport in the API object. Anyone who can read the object can decode the value. `stringData` accepts unencoded strings on write, but the stored representation is still Secret data; it is not a security boundary.

## Threat model

Sensitive values can be exposed through:
- Excessively broad `get`, `list`, or `watch` permissions on Secrets.
- Workloads that mount secrets they do not need.
- Container logs, debug output, crash dumps, or shell history.
- Unencrypted etcd backups or datastore access.
- Node/root access and privileged workloads.
- CI/CD logs and Git repositories.

## RBAC

Grant only the minimum verbs and namespaces required. A subject with permission to create Pods in a namespace may often arrange for a Pod to consume Secrets in that namespace, so Pod creation itself is a sensitive permission.

Example Role (adapt names and subjects):

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: read-app-secret
  namespace: config-lab
rules:
  - apiGroups: [""]
    resources: ["secrets"]
    resourceNames: ["app-credentials"]
    verbs: ["get"]
```

Bind this Role only to the intended ServiceAccount or user. Avoid broad Secret `list` or `watch` access unless required.

## Encryption at rest

Configure API server encryption providers for sensitive resources and manage encryption keys securely. Verify the cluster's configuration and test backup/restore procedures. Encryption at rest does not replace RBAC: authorized API reads return plaintext values.

## Operational controls

- Use short-lived credentials where possible.
- Rotate secrets and revoke compromised values.
- Restrict node and etcd access.
- Audit Secret reads and writes.
- Avoid printing values in automation output.
- Encrypt backups and protect backup credentials.
- Use dedicated ServiceAccounts and disable unnecessary token automounting.
- Prefer external secret managers for centralized lifecycle and rotation.

## References

- [Good practices for Kubernetes Secrets](https://kubernetes.io/docs/concepts/security/secrets-good-practices/)
- [Encrypting Confidential Data at Rest](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/)
- [RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
