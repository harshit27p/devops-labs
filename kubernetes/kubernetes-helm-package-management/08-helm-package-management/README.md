# Kubernetes Helm & Package Management

Advanced module covering Helm architecture, charts, Go templates, values, release lifecycle, dependencies, hooks, testing, OCI registries, security, GitOps integration, and production operations.

## Learning path
1. [Helm fundamentals and architecture](01-helm-fundamentals.md)
2. [Chart structure and metadata](02-chart-structure.md)
3. [Values and configuration](03-values-configuration.md)
4. [Go templates and functions](04-templates-functions.md)
5. [Template control flow and named templates](05-template-control-flow.md)
6. [Release lifecycle and upgrade strategies](06-release-lifecycle.md)
7. [Dependencies and library charts](07-dependencies-library-charts.md)
8. [Hooks and lifecycle automation](08-hooks-lifecycle.md)
9. [Testing, linting and debugging](09-testing-linting-debugging.md)
10. [OCI registries and chart distribution](10-oci-registries.md)
11. [Helm security and secrets](11-security-secrets.md)
12. [Helm in CI/CD and GitOps](12-cicd-gitops.md)
13. [Production patterns and troubleshooting](13-production-troubleshooting.md)
14. [Interview questions](14-interview-questions.md)

## Labs
- [01 — Install Helm and inspect a chart](labs/01-install-and-inspect.md)
- [02 — Package and deploy the sample chart](labs/02-package-deploy-chart.md)
- [03 — Upgrade, rollback and history](labs/03-upgrade-rollback.md)
- [04 — Test and validate a chart](labs/04-chart-testing.md)

## Sample chart
`charts/platform-web/` contains a small reusable chart with Deployment, Service, optional Ingress, ConfigMap, ServiceAccount, helpers, values, and NOTES. It uses a non-root Nginx image and explicit resource settings. Review image availability and controller prerequisites before deployment.

## Prerequisites
- Kubernetes cluster and `kubectl`.
- Helm 3 or compatible Helm 4 installation; commands are broadly similar, but verify version-specific behavior.
- Familiarity with Deployments, Services, ConfigMaps, Secrets, Ingress/Gateway, and RBAC.

## Official references
- https://helm.sh/docs/
- https://helm.sh/docs/topics/charts/
- https://helm.sh/docs/chart_template_guide/
- https://helm.sh/docs/helm/helm_install/
- https://helm.sh/docs/helm/helm_upgrade/
- https://helm.sh/docs/topics/registries/
- https://helm.sh/docs/topics/charts_hooks/
- https://helm.sh/docs/topics/chart_tests/
