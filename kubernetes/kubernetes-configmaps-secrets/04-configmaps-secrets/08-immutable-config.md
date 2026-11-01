# 08 — Immutable ConfigMaps and Secrets

## What does immutable mean?

Setting `immutable: true` prevents the data in a ConfigMap or Secret from being changed after creation. The object can still be deleted and recreated, subject to normal API and reference behavior.

Immutable objects can reduce accidental updates and API-server watch load for high-volume configurations.

## Example

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-settings-v1
  namespace: config-lab
immutable: true
data:
  LOG_LEVEL: "info"
```

## Versioned naming

A common pattern is to create a new object for each configuration revision:
- `app-settings-v1`
- `app-settings-v2`
- `app-settings-v3`

Update the Pod template to reference the new object, then roll out the workload. Keep previous versions for a controlled rollback window, then remove them after checking references.

## Trade-offs

Benefits:
- Prevents in-place drift.
- Makes configuration revisions explicit.
- Supports reproducible rollbacks.

Costs:
- More objects to manage.
- Requires deployment automation to update references.
- Old versions need retention and cleanup policies.

## Reference

- [Immutable ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/#immutable-configmaps)
- [Immutable Secrets](https://kubernetes.io/docs/concepts/configuration/secret/#immutable-secrets)
