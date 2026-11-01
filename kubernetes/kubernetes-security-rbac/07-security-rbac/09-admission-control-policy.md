# 09 — Admission Control and Policy Enforcement

Admission runs after authentication and authorization and before an API object is persisted. Admission controllers can validate or mutate API requests.

## Types
- **Mutating admission:** changes an incoming object, for example injecting defaults or sidecars.
- **Validating admission:** accepts or rejects an object based on policy.
- **Built-in admission plugins:** enabled/configured by the API server.
- **Admission webhooks:** external services called by the API server.
- **ValidatingAdmissionPolicy:** declarative CEL-based validation, subject to Kubernetes version and API availability.

## Common policy use cases
- Require approved registries.
- Require resource requests and limits.
- Reject privileged containers.
- Require labels/annotations.
- Enforce approved ServiceAccount usage.
- Restrict hostPath, host namespaces, or unsafe capabilities.

## Webhook reliability
Admission webhooks are on the API request path. Configure timeouts, TLS, service availability, and `failurePolicy` carefully. A failing webhook with fail-closed behavior can block API operations; fail-open behavior can permit policy bypass.

## Inspect
```bash
kubectl get validatingwebhookconfigurations
kubectl get mutatingwebhookconfigurations
kubectl get validatingadmissionpolicies
```
Availability of ValidatingAdmissionPolicy resources depends on cluster version and feature support.
