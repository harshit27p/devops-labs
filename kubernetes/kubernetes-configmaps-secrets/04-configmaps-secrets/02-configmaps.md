# 02 — ConfigMaps

## What is a ConfigMap?

A ConfigMap stores non-confidential configuration as key-value data. Pods can consume it as environment variables, command-line arguments, or mounted files. ConfigMaps are namespaced and are limited in size; they are not intended for large data stores.

## Create a ConfigMap imperatively

```bash
kubectl create configmap app-settings \
  --from-literal=APP_MODE=development \
  --from-literal=LOG_LEVEL=info \
  -n config-lab
```

From a file:

```bash
kubectl create configmap app-config \
  --from-file=application.properties \
  -n config-lab
```

## Declarative example

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-settings
  namespace: config-lab
data:
  APP_MODE: "development"
  LOG_LEVEL: "info"
  application.yaml: |
    server:
      port: 8080
    feature:
      newCheckout: false
```

`data` contains UTF-8 strings. `binaryData` can be used for binary values encoded as base64 in the manifest representation.

## Inspect and update

```bash
kubectl get configmap -n config-lab
kubectl describe configmap app-settings -n config-lab
kubectl get configmap app-settings -n config-lab -o yaml
kubectl edit configmap app-settings -n config-lab
```

Avoid displaying ConfigMaps containing internal details in public logs or screenshots even though they are not designed for secrets.

## Best practices

- Keep each ConfigMap focused on one application's configuration.
- Use clear, stable key names.
- Validate application configuration before rollout.
- Do not place passwords or tokens in ConfigMaps.
- Consider immutable/versioned ConfigMaps for controlled releases.
- Keep manifests in version control, with environment-specific overlays where appropriate.

## Reference

- [ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/)
