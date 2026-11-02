# Trivy JSON Reports

Trivy can report vulnerabilities in container images, filesystems and other supported targets. Use only approved artifacts and environments.

Example for an image you own:

```bash
trivy image --format json --output trivy-report.json example-app:local
```

## Parsing approach
- Read the top-level results array.
- Iterate target results and vulnerability arrays.
- Preserve package name, installed version, fixed version, vulnerability ID and severity.
- Keep target/image digest and scanner database metadata where available.

Do not treat an empty result as proof of safety: confirm that the intended target was scanned successfully and that the report contains expected metadata.
