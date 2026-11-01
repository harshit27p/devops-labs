# Lab 01 — Service Discovery with ClusterIP

## Objective

Deploy a web workload and access it through a stable Service DNS name.

## Step 1 — Verify context

```bash
kubectl config current-context
kubectl get nodes
```

## Step 2 — Deploy application and Service

```bash
kubectl apply -f manifests/demo-app.yaml
kubectl apply -f manifests/clusterip-service.yaml
kubectl get deploy,pods,svc -n networking-lab -o wide
kubectl get endpointslices -n networking-lab -l kubernetes.io/service-name=demo-web
```

## Step 3 — Test by DNS

```bash
kubectl run client -n networking-lab --rm -it --restart=Never --image=curlimages/curl -- curl -sS http://demo-web
```

If your cluster cannot pull that image, use an approved image that includes curl.

## Step 4 — Scale the workload

```bash
kubectl scale deployment/demo-web --replicas=4 -n networking-lab
kubectl get pods -n networking-lab -o wide
kubectl get endpointslices -n networking-lab -l kubernetes.io/service-name=demo-web
```

Observe that the Service name and ClusterIP remain stable while the backend endpoint set changes.

## Step 5 — Cleanup

```bash
kubectl delete namespace networking-lab
```
