# 14 — Ingress and Gateway Security

## Threat model

The edge routing layer is exposed to untrusted clients and often has access to many internal Services. Treat it as a security boundary.

## Controls

- Expose only intended hosts, paths, and ports.
- Enforce TLS and define a certificate renewal process.
- Apply authentication and authorization at the appropriate gateway/application layer.
- Restrict controller ServiceAccounts and RBAC.
- Avoid granting tenants unrestricted ability to create routes that attach to shared public Gateways.
- Use Gateway `allowedRoutes` and ReferenceGrant to control delegation.
- Apply NetworkPolicy to restrict controller-to-backend traffic where supported.
- Set request size, timeout, rate-limit, and connection limits using supported implementation features.
- Sanitize forwarded headers at the trusted edge.
- Keep controller images and dependencies patched.

## Multi-tenant considerations

Gateway API's role-oriented model can delegate route creation while keeping listener and infrastructure control with platform operators. Review namespace attachment policies and backend reference permissions carefully.

## Secrets

TLS private keys are sensitive. Limit read access to the Gateway/controller components that need them, enable encryption at rest for the cluster's secret store, and use a managed certificate lifecycle.

## Logging and privacy

Avoid logging authorization headers, cookies, tokens, and personal data. Define retention and access controls for access logs.

## Reference

- [Gateway API security model](https://gateway-api.sigs.k8s.io/guides/)
- [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
