# 03 — Host-Based Routing

## Concept

Host-based routing selects a backend based on the HTTP Host header (or TLS SNI during TLS negotiation, depending on the listener and implementation). Multiple applications can share one external address while using distinct DNS names.

Example:
- `shop.example.test` -> shop Service
- `api.example.test` -> API Service
- `docs.example.test` -> documentation Service

## Ingress rule example

```yaml
spec:
  rules:
    - host: shop.example.test
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: shop
                port:
                  number: 80
    - host: api.example.test
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: api
                port:
                  number: 8080
```

## DNS

The hostnames must resolve to the address used by the ingress data plane. In a lab, a hosts-file entry can be used; in production, configure authoritative DNS and appropriate TTLs.

## Testing

```bash
curl -H 'Host: shop.example.test' http://<ingress-address>/
curl -H 'Host: api.example.test' http://<ingress-address>/
```

For HTTPS, test SNI and certificate hostname matching:

```bash
curl --resolve shop.example.test:443:<ingress-address> https://shop.example.test/
```

## Troubleshooting

- DNS points to wrong address.
- Host header does not match rule.
- TLS SNI/certificate hostname mismatch.
- Wrong IngressClass or controller.
- Backend Service has no ready endpoints.

## Reference

- [Ingress rules](https://kubernetes.io/docs/concepts/services-networking/ingress/#name-based-virtual-hosting)
