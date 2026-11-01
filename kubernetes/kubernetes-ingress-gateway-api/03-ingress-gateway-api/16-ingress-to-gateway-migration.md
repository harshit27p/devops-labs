# 16 — Migrating from Ingress to Gateway API

## Why migrate?

Ingress remains stable and is not planned for removal, but its API is frozen. Gateway API is the recommended direction for new features and more expressive routing.

The community `kubernetes/ingress-nginx` controller was retired in March 2026. It no longer receives releases or security fixes. Existing deployments may continue to function, but should be reviewed and migrated to a maintained alternative.

## Migration inventory

- List all Ingress resources and IngressClasses.
- Identify controller-specific annotations.
- Inventory TLS Secrets, certificate automation, DNS records, and external addresses.
- Record rewrites, redirects, auth, rate limits, timeouts, canaries, and source IP behavior.
- Identify dependencies on controller-specific ConfigMaps or snippets.
- Confirm target controller support and Gateway API conformance.

## Mapping concepts

| Ingress | Gateway API |
|---|---|
| IngressClass | GatewayClass |
| Ingress controller entry point | Gateway |
| Ingress host/path rule | HTTPRoute |
| TLS configuration | Gateway HTTPS listener |
| Controller annotation | Standard filter or implementation-specific policy/extension |
| Cross-namespace backend (limited) | ReferenceGrant plus route/backend references |

Not every annotation has a direct standard equivalent. Some behavior may require implementation-specific policies or application changes.

## Safe migration strategy

1. Select a maintained Gateway API implementation.
2. Install supported Gateway API CRDs and controller in a test environment.
3. Translate a low-risk route and validate behavior.
4. Test host/path precedence, TLS, headers, timeouts, redirects, and client IP.
5. Run parallel entry points or staged DNS migration where architecture allows.
6. Compare logs, metrics, latency, and error rates.
7. Shift traffic gradually and maintain a rollback path.
8. Remove old resources only after validation and stakeholder sign-off.

## Do not assume a mechanical conversion is complete

A converter can generate initial Gateway API resources, but semantic differences, annotations, filters, security, and controller behavior require manual review.

## References

- [Kubernetes Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- [Ingress NGINX retirement announcement](https://kubernetes.io/blog/2025/11/11/ingress-nginx-retirement/)
- [Gateway API migration guide](https://gateway-api.sigs.k8s.io/guides/migrating-from-ingress/)
