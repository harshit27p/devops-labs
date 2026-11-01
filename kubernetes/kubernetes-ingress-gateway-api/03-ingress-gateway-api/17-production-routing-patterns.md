# 17 — Production Routing Patterns

## Pattern 1: Shared edge Gateway

A platform team manages one or more Gateways. Application teams attach HTTPRoutes from their namespaces, subject to listener `allowedRoutes` and reference permissions.

Benefits:
- Centralized infrastructure ownership.
- Consistent TLS and edge policy.
- Namespace-level application autonomy.
- Reduced proliferation of external load balancers.

Risks:
- Shared failure domain and capacity.
- Need for clear ownership and quota boundaries.
- Route attachment must be tightly controlled.

## Pattern 2: Separate internal and external Gateways

Use distinct Gateways/listeners or controller classes for internal and public traffic. Ensure DNS, load balancer scheme, firewall, and allowed route namespaces align with the intended trust boundary.

## Pattern 3: Canary release

Use weighted HTTPRoute backendRefs when supported. Monitor service-level indicators and business outcomes; shift traffic gradually and preserve rollback capability.

## Pattern 4: TLS at the edge

Terminate TLS at Gateway and forward to Services. For sensitive environments, consider TLS re-encryption or end-to-end encryption, depending on implementation and threat model.

## Reliability checklist

- [ ] Controller is maintained and version-compatible.
- [ ] GatewayClass/Gateway/listeners are accepted and programmed.
- [ ] Multiple replicas and disruption strategy are configured where appropriate.
- [ ] External load balancer health checks are understood.
- [ ] Certificates renew automatically and expiry is monitored.
- [ ] DNS TTL and cutover process are documented.
- [ ] Backend readiness and graceful shutdown are configured.
- [ ] Timeouts, retries, and request limits are intentional.
- [ ] Access logs and metrics are available without leaking secrets.
- [ ] Route delegation and cross-namespace references are restricted.
- [ ] Migration and rollback are tested.

## Interview quick checks

1. Why does creating an Ingress resource alone not expose an application?
2. Compare Ingress and Gateway API.
3. Explain GatewayClass, Gateway, and HTTPRoute.
4. How does a route attach to a listener?
5. What does ReferenceGrant authorize?
6. How do weighted backendRefs support canary deployment?
7. How would you diagnose a Gateway that is accepted but not programmed?
