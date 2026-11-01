# 08 — Hooks and Lifecycle Automation

Helm hooks allow chart resources to run at specific points in a release lifecycle, such as pre-install, post-install, pre-upgrade, post-upgrade, pre-delete, and post-delete.

## Example annotation
```yaml
metadata:
  annotations:
    helm.sh/hook: pre-upgrade
    helm.sh/hook-weight: "-5"
    helm.sh/hook-delete-policy: before-hook-creation,hook-succeeded
```

## Use cases
- Pre-upgrade validation.
- Database migration jobs.
- Post-deploy smoke tests.
- Controlled cleanup tasks.

## Risks
Hooks can introduce ordering, retries, and failure complexity. A migration may be irreversible even if Helm rolls back the release. Hook-created resources are managed differently from ordinary release resources and may remain unless deletion policy is configured.

## Best practices
- Make hooks idempotent where possible.
- Set Job backoff and active deadlines.
- Use dedicated ServiceAccounts and minimal RBAC.
- Avoid embedding credentials.
- Document rollback and partial-failure recovery.
- Do not use hooks as a substitute for a proper database migration system.
