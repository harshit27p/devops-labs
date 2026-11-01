# 02 — Authentication and Identity

Authentication establishes the identity behind an API request. Kubernetes API servers can be configured with supported authenticators such as client certificates, bearer tokens, OIDC, and cloud/provider integrations. Exact configuration depends on the distribution and managed service.

## Human and workload identities
- Human operators commonly authenticate through an identity provider, OIDC, client certificates, or cloud CLI integration.
- Pods commonly use a ServiceAccount identity when calling the API.
- Nodes authenticate using node credentials and certificates managed by the cluster.

## Authentication is not authorization
A successfully authenticated user may still be denied by RBAC or another authorizer.

## ServiceAccount tokens
Modern Kubernetes uses projected, time-bound ServiceAccount tokens by default in normal Pod usage. Avoid manually creating long-lived token Secrets unless there is a specific compatibility requirement and a risk-reviewed reason.

## Inspect identity context
```bash
kubectl config current-context
kubectl config view --minify
kubectl auth whoami
kubectl get serviceaccounts -A
```
`kubectl auth whoami` availability depends on Kubernetes/kubectl version and API support.

## Security recommendations
- Integrate human access with centralized identity and MFA.
- Avoid sharing kubeconfig files.
- Protect client certificates and tokens as credentials.
- Prefer short-lived tokens and workload identity federation where supported.
- Revoke/rotate compromised credentials promptly.
- Audit identity-to-role mappings regularly.

Never paste kubeconfig credentials, bearer tokens, private keys, or cloud access tokens into tickets or chat.
