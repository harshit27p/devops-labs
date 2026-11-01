# Lab 02 — Package and Deploy the Sample Chart

```bash
helm lint charts/platform-web
helm package charts/platform-web --destination dist/
helm install web dist/platform-web-0.1.0.tgz -n helm-lab --create-namespace --wait
helm list -n helm-lab
helm status web -n helm-lab
kubectl get all -n helm-lab
```

If the selected image is unavailable or blocked, update the chart values to an approved image. If Ingress is enabled, install a compatible controller and set the correct class/host.

Cleanup:
```bash
helm uninstall web -n helm-lab
kubectl delete namespace helm-lab
```
