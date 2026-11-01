# Lab 04 — Weighted Traffic and Troubleshooting

## Prerequisite

A Gateway API controller that supports HTTPRoute weighted backendRefs is installed and the Gateway is programmed.

## Step 1 — Deploy two backend versions

```bash
kubectl apply -f manifests/demo-apps.yaml
```

## Step 2 — Apply weighted route

```bash
kubectl apply -f manifests/gatewayclass-gateway.yaml
kubectl apply -f manifests/httproute-weighted.yaml
kubectl describe httproute weighted-demo -n networking-lab
```

## Step 3 — Generate requests

```bash
for i in $(seq 1 50); do
  curl -s -H 'Host: app.example.test' http://<gateway-address>/
done
```

Observe relative distribution over enough requests. A 90:10 weight is not a guarantee that every small sample will show exactly 90/10.

## Step 4 — Troubleshoot

- Check Gateway and route conditions.
- Check backendRefs names, namespaces, ports, and reference grants.
- Check Services and EndpointSlices.
- Check controller support for weighted routing.
- Inspect controller logs and metrics.

## Step 5 — Roll back

Set canary weight to zero or restore the previous route manifest.

## Cleanup

```bash
kubectl delete namespace networking-lab
```
