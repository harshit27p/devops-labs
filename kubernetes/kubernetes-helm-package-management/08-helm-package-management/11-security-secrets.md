# 11 — Helm Security and Secrets

Helm release data is stored in the Kubernetes cluster (commonly as Secrets by default in Helm 3). Release records can contain chart values and rendered manifests. Sensitive values supplied to Helm may therefore be retained in release storage and visible to identities with sufficient access.

## Controls
- Apply least-privilege RBAC to release namespaces and Secrets.
- Avoid plaintext secrets in values files, Git, shell history, CI logs, and rendered artifacts.
- Use an external secret manager or secure secret injection workflow.
- Enable Kubernetes Secret encryption at rest.
- Review chart templates for accidental Secret exposure.
- Pin and verify chart dependencies and images.
- Restrict who can install charts and modify release values.

## Do not assume
- Helm does not automatically encrypt every sensitive value before storing release state.
- A private chart repository does not make embedded credentials safe.
- `--set` does not prevent shell history or process/log exposure.
- Helm rollback does not reverse external side effects.

For Kubernetes Secret design and encryption, see Module 07 and Module 04.
