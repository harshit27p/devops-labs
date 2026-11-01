# Lab 02 — Gateway API HTTPRoute

## Prerequisites

A Gateway API-compatible controller and the Gateway API CRDs it supports must already be installed. Use the controller's official installation guide and version matrix. CRDs alone do not create a routing dataplane.

## Step 1 — Verify API resources

```bash
kubectl api-resources | grep -E 'gatewayclass|gateways|httproutes'
kubectl get gatewayclass
```

## Step 2 — Create demo applications

```bash
kubectl apply -f manifests/demo-apps.yaml
```

## Step 3 — Configure GatewayClass

Edit `manifests/gatewayclass-gateway.yaml` and replace the example controller name with the controller's documented name. If the platform team already created a GatewayClass, reuse it rather than creating a duplicate.

## Step 4 — Apply Gateway and HTTPRoute

```bash
kubectl apply -f manifests/gatewayclass-gateway.yaml
kubectl apply -f manifests/httproute.yaml
kubectl get gateway -n networking-lab
kubectl get httproute -n networking-lab
kubectl describe gateway public-gateway -n networking-lab
kubectl describe httproute demo-route -n networking-lab
```

## Step 5 — Inspect conditions

Confirm the Gateway is accepted/programmed and the HTTPRoute is accepted with references resolved. A resource existing in the API does not prove the controller programmed traffic.

## Step 6 — Test

Use the Gateway address and correct Host header:

```bash
curl -H 'Host: app.example.test' http://<gateway-address>/
```

## Cleanup

```bash
kubectl delete namespace networking-lab
```
