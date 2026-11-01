# Lab 01 — RBAC Least Privilege

Create a namespace-scoped read-only identity:
```bash
kubectl apply -f manifests/rbac-reader.yaml
kubectl auth can-i get pods -n security-lab --as=system:serviceaccount:security-lab:pod-reader
kubectl auth can-i delete pods -n security-lab --as=system:serviceaccount:security-lab:pod-reader
kubectl auth can-i get secrets -n security-lab --as=system:serviceaccount:security-lab:pod-reader
```
Expected: get/list/watch Pods allowed; delete Pods and reading Secrets denied. The invoking administrator needs impersonation permission for `--as`.

Cleanup:
```bash
kubectl delete -f manifests/rbac-reader.yaml
```
