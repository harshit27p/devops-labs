# 09 — Configuration Updates and Rollout Patterns

## How update behavior differs

| Delivery method | Existing container sees update? |
|---|---|
| ConfigMap/Secret as environment variable | No; restart container/Pod |
| ConfigMap/Secret projected volume | File updates eventually, unless mounted with `subPath` |
| Application reads external secret API | Depends on client refresh/rotation logic |

A mounted file update does not guarantee the application reloads it. Confirm application behavior.

## Pattern 1: Explicit rollout

Update the ConfigMap, then restart the Deployment:

```bash
kubectl rollout restart deployment/<deployment> -n <ns>
kubectl rollout status deployment/<deployment> -n <ns>
```

## Pattern 2: Versioned object name

Create `app-settings-v2`, update the Deployment's reference, and apply both changes through the same release process. The Pod template changes, causing a controlled rollout.

## Pattern 3: Pod template checksum

A deployment tool can compute a checksum of a ConfigMap/Secret template and place it in a Pod annotation. A changed checksum updates the Pod template and triggers a rollout. Ensure secret-derived checksums do not leak information about low-entropy secret values; use a safe tool-specific mechanism.

## Rotation strategy

1. Create new credential at the upstream service.
2. Publish it through the approved secret store.
3. Roll workloads to consume the new credential.
4. Verify successful authentication.
5. Revoke the old credential.
6. Monitor for stale clients and failures.

Avoid revoking the old credential before consumers have safely transitioned unless responding to an active compromise.

## Reference

- [ConfigMap update behavior](https://kubernetes.io/docs/concepts/configuration/configmap/)
- [Secret good practices](https://kubernetes.io/docs/concepts/security/secrets-good-practices/)
