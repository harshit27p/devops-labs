# 12 — TLS with Gateway API

## HTTPS listener

A Gateway HTTPS listener uses TLS configuration and references certificate material through a Secret reference. Commonly the certificate Secret is in the Gateway's namespace; cross-namespace references have additional constraints and permissions.

```yaml
listeners:
  - name: https
    protocol: HTTPS
    port: 443
    hostname: app.example.test
    tls:
      mode: Terminate
      certificateRefs:
        - kind: Secret
          name: app-example-tls
```

## TLS modes

- `Terminate`: TLS is terminated at the Gateway and HTTP routing can inspect the request.
- `Passthrough`: TLS is passed through without termination at the Gateway; support depends on listener protocol and implementation.

## Certificate lifecycle

Use cert-manager or an external PKI workflow to issue, renew, and distribute certificates. Restrict Secret access, monitor expiry, and test renewal before production rollout.

## Verify

```bash
kubectl describe gateway <gateway> -n <ns>
kubectl get secret app-example-tls -n <ns>
openssl s_client -connect <address>:443 -servername app.example.test
```

## Reference

- [Gateway API TLS](https://gateway-api.sigs.k8s.io/guides/tls/)
