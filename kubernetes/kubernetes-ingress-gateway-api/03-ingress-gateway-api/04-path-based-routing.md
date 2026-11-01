# 04 — Path-Based Routing

## Concept

Path routing directs requests to different Services based on URI path. A common design routes `/api` to an API Service and `/` to a frontend Service.

## Ingress path types

- `Exact`: exact path match.
- `Prefix`: path element prefix match; `/api` matches `/api` and `/api/v1`, but not `/apix`.
- `ImplementationSpecific`: matching behavior is defined by the selected controller.

Prefer `Prefix` or `Exact` for portable manifests. Do not assume regular-expression behavior is portable across controllers.

## Example

```yaml
paths:
  - path: /api
    pathType: Prefix
    backend:
      service:
        name: api
        port:
          number: 8080
  - path: /
    pathType: Prefix
    backend:
      service:
        name: frontend
        port:
          number: 80
```

The API backend may receive the original `/api/...` path. Path rewriting is not a portable core Ingress feature; it is commonly controller-specific or expressed with Gateway API filters where supported.

## Common mistakes

- Assuming `/api` is rewritten to `/`.
- Using `ImplementationSpecific` without checking controller documentation.
- Overlapping paths and misunderstanding precedence.
- Mismatched Service port and backend listener.
- Testing without the correct Host header.

## Reference

- [Ingress path types](https://kubernetes.io/docs/concepts/services-networking/ingress/#path-types)
