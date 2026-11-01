# 06 — Release Lifecycle and Upgrade Strategies

## Install
```bash
helm install web ./charts/platform-web -n demo --create-namespace
```

## Upgrade or install idempotently
```bash
helm upgrade --install web ./charts/platform-web   -n demo --create-namespace   --wait --timeout 5m
```

## Inspect release
```bash
helm list -n demo
helm status web -n demo
helm history web -n demo
helm get manifest web -n demo
helm get values web -n demo
```

## Rollback
```bash
helm rollback web <revision> -n demo --wait
```
Rollback reapplies a previous release's rendered resources; it does not reverse database migrations, external API side effects, or data changes.

## Uninstall
```bash
helm uninstall web -n demo
```
Kubernetes resources with retention policies, PVCs, or external resources may not be deleted as operators expect. Review chart annotations and resource policies before uninstalling.

## Upgrade safety
- Review rendered diff before deployment.
- Use `--atomic` only when its rollback behavior is appropriate.
- Use `--wait` with a realistic timeout.
- Coordinate schema/database migrations separately.
- Test backward/forward compatibility.
- Keep release history according to operational policy.
