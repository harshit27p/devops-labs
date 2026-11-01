# Lab 04 — Priority and Preemption

Use only a disposable cluster. Preemption can evict workloads.

```bash
kubectl apply -f manifests/priorityclass-demo.yaml
kubectl apply -f manifests/priority-pods-demo.yaml
kubectl get pods -o wide
kubectl get events --sort-by=.lastTimestamp
```
Inspect Pod priority and scheduling events:
```bash
kubectl get pod <pod> -o jsonpath='{.spec.priority}{"\n"}'
kubectl describe pod <pod>
```
Observe behavior under constrained capacity, then clean up:
```bash
kubectl delete -f manifests/priority-pods-demo.yaml
kubectl delete -f manifests/priorityclass-demo.yaml
```
Do not use critical production priority values in a lab or assign high priority indiscriminately.
