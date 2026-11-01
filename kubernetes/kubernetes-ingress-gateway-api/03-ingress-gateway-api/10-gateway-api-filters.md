# 10 — Gateway API Filters

## Purpose

HTTPRoute filters modify request handling. Common standard filters include request redirects, URL rewrites, and request/response header modification. Filter availability and support level vary by Gateway API release and implementation.

## Request redirect

A redirect returns a response instructing the client to request another URL. It does not proxy the original request to the backend.

## URL rewrite

A rewrite changes the request path or hostname before forwarding to the backend. This is useful when a public route prefix differs from the backend's expected URI structure.

## Header modification

Request headers can be added, set, or removed; response header modification may also be supported. Be careful not to overwrite security-sensitive headers such as authentication or forwarding metadata without a deliberate trust model.

## Example pattern

```yaml
filters:
  - type: RequestRedirect
    requestRedirect:
      scheme: https
      statusCode: 301
```

Use this inside an HTTPRoute rule's `filters` list and verify the selected implementation supports the filter.

## Best practices

- Keep redirects deterministic and avoid loops.
- Do not trust client-supplied forwarding headers unless the edge proxy sanitizes them.
- Avoid leaking internal hostnames or paths.
- Test both direct backend and externally routed behavior.
- Review filter support and conformance for the deployed controller.

## Reference

- [Gateway API HTTPRoute filters](https://gateway-api.sigs.k8s.io/guides/http-redirect-rewrite/)
