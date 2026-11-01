# 07 — Dependencies and Library Charts

Charts can declare dependencies in `Chart.yaml`. Dependencies may be downloaded from chart repositories or OCI registries, depending on repository support.

## Dependency example
```yaml
dependencies:
  - name: common
    version: 1.2.3
    repository: https://charts.example.org
```

Commands:
```bash
helm dependency list ./charts/my-app
helm dependency update ./charts/my-app
helm dependency build ./charts/my-app
```

Commit `Chart.lock` to make dependency resolution reproducible. Package dependencies under `charts/` for controlled offline or release builds.

## Aliases and conditions
Dependencies can use aliases and conditions/tags to enable or disable subcharts. Values are nested under the dependency name or alias.

## Library charts
A chart with `type: library` provides named templates for reuse. It is not deployed as a standalone workload.

## Supply-chain considerations
Pin dependency versions, review chart sources, inspect packaged templates, scan images, verify signatures/provenance where supported, and avoid unreviewed dependency updates in production.
