# Kubernetes Ingress & Gateway API

Advanced notes for north-south HTTP(S) traffic routing into Kubernetes workloads. Covers the stable Ingress API, controller architecture, TLS, Gateway API resources, traffic policy, migration, and operations.

> Prerequisites: [00 Architecture](../00-architecture-fundamentals/README.md), [01 Workloads](../01-kubernetes-workloads/README.md), and [02 Networking & Services](../02-networking-services/README.md).

## Important ecosystem note

Kubernetes Ingress is stable but frozen: it remains supported as an API, but no new features are planned. Kubernetes recommends Gateway API for new capabilities. The community `kubernetes/ingress-nginx` controller was retired in March 2026; do not select it for a new production deployment. Existing installations may continue to run, but should be assessed and migrated. See the official [Ingress documentation](https://kubernetes.io/docs/concepts/services-networking/ingress/) and [retirement announcement](https://kubernetes.io/blog/2025/11/11/ingress-nginx-retirement/).

## Learning outcomes

- Explain the difference between an Ingress resource and an Ingress controller.
- Configure host-based, path-based, and TLS routing.
- Understand IngressClass and controller-specific behavior.
- Understand Gateway API's GatewayClass, Gateway, HTTPRoute, listeners, and parent references.
- Configure route attachment, backend references, filters, and traffic weights.
- Understand certificate management, security boundaries, observability, and migration planning.

## Module map

| File | Coverage |
|---|---|
| [01 Ingress fundamentals](01-ingress-fundamentals.md) | API model, controller, lifecycle |
| [02 IngressClass](02-ingressclass-controller.md) | Class selection and controller responsibility |
| [03 Host routing](03-host-based-routing.md) | Virtual hosts and DNS |
| [04 Path routing](04-path-based-routing.md) | Prefix, Exact, ImplementationSpecific |
| [05 TLS](05-ingress-tls.md) | TLS termination and Secret references |
| [06 Controller architecture](06-ingress-controller-architecture.md) | Proxy dataplane, reconciliation |
| [07 Gateway API overview](07-gateway-api-overview.md) | Design, roles, resources |
| [08 GatewayClass and Gateway](08-gatewayclass-gateway.md) | Infrastructure and listeners |
| [09 HTTPRoute](09-httproute.md) | Host/path/header matching and backendRefs |
| [10 Filters](10-gateway-api-filters.md) | Redirect, rewrite, headers |
| [11 Traffic splitting](11-traffic-splitting.md) | Weighted backends and canary patterns |
| [12 TLS with Gateway API](12-gateway-api-tls.md) | Listener certificates and termination |
| [13 cert-manager](13-cert-manager.md) | Certificate automation |
| [14 Security](14-ingress-gateway-security.md) | Exposure, RBAC, policy, trust boundaries |
| [15 Troubleshooting](15-ingress-gateway-troubleshooting.md) | Layered diagnosis |
| [16 Migration](16-ingress-to-gateway-migration.md) | Ingress migration and controller retirement |
| [17 Production patterns](17-production-routing-patterns.md) | Architecture and operations |

## Labs

1. [Ingress host and path routing](labs/01-ingress-host-path-routing.md)
2. [Gateway API HTTPRoute](labs/02-gateway-api-httproute.md)
3. [TLS termination](labs/03-tls-termination.md)
4. [Traffic splitting and troubleshooting](labs/04-traffic-splitting-troubleshooting.md)

## Manifests

- `manifests/demo-apps.yaml`
- `manifests/ingress-host-path.yaml`
- `manifests/gatewayclass-gateway.yaml`
- `manifests/httproute.yaml`
- `manifests/httproute-weighted.yaml`
- `manifests/ingress-tls.yaml`

## Before you run the labs

Gateway API CRDs and a compatible controller are separate prerequisites. Installing CRDs only makes API resources available; it does not provide a dataplane. The exact installation procedure depends on the selected implementation and its supported Gateway API release channel. Check controller documentation and conformance before applying examples.

For Ingress, install and operate a currently maintained controller. Do not use the retired community `ingress-nginx` controller for new deployments. Ingress controller implementations differ in supported annotations and behavior.

## Quick inspection

```bash
kubectl config current-context
kubectl get ingressclass
kubectl get ingress -A
kubectl get gatewayclass
kubectl get gateways -A
kubectl get httproutes -A
kubectl get svc -A
```

## Official references

- [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- [Ingress controllers](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/)
- [Gateway API introduction](https://gateway-api.sigs.k8s.io/docs/introduction/)
- [Gateway API guides](https://gateway-api.sigs.k8s.io/guides/)
- [Gateway API reference](https://gateway-api.sigs.k8s.io/reference/spec/)
- [cert-manager documentation](https://cert-manager.io/docs/)
