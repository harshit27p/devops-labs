# 05 — NodePort Services

## Purpose

NodePort exposes a Service on a port across cluster nodes. The default allocated port range is commonly `30000-32767`, but clusters can configure a different range.

A NodePort is useful for learning, development, or specific infrastructure patterns. For production public traffic, a cloud LoadBalancer or an HTTP routing layer is often a better fit.

## Example

See [`manifests/nodeport-service.yaml`](manifests/nodeport-service.yaml).

```bash
kubectl get svc demo-web-nodeport -n networking-lab
kubectl get nodes -o wide
```

Access the NodePort through a reachable node address and the assigned port, subject to node firewall, routing, and dataplane configuration.

## Important details

- `nodePort` can be explicitly specified if it is within the configured range and not already allocated.
- `externalTrafficPolicy: Cluster` can forward traffic to endpoints on other nodes; source IP may be obscured by forwarding/NAT behavior.
- `externalTrafficPolicy: Local` routes external traffic only to local node endpoints and can preserve the client source IP, but nodes without local endpoints may not serve traffic.
- Health checks and load balancer behavior vary by environment.

## Security considerations

Do not expose administrative or sensitive services through NodePort without explicit network controls. Restrict node firewall access and use TLS/authentication at the application or gateway layer.

## Reference

- [Service types](https://kubernetes.io/docs/concepts/services-networking/service/#type-nodeport)
