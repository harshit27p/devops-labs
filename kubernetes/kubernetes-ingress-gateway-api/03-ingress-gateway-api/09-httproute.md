# 09 — HTTPRoute

## Purpose

HTTPRoute defines HTTP routing rules and attaches them to a Gateway through `parentRefs`. It can match hostnames, paths, headers, and query parameters, then direct traffic to one or more backend references.

## Example

See [`manifests/httproute.yaml`](manifests/httproute.yaml).

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: app-route
  namespace: networking-lab
spec:
  parentRefs:
    - name: public-gateway
  hostnames:
    - app.example.test
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /api
      backendRefs:
        - name: api-service
          port: 8080
```

## Attachment

A route attaches to a Gateway listener only when parent reference, namespace policy, route kind, hostname, and listener constraints permit it. Cross-namespace attachment is controlled by Gateway listener `allowedRoutes`; backend references across namespaces require explicit authorization through ReferenceGrant.

## Matches

HTTPRoute supports match types such as:
- Exact path.
- PathPrefix.
- RegularExpression (implementation support may vary).
- Header matches.
- Query parameter matches.

When multiple rules or matches exist, precedence is defined by Gateway API; check the specification for detailed tie-breaking rules.

## Filters

Filters modify or redirect requests/responses, for example URL rewrite, request redirect, header modification, or extension-specific behavior. Not every implementation supports every filter or feature.

## Troubleshooting

```bash
kubectl get httproute -A
kubectl describe httproute <route> -n <ns>
kubectl get gateway <gateway> -n <ns> -o yaml
```

Inspect route status conditions and parent status, including Accepted and ResolvedRefs.

## Reference

- [HTTPRoute](https://gateway-api.sigs.k8s.io/api-types/httproute/)
