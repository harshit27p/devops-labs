# 07 — Gateway API Overview

## What is Gateway API?

Gateway API is a Kubernetes project for expressive L4 and L7 routing. It provides role-oriented resources that separate infrastructure provisioning, listener configuration, and application route attachment.

Gateway API is not a controller. A compatible implementation must be installed to program a data plane.

## Role-oriented model

- Infrastructure provider / platform team: provides GatewayClass and implementation.
- Cluster operator: creates or manages Gateway resources and listeners.
- Application developer: creates routes such as HTTPRoute and requests attachment to a Gateway.

This separation supports multi-team clusters and controlled delegation.

## Core resources

| Resource | Purpose |
|---|---|
| GatewayClass | Defines a class of Gateways handled by a controller |
| Gateway | Requests listeners and infrastructure for a traffic entry point |
| HTTPRoute | Defines HTTP matches, filters, and backend references |
| GRPCRoute | gRPC routing |
| TLSRoute | TLS passthrough routing where supported |
| ReferenceGrant | Allows selected cross-namespace references |

Resource support varies by implementation and Gateway API release channel. Check conformance and feature support.

## Why Gateway API?

Compared with the compact Ingress API, Gateway API provides:
- More expressive matching and filters.
- Clearer role separation.
- Cross-namespace delegation with explicit permission.
- Weighted backend references for traffic splitting.
- Multiple protocol-specific route kinds.
- A standard extension model and conformance program.

## Ingress is not being removed

Ingress remains a stable API and there are no plans to remove it. It is frozen, while Gateway API is the recommended direction for new features. Existing Ingress controllers may continue supporting Ingress.

## References

- [Gateway API introduction](https://gateway-api.sigs.k8s.io/docs/introduction/)
- [Gateway API FAQ](https://gateway-api.sigs.k8s.io/docs/faq/)
