# 12 — Service Design Patterns and Selection

## Choose by traffic requirement

| Need | Pattern |
|---|---|
| Internal communication to changing Pods | ClusterIP |
| Direct node-port access for lab or controlled network | NodePort |
| External L4 load balancer | LoadBalancer |
| HTTP host/path routing to many services | Ingress or Gateway API |
| Stable per-Pod DNS discovery | Headless Service |
| DNS alias for an external dependency | ExternalName |
| Manually managed backend addresses | Selectorless Service + EndpointSlices |

## Common architecture

A typical application path may look like:

```text
External client
   |
Cloud LoadBalancer
   |
Ingress / Gateway controller
   |
ClusterIP Service
   |
Ready Pod endpoints
```

Ingress/Gateway behavior is intentionally documented in the next external-routing module.

## Production principles

- Prefer DNS names over hardcoded ClusterIPs and Pod IPs.
- Use readiness probes so unready Pods are not advertised as ready endpoints.
- Use NetworkPolicy for least-privilege Pod traffic where supported.
- Avoid exposing internal services publicly without a business requirement.
- Understand client source IP behavior and health checks.
- Monitor DNS latency, endpoint count, connection errors, and CNI health.
- Plan CIDRs to avoid overlap with VPCs, VPNs, and connected networks.
- Test failover and node drain behavior, not only the happy path.

## Interview quick checks

- Why does a Service need a selector?
- What is the difference between `port`, `targetPort`, and `nodePort`?
- What is an EndpointSlice?
- Why can DNS work while a TCP connection fails?
- Why might a NetworkPolicy have no effect?
- Compare ClusterIP, NodePort, and LoadBalancer.
