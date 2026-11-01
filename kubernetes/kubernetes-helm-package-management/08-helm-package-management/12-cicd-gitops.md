# 12 — Helm in CI/CD and GitOps

## CI/CD pattern
1. Validate source and chart metadata.
2. Lint and render with environment values.
3. Run policy/security checks.
4. Package and sign/publish the chart.
5. Deploy to staging.
6. Run smoke/integration tests.
7. Promote the same immutable artifact to production.

## GitOps pattern
A GitOps controller such as Argo CD or Flux can reconcile Helm charts from Git or OCI sources. The controller owns continuous reconciliation; avoid having a separate CI job and GitOps controller fight over the same resources.

## Environment configuration
Keep common defaults in `values.yaml`; environment-specific values in reviewed files. Avoid copying whole charts per environment.

## Promotion
Promote the same chart version and image digests between environments. Change only environment-specific configuration. Record release version, commit SHA, chart digest, image digest, and deployment outcome.

## Secrets
Use the GitOps tool's supported external secret integration or encrypted secret workflow. Never commit raw credentials.
