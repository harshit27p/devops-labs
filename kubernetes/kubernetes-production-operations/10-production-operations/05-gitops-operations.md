# 05 — GitOps and Release Operations

## GitOps operating model

Git is the reviewed source of desired state. A reconciliation controller continuously compares the declared state with the live cluster and applies approved changes.

Core principles:
- declarative desired state;
- versioned and reviewed changes;
- automated reconciliation;
- drift visibility and correction;
- auditable promotion between environments.

Common tools include Argo CD and Flux. Their APIs and workflows differ; use the official documentation for the installed version.

## Repository design

Separate reusable application definitions from environment-specific configuration. Keep secrets out of plaintext Git; use sealed/encrypted secrets or external secret management with controlled decryption and identity.

A typical flow:

```mermaid
flowchart LR
  DEV[Developer change] --> PR[Pull request]
  PR --> CI[Tests and policy checks]
  CI --> MERGE[Reviewed merge]
  MERGE --> GIT[Desired state in Git]
  GIT --> CTRL[GitOps controller]
  CTRL --> CLUSTER[Kubernetes cluster]
  CLUSTER --> STATUS[Health and drift status]
  STATUS --> CTRL
```

## Promotion strategy

Promote the same immutable artifact through environments. Change environment configuration, not the image contents. Use approvals for production and preserve traceability from commit to deployed image digest.

## Drift and emergency changes

A GitOps controller may revert manual changes. During an incident, use the documented break-glass procedure, record the change, and reconcile Git promptly. Avoid leaving untracked configuration in production.

## Operational controls

- Protect main branches and require reviews.
- Run schema, policy, security, and manifest validation in CI.
- Pin chart and image versions.
- Separate cluster credentials and environment permissions.
- Define sync windows or approvals for sensitive systems.
- Monitor reconciliation failures and stale revisions.

## Further reading

- https://opengitops.dev/
- https://argo-cd.readthedocs.io/
- https://fluxcd.io/docs/
