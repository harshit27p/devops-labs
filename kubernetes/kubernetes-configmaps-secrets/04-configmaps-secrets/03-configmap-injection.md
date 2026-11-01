# 03 — Injecting ConfigMaps into Containers

## Individual environment variables

```yaml
env:
  - name: LOG_LEVEL
    valueFrom:
      configMapKeyRef:
        name: app-settings
        key: LOG_LEVEL
```

This makes the mapping explicit and documents which keys the application requires.

## Bulk environment import

```yaml
envFrom:
  - configMapRef:
      name: app-settings
```

`envFrom` imports all eligible keys. Use `prefix` when needed to avoid collisions. Explicit `env` entries are preferable when the application requires a small, known set of values.

## Optional references

`optional: true` allows a Pod to start if the referenced ConfigMap or key is absent. Use this only when the application has a safe default. For required configuration, fail clearly rather than silently starting with unintended values.

## Update behavior

Environment variables are established when the container process starts. Updating a ConfigMap does not modify the environment of an already-running process. Restart or roll out Pods to consume updated environment values.

## Example

See [`manifests/configmap-env-deployment.yaml`](manifests/configmap-env-deployment.yaml).

## Inspect

```bash
kubectl describe pod <pod> -n <ns>
kubectl exec <pod> -n <ns> -- printenv | grep '^APP_'
```

Do not use broad environment dumps in production troubleshooting; they may expose credentials injected by other mechanisms.

## Reference

- [Configure a Pod to use a ConfigMap](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/)
