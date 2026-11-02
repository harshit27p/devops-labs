# Plugin Configuration Validation

Treat plugin configuration as untrusted input even when it comes from a local file.

## Good configuration
- Has a schema and version.
- Rejects unknown or malformed fields where appropriate.
- Has conservative defaults.
- Does not contain plaintext secrets.
- Limits paths, network destinations and resource usage.
- Is validated before plugin execution.

## Exercise
Define a plugin configuration with `enabled`, `timeout_seconds` and `severity_threshold`. Validate types and ranges, and reject timeouts outside 1–120 seconds.
