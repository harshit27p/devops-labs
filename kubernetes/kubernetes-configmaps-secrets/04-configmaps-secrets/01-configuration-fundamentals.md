# 01 — Configuration Management Fundamentals

## Why externalize configuration?

Container images should package application code and runtime dependencies, not environment-specific values. The same image should be promotable from development to staging and production while configuration changes independently.

Examples of configuration:
- Log level and feature flags.
- Service URLs and ports.
- Non-sensitive application settings.
- Database connection parameters that are not credentials.
- Credentials, tokens, and private keys (sensitive data).

## ConfigMap vs Secret

| Requirement | Resource |
|---|---|
| Non-sensitive settings | ConfigMap |
| Password, token, private key | Secret or external secret manager |
| Binary configuration file | ConfigMap or Secret binary data, within size constraints |
| Large durable application data | External storage, not ConfigMap/Secret |
| Dynamic centralized secret rotation | External secret manager integration |

A Secret is a Kubernetes API object designed for sensitive data. It does not automatically encrypt values in etcd or prevent authorized users and workloads from reading them.

## Configuration delivery methods

1. Environment variables: easy for simple values; process environment is fixed at container start.
2. `env` / `envFrom`: explicit or bulk import from ConfigMap/Secret keys.
3. Volumes: deliver configuration as files.
4. Application API or external secret provider: useful for dynamic retrieval and rotation.

## Design questions

- Is the value confidential?
- Does the application expect a file or an environment variable?
- Does the application reload changes dynamically?
- How is the value versioned and promoted?
- Who can read or update it?
- How is it rotated and audited?
- Can it leak into logs, crash dumps, command output, or metrics?

## References

- [ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/)
- [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
