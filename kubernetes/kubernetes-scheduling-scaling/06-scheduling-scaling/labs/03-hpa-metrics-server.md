# Lab 03 — HPA with Metrics Server

Prerequisites: Metrics Server (or compatible Metrics API) installed, resource requests on the target container, and a test cluster.

```bash
kubectl apply -f manifests/hpa-demo.yaml
kubectl get deploy,hpa,pods
kubectl get apiservices | grep metrics
kubectl top pods
```
Generate load only in a disposable environment using an approved load generator. Observe:
```bash
kubectl get hpa -w
kubectl describe hpa web-demo-hpa
kubectl get pods -l app=hpa-web -w
```
If metrics are unavailable, troubleshoot Metrics API and requests before changing HPA thresholds. Clean up:
```bash
kubectl delete -f manifests/hpa-demo.yaml
```
