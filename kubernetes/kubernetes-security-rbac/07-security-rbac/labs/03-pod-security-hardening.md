# Lab 03 — Pod Security Hardening

```bash
kubectl apply -f manifests/hardened-pod.yaml
kubectl get pod hardened-demo -n security-lab
kubectl describe pod hardened-demo -n security-lab
kubectl exec -n security-lab hardened-demo -- id
kubectl exec -n security-lab hardened-demo -- sh -c 'touch /tmp/test-file'
```
The example runs as non-root, drops capabilities, disables privilege escalation, and uses a read-only root filesystem with a writable temporary volume. Validate behavior in your runtime; images may need adjustment to run non-root.

Cleanup:
```bash
kubectl delete -f manifests/hardened-pod.yaml
```
