# Lab 02 — ServiceAccount Identity

```bash
kubectl apply -f manifests/serviceaccount-no-token.yaml
kubectl get serviceaccount app-no-api -n security-lab
kubectl get pod sa-no-api-demo -n security-lab -o yaml
kubectl exec -n security-lab sa-no-api-demo -- sh -c 'ls -la /var/run/secrets/kubernetes.io/serviceaccount 2>/dev/null || true'
```
The Pod explicitly disables automatic token mounting. Do not enable API access unless required; if required, add a narrowly scoped Role/RoleBinding and use supported projected tokens.

Cleanup:
```bash
kubectl delete -f manifests/serviceaccount-no-token.yaml
```
