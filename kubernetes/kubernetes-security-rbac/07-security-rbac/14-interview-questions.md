# 14 — Kubernetes Security & RBAC Interview Questions

1. Explain authentication, authorization, and admission in the API request path.
2. Compare Role and ClusterRole.
3. Compare RoleBinding and ClusterRoleBinding.
4. Why is least privilege important in RBAC?
5. What are Kubernetes ServiceAccounts?
6. Why disable ServiceAccount token automount?
7. What is Pod Security Admission?
8. Compare Privileged, Baseline, and Restricted Pod Security Standards.
9. Explain runAsNonRoot, readOnlyRootFilesystem, and allowPrivilegeEscalation.
10. What are Linux capabilities?
11. How does NetworkPolicy work, and what does CNI enforcement mean?
12. Why is NetworkPolicy additive?
13. What are mutating and validating admission webhooks?
14. What is a webhook failurePolicy trade-off?
15. Why is base64 not encryption?
16. How should image provenance and signatures be enforced?
17. What does Kubernetes audit logging capture?
18. Why can permission to create Pods expose namespace Secrets?
19. How would you investigate a Forbidden error?
20. How would you respond to a compromised ServiceAccount?

## Scenario prompts
- A developer needs to read Pods but must not read Secrets. Design the RBAC.
- A Pod is rejected by Restricted policy. How do you identify and fix violations?
- A NetworkPolicy is present but traffic is still allowed. What do you verify?
- An application does not need Kubernetes API access. How do you reduce token exposure?
- A privileged image was deployed. What evidence and containment steps matter?

Strong answers identify the security layer, scope permissions narrowly, validate enforcement, and explain operational trade-offs.
