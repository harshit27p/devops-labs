# Lab 02 — Create and Use a PVC

Prerequisite: a working default StorageClass. If none exists, use an administrator-approved class; do not guess a provisioner.

```bash
kubectl apply -f manifests/pvc-basic.yaml
kubectl apply -f manifests/pod-using-pvc.yaml
kubectl get pvc -w
kubectl get pods -w
kubectl exec storage-writer -- sh -c 'date > /data/proof.txt'
kubectl exec storage-writer -- cat /data/proof.txt
kubectl delete pod storage-writer
kubectl apply -f manifests/pod-using-pvc.yaml
kubectl wait --for=condition=Ready pod/storage-writer --timeout=120s
kubectl exec storage-writer -- cat /data/proof.txt
```
The file should remain when the same PVC/backend volume is reused. Before cleanup, inspect reclaim policy:
```bash
kubectl delete -f manifests/pod-using-pvc.yaml
kubectl delete -f manifests/pvc-basic.yaml
```
Only delete disposable lab data.
