# 06 — Pod Security Standards and Admission

Pod Security Standards define three policy levels:
- **Privileged:** unrestricted; intended for trusted system workloads.
- **Baseline:** prevents known privilege escalations while allowing common workloads.
- **Restricted:** strongly constrained best-practice profile.

## Pod Security Admission
Pod Security Admission is built into Kubernetes and can enforce namespace-level policy using labels:
- `pod-security.kubernetes.io/enforce`
- `pod-security.kubernetes.io/audit`
- `pod-security.kubernetes.io/warn`

Example labels:
```bash
kubectl label namespace app   pod-security.kubernetes.io/enforce=restricted   pod-security.kubernetes.io/audit=restricted   pod-security.kubernetes.io/warn=restricted
```

Use version labels where appropriate to pin policy behavior, such as `pod-security.kubernetes.io/enforce-version`.

## Rollout strategy
1. Start with `warn` and `audit`.
2. Review violations and remediate workloads.
3. Test in a staging namespace.
4. Enable `enforce` with an agreed version.
5. Monitor rejected deployments and maintain exceptions narrowly.

## Important
Pod Security Admission evaluates Pod security settings. It is not a general-purpose policy engine for all Kubernetes object types. Use admission policy frameworks or webhooks for additional organizational rules.
