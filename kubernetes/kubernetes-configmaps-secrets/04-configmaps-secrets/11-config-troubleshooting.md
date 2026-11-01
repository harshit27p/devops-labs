# 11 — ConfigMap and Secret Troubleshooting

## Start with object existence and namespace

ConfigMaps and Secrets are namespaced. A Pod can reference only objects in its own namespace.

```bash
kubectl get configmap,secret -n <ns>
kubectl describe pod <pod> -n <ns>
kubectl get events -n <ns> --sort-by=.metadata.creationTimestamp
```

## Common symptoms

| Symptom | Likely cause |
|---|---|
| `CreateContainerConfigError` | Missing object or key, invalid reference |
| Pod stuck during volume setup | Missing Secret/ConfigMap, mount or projection issue |
| App uses old environment value | Environment captured at process start |
| Mounted file remains stale | `subPath`, propagation delay, wrong mount |
| App cannot read mounted file | File mode, UID/GID, path, read-only filesystem |
| Secret access denied | RBAC or external provider identity |
| New Secret value not active | Workload not restarted or app did not reload file |

## Safe inspection

```bash
kubectl describe configmap <name> -n <ns>
kubectl describe secret <name> -n <ns>
kubectl get pod <pod> -n <ns> -o yaml
```

Avoid printing Secret contents. Verify key names and metadata without decoding values.

## Check a specific key without exposing its value

```bash
kubectl get secret app-credentials -n <ns> \
  -o go-template='{{if index .data "password"}}key-present{{else}}key-missing{{end}}{{"\n"}}'
```

## Verify RBAC

```bash
kubectl auth can-i get secrets -n <ns> --as=system:serviceaccount:<ns>:<service-account>
kubectl auth can-i list secrets -n <ns> --as=system:serviceaccount:<ns>:<service-account>
```

Use an authorized administrator account for impersonation checks.

## Recovery sequence

1. Confirm context and namespace.
2. Verify object name and key names.
3. Check Pod Events and container status.
4. Confirm volume mount path and permissions.
5. Determine whether environment injection requires a restart.
6. Confirm RBAC and provider identity.
7. Rotate credentials if exposure is suspected; do not merely recreate the same leaked value.
