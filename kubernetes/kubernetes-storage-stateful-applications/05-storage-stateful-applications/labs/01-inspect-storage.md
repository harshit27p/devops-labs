# Lab 01 — Inspect Storage Capabilities

```bash
kubectl version
kubectl get nodes -o wide
kubectl get storageclass
kubectl get pv
kubectl get pvc -A
kubectl get csidrivers
kubectl get csinodes
kubectl api-resources | grep -i snapshot
```
Record the default class, provisioner, binding mode, reclaim policy, expansion support, CSI drivers, and snapshot availability. Do not create/delete cluster-wide storage resources without authorization.
