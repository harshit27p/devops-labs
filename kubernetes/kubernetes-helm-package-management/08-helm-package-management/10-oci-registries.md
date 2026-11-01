# 10 — OCI Registries and Chart Distribution

Helm supports storing and distributing charts through OCI-compatible registries.

## Login and push
```bash
helm registry login registry.example.com
helm package ./charts/platform-web
helm push platform-web-0.1.0.tgz oci://registry.example.com/helm
```

## Pull and install
```bash
helm pull oci://registry.example.com/helm/platform-web --version 0.1.0
helm install web oci://registry.example.com/helm/platform-web   --version 0.1.0 -n demo --create-namespace
```

The exact OCI reference format and registry capabilities should be checked against the Helm version and registry implementation.

## Authentication
Use short-lived credentials or CI workload identity where supported. Avoid passing passwords directly on command lines. Use least-privilege push/pull permissions and rotate credentials.

## Artifact integrity
Use immutable tags/digests where available, verify provenance/signatures according to your organization's process, and retain chart source plus build metadata for reproducibility.
