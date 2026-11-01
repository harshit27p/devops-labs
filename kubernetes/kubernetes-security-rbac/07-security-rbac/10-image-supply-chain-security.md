# 10 — Image and Software Supply-Chain Security

A secure workload begins before scheduling: the image and its build/deployment provenance matter.

## Controls
- Use trusted, maintained base images.
- Pin production images by immutable digest where practical.
- Scan images for known vulnerabilities and prioritize exploitability and reachability.
- Generate and verify SBOMs.
- Sign images and verify signatures through an admission or deployment policy.
- Build with minimal packages and non-root defaults.
- Protect CI credentials and build runners.
- Rebuild regularly to incorporate security fixes.

## Digest pinning
```yaml
containers:
  - name: app
    image: registry.example.com/team/app@sha256:<digest>
```
Replace the placeholder with the real digest. Tags can move; digests identify immutable content.

## ImagePullSecrets
Use namespace-scoped pull credentials only when required. Prefer workload identity or registry integration where supported. Do not commit registry passwords into manifests.

## Supply-chain stages
```mermaid
flowchart LR
 A[Source] --> B[CI build]
 B --> C[Scan and SBOM]
 C --> D[Sign artifact]
 D --> E[Registry]
 E --> F[Admission verification]
 F --> G[Cluster workload]
```

## Runtime considerations
Image scanning does not replace runtime least privilege, network isolation, patching, or monitoring.
