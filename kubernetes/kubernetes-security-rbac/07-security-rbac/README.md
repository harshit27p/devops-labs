# Kubernetes Security & RBAC

Advanced module covering Kubernetes identity, authentication, authorization, RBAC, ServiceAccounts, Pod Security Standards, SecurityContext, NetworkPolicy, admission control, supply-chain security, audit logging, and troubleshooting.

## Learning path
1. [Kubernetes security model](01-security-model.md)
2. [Authentication and identity](02-authentication-identity.md)
3. [Authorization and RBAC](03-authorization-rbac.md)
4. [Roles, ClusterRoles and bindings](04-roles-bindings.md)
5. [ServiceAccounts and workload identity](05-serviceaccounts-workload-identity.md)
6. [Pod Security Standards and Admission](06-pod-security-standards.md)
7. [SecurityContext and container hardening](07-securitycontext-hardening.md)
8. [NetworkPolicy and network isolation](08-networkpolicy-isolation.md)
9. [Admission control and policy enforcement](09-admission-control-policy.md)
10. [Image and software supply-chain security](10-image-supply-chain-security.md)
11. [Secrets protection and encryption](11-secrets-protection.md)
12. [Audit logging and runtime detection](12-audit-runtime-security.md)
13. [Security troubleshooting and incident response](13-troubleshooting-incident-response.md)
14. [Interview questions](14-interview-questions.md)

## Labs
- [01 — RBAC least privilege](labs/01-rbac-least-privilege.md)
- [02 — ServiceAccount identity](labs/02-serviceaccount-identity.md)
- [03 — Pod security hardening](labs/03-pod-security-hardening.md)
- [04 — NetworkPolicy isolation](labs/04-networkpolicy-isolation.md)

## Manifests
See `manifests/`. Review namespaces, labels, service accounts, and policy selectors before applying. NetworkPolicy enforcement requires a compatible CNI. Pod Security Admission behavior depends on namespace labels and cluster version/configuration.

## Prerequisites
- Working Kubernetes cluster and `kubectl`.
- A non-production namespace or disposable cluster for labs.
- Permission to create Roles, RoleBindings, ServiceAccounts, and NetworkPolicies.
- Familiarity with ConfigMaps and Secrets from Module 04.

## Security principles
- Least privilege for users and workloads.
- Prefer namespace-scoped Roles over ClusterRoles where possible.
- Avoid wildcard verbs/resources.
- Do not mount credentials that a workload does not need.
- Use non-root, read-only, and capability-restricted containers where compatible.
- Treat network isolation as default-deny plus explicit allow rules.
- Verify policy enforcement; a YAML object alone does not prove the control is active.

## Official references
- https://kubernetes.io/docs/concepts/security/
- https://kubernetes.io/docs/reference/access-authn-authz/authentication/
- https://kubernetes.io/docs/reference/access-authn-authz/authorization/
- https://kubernetes.io/docs/reference/access-authn-authz/rbac/
- https://kubernetes.io/docs/concepts/security/service-accounts/
- https://kubernetes.io/docs/concepts/security/pod-security-standards/
- https://kubernetes.io/docs/tasks/configure-pod-container/security-context/
- https://kubernetes.io/docs/concepts/services-networking/network-policies/
- https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/
- https://kubernetes.io/docs/tasks/debug/debug-cluster/audit/
