# Lab 04 — DNS and Connectivity Troubleshooting

## Objective

Use a structured diagnostic process to separate DNS resolution from Service connectivity.

## Step 1 — Deploy demo app and Service

```bash
kubectl apply -f manifests/demo-app.yaml
kubectl apply -f manifests/clusterip-service.yaml
```

## Step 2 — Inspect DNS configuration

```bash
kubectl get pods -n kube-system
kubectl get svc -n kube-system
kubectl exec -n networking-lab deploy/demo-web -- cat /etc/resolv.conf
```

If the application image lacks `cat`, use a diagnostic Pod.

## Step 3 — Resolve service name

```bash
kubectl run dns-client -n networking-lab --rm -it --restart=Never --image=busybox:1.36 -- nslookup demo-web
kubectl run dns-client -n networking-lab --rm -it --restart=Never --image=busybox:1.36 -- nslookup kubernetes.default
```

## Step 4 — Check endpoints and ports

```bash
kubectl get svc demo-web -n networking-lab -o yaml
kubectl get endpointslices -n networking-lab -l kubernetes.io/service-name=demo-web -o yaml
kubectl describe deployment demo-web -n networking-lab
```

## Step 5 — Test HTTP

```bash
kubectl run http-client -n networking-lab --rm -it --restart=Never --image=curlimages/curl -- curl -v http://demo-web
```

Record separately: DNS result, TCP connection result, HTTP status, and application response.

## Cleanup

```bash
kubectl delete namespace networking-lab
```
