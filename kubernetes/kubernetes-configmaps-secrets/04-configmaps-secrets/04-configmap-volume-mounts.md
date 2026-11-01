# 04 — ConfigMap Volume Mounts

## Mount configuration as files

A ConfigMap volume exposes keys as files. This is useful when applications expect configuration files such as `application.yaml`, `nginx.conf`, or logging configuration.

```yaml
volumes:
  - name: app-config
    configMap:
      name: app-settings
containers:
  - name: app
    image: example.invalid/app:1.0
    volumeMounts:
      - name: app-config
        mountPath: /etc/app/config
        readOnly: true
```

The placeholder image is not intended to be run; adapt it to your application.

## Project selected keys

Use `items` to map only selected keys and choose file paths. This reduces accidental exposure of unrelated settings to a container.

## Update propagation

Mounted ConfigMap volumes are updated eventually after the ConfigMap changes. The delay depends on kubelet synchronization and cache propagation. The application must detect and reload the changed file; Kubernetes does not automatically restart the process.

## `subPath` caveat

A ConfigMap mounted using `subPath` does not receive updates when the ConfigMap changes. Avoid `subPath` when the application depends on live projected updates.

## Rollout pattern

For deterministic deployments, use a versioned ConfigMap name or a Pod template checksum annotation so a configuration change triggers a Deployment rollout. See the configuration update guide.

## Reference

- [ConfigMap volume updates](https://kubernetes.io/docs/concepts/configuration/configmap/#mounted-configmaps-are-updated-automatically)
