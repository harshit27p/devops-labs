# 12 — Production Configuration Patterns

## Recommended separation

- ConfigMap: non-sensitive environment-specific settings.
- Secret/external secret manager: credentials and private material.
- Deployment: references configuration and defines rollout behavior.
- Application: validates configuration at startup and supports safe reload where appropriate.

## Anti-patterns

- Committing raw credentials to Git.
- Treating base64 as encryption.
- Granting every application ServiceAccount read access to all Secrets.
- Putting sensitive values in command-line arguments.
- Printing complete environment variables or Secret objects in logs.
- Assuming ConfigMap volume updates restart the application.
- Using `subPath` when expecting projected file updates.
- Rotating credentials without coordinating application rollout.
- Storing large files or durable data in ConfigMaps/Secrets.

## Production checklist

- [ ] Sensitive and non-sensitive values are separated.
- [ ] Secret access is least-privilege and namespace-scoped.
- [ ] API datastore encryption at rest is enabled and verified.
- [ ] Backups are encrypted and access-controlled.
- [ ] Secrets are not exposed in source control or CI logs.
- [ ] Rotation and revocation procedures are tested.
- [ ] Applications handle missing/invalid configuration safely.
- [ ] Update behavior is understood for env vars and mounted files.
- [ ] Immutable/versioned configuration is considered.
- [ ] External provider availability and identity are monitored.
- [ ] Secret access is audited.

## Interview quick checks

1. ConfigMap vs Secret?
2. Why is Base64 not encryption?
3. What happens when a ConfigMap environment variable changes?
4. How do projected ConfigMap volume updates work?
5. Why does `subPath` prevent updates?
6. What does `immutable: true` do?
7. How does RBAC protect Secrets?
8. Why can permission to create Pods be sensitive?
9. Compare External Secrets Operator and Secrets Store CSI Driver.
10. Explain a safe credential rotation sequence.
