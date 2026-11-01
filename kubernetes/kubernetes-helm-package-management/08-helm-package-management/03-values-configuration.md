# 03 — Values and Configuration

`values.yaml` provides defaults. Users can override values with `-f` files and `--set`/`--set-string`/`--set-file` flags.

## Precedence
For typical Helm usage, later `-f` files override earlier files, and command-line `--set` values override values files. Confirm exact behavior for your Helm version and command.

```bash
helm upgrade --install web ./charts/platform-web   -n demo --create-namespace   -f values-prod.yaml   --set replicaCount=3
```

## Design values as an API
- Prefer clear nested structures.
- Keep secure defaults.
- Avoid excessive knobs that expose implementation details.
- Document every configurable field.
- Use `values.schema.json` to validate shape and types.
- Avoid putting plaintext credentials in values files or shell history.

## Schema
A JSON Schema can define required fields, types, ranges, and enums. It helps reject invalid chart configuration before resources are submitted.

## Debug merged values
```bash
helm get values <release> -n <namespace>
helm get values <release> -n <namespace> --all
helm template web ./charts/platform-web -f values-prod.yaml
```

Be careful: rendered output and release values can contain sensitive data if a chart handles secrets poorly.
