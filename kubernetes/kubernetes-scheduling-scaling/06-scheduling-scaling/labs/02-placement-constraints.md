# Lab 02 — Placement Constraints

1. Inspect node labels:
```bash
kubectl get nodes --show-labels
```
2. In a disposable cluster, label one node:
```bash
kubectl label node <node> lab-pool=blue
```
3. Apply `manifests/node-affinity-demo.yaml` and inspect placement:
```bash
kubectl apply -f manifests/node-affinity-demo.yaml
kubectl get pod node-affinity-demo -o wide
kubectl describe pod node-affinity-demo
```
4. Remove the lab Pod and label:
```bash
kubectl delete -f manifests/node-affinity-demo.yaml
kubectl label node <node> lab-pool-
```
If no node has the required label, the Pod should remain Pending. Never modify production node labels/taints for an experiment without approval.
