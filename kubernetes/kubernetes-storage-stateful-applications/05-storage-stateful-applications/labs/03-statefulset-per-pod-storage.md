# Lab 03 — StatefulSet Per-Pod Storage

```bash
kubectl apply -f manifests/statefulset-with-pvc.yaml
kubectl get pods -l app=stateful-demo -w
kubectl get pvc
kubectl exec stateful-demo-0 -- sh -c 'echo replica-0 > /data/identity.txt'
kubectl exec stateful-demo-1 -- sh -c 'echo replica-1 > /data/identity.txt'
kubectl exec stateful-demo-0 -- cat /data/identity.txt
kubectl exec stateful-demo-1 -- cat /data/identity.txt
kubectl scale statefulset stateful-demo --replicas=3
kubectl get pods
kubectl get pvc
```
Claims are distinct per ordinal. Delete the StatefulSet, inspect remaining PVCs, and only remove claims if lab data is disposable and reclaim behavior is understood.
