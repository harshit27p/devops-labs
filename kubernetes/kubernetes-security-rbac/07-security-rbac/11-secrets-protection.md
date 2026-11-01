# 11 — Secrets Protection and Encryption

Kubernetes Secret objects hold sensitive values, but their existence does not automatically provide complete secret management.

## Security baseline
- Enable encryption at rest for Secrets in etcd using the distribution/provider-supported mechanism.
- Restrict `get`, `list`, and `watch` on Secrets with RBAC.
- Avoid exposing Secrets as environment variables when file projection or external secret delivery is more appropriate.
- Do not log secret values.
- Rotate credentials and audit access.
- Use external secret managers or workload identity where suitable.

## Base64 is not encryption
Secret `data` values are base64 encoded for representation. Anyone with sufficient API access or etcd access may recover the plaintext unless encryption and access controls are configured.

## Avoid accidental exposure
- Do not place credentials in Git, container images, command history, or CI logs.
- Restrict Pod creation in namespaces containing sensitive Secrets; a user able to create arbitrary Pods may often arrange to mount namespace Secrets.
- Keep backups containing Secrets protected.
- Prefer short-lived credentials.

For full ConfigMap/Secret injection and external secret patterns, see Module 04 — ConfigMaps & Secrets. This guide focuses on security boundaries and operational controls.
