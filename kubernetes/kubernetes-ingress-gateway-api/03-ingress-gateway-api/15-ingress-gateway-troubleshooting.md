# 15 — Ingress and Gateway API Troubleshooting

## First identify the layer

```text
DNS -> edge/load balancer -> controller dataplane -> route resource
    -> Service -> EndpointSlice -> Pod listener
```

## Ingress checks

```bash
kubectl get ingressclass
kubectl get ingress -A -o wide
kubectl describe ingress <name> -n <ns>
kubectl get svc,endpointslices -n <ns>
kubectl get events -n <ns> --sort-by=.metadata.creationTimestamp
```

Check controller logs and status using the actual controller namespace, labels, and documentation.

## Gateway API checks

```bash
kubectl get gatewayclass
kubectl get gateway -A
kubectl describe gateway <name> -n <ns>
kubectl get httproute -A
kubectl describe httproute <name> -n <ns>
kubectl get referencegrant -A
```

Inspect status conditions:
- GatewayClass accepted by a controller.
- Gateway accepted and programmed.
- Listener accepted and programmed.
- Route accepted by parent.
- References resolved.

## Common symptoms

| Symptom | Likely causes |
|---|---|
| No address assigned | controller or infrastructure provisioning issue |
| 404 from proxy | host/path mismatch, default backend, route not attached |
| 502/503 | backend endpoints absent, wrong port, upstream connection issue |
| TLS certificate warning | wrong Secret, hostname/SAN mismatch, expired cert, SNI mismatch |
| Route not accepted | listener attachment policy, hostname mismatch, unsupported kind |
| Backend reference unresolved | wrong Service/port or cross-namespace grant missing |
| Works inside cluster only | DNS, firewall, edge load balancer, public routing |
| Intermittent failures | endpoint readiness, controller capacity, backend health, retries |

## Test host and TLS explicitly

```bash
curl -v -H 'Host: app.example.test' http://<address>/
curl --resolve app.example.test:443:<address> https://app.example.test/
openssl s_client -connect <address>:443 -servername app.example.test
```

## Debugging sequence

1. Confirm DNS points to the correct edge address.
2. Confirm controller Pods and Service are healthy.
3. Confirm route resource is accepted/programmed.
4. Confirm listener/host/path match.
5. Confirm backend Service and EndpointSlices are populated.
6. Confirm Pod listener and target port.
7. Inspect TLS Secret/certificate and SNI.
8. Inspect controller logs, Events, and metrics.
