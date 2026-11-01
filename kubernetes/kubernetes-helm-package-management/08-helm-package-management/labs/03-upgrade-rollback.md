# Lab 03 — Upgrade, Rollback, and History

Install:
```bash
helm upgrade --install web charts/platform-web -n helm-lab --create-namespace --set replicaCount=2
```

Upgrade:
```bash
helm upgrade web charts/platform-web -n helm-lab --set replicaCount=3
helm history web -n helm-lab
helm status web -n helm-lab
```

Rollback to a previous revision:
```bash
helm rollback web 1 -n helm-lab --wait
```

Inspect the resulting Deployment replica count and release history. Remember rollback restores Helm-managed Kubernetes resource definitions; it cannot undo database or external-system side effects.

Cleanup:
```bash
helm uninstall web -n helm-lab
kubectl delete namespace helm-lab
```
