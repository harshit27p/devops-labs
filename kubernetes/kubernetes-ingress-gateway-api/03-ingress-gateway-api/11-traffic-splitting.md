# 11 — Traffic Splitting and Canary Releases

## Weighted backendRefs

Gateway API HTTPRoute can distribute traffic across multiple backend references using weights. Weights express relative proportions, not a guarantee that every short sample will match the exact percentage.

Example: weights 90 and 10 express a 90:10 relative distribution when both backends are healthy and the implementation supports the feature.

```yaml
backendRefs:
  - name: app-stable
    port: 80
    weight: 90
  - name: app-canary
    port: 80
    weight: 10
```

See [`manifests/httproute-weighted.yaml`](manifests/httproute-weighted.yaml).

## Canary workflow

1. Deploy a stable version and a canary version as separate Services.
2. Route a small percentage to canary.
3. Observe error rate, latency, saturation, and business metrics.
4. Increase canary weight gradually if healthy.
5. Roll back by setting canary weight to zero or reverting the route.
6. Remove old workloads only after validation and rollback window.

## Important limitations

- Weighting is not the same as user/session affinity.
- Request distribution can vary due to connection reuse, retries, and implementation behavior.
- Backend health and failure handling are controller-specific.
- Database schema and message format compatibility must be planned separately.

## Ingress comparison

Ingress has no portable standard weighted backend mechanism. Weighted canaries have often depended on controller-specific annotations. Gateway API provides a standard route model for weighted backends where supported.

## Reference

- [Gateway API HTTPRoute](https://gateway-api.sigs.k8s.io/api-types/httproute/)
