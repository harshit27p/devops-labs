# 08 — GatewayClass and Gateway

## GatewayClass

GatewayClass defines a class of Gateways and identifies the controller responsible for managing them.

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: GatewayClass
metadata:
  name: example-gateway-class
spec:
  controllerName: example.net/gateway-controller
```

The controller name is implementation-specific. Do not apply this placeholder as if it were a real installed controller.

## Gateway

A Gateway requests an entry point with one or more listeners. A listener defines protocol, port, hostname constraints, and TLS configuration.

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: public-gateway
  namespace: networking-lab
spec:
  gatewayClassName: example-gateway-class
  listeners:
    - name: web
      protocol: HTTP
      port: 80
      allowedRoutes:
        namespaces:
          from: Same
```

## Listener concepts

- `name`: unique listener name within the Gateway.
- `protocol`: HTTP, HTTPS, TLS, TCP, or UDP depending on API support and implementation.
- `port`: listener port.
- `hostname`: optional hostname constraint.
- `tls`: certificate and TLS mode settings for secure listeners.
- `allowedRoutes`: controls which route kinds and namespaces may attach.

## Status

Inspect status conditions rather than assuming that an accepted manifest is active:

```bash
kubectl get gatewayclass
kubectl describe gatewayclass <name>
kubectl get gateway -A
kubectl describe gateway <name> -n <ns>
```

Look for conditions such as Accepted, Programmed, and listener-specific status. Exact conditions depend on API version and implementation.

## Reference

- [Gateway API specification](https://gateway-api.sigs.k8s.io/reference/spec/)
- [Gateway API guides](https://gateway-api.sigs.k8s.io/guides/)
