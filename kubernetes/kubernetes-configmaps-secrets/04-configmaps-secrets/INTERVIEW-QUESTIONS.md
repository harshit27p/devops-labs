# Kubernetes ConfigMaps & Secrets — Interview Questions

## Fundamentals

1. Why externalize configuration from container images?
2. Compare ConfigMap and Secret.
3. What are the ways to inject configuration into a Pod?
4. When should a value be stored in a ConfigMap versus a Secret?
5. Are ConfigMaps intended for large files?

## ConfigMaps

6. Compare `env`, `envFrom`, and volume mounts.
7. What happens when a ConfigMap used as an environment variable changes?
8. How are mounted ConfigMap updates propagated?
9. Why does a `subPath` mount not receive projected updates?
10. How can a configuration change trigger a Deployment rollout?

## Secrets and security

11. Why is Base64 not encryption?
12. What are common Kubernetes Secret types?
13. How do you create a TLS Secret?
14. How does RBAC protect Secrets?
15. Why can permission to create Pods in a namespace be sensitive?
16. What is encryption at rest and how is it configured?
17. What are common ways secrets leak through CI/CD or debugging?
18. Why should secret values not be printed in logs?

## Advanced operations

19. What does `immutable: true` do?
20. Explain versioned ConfigMaps and rollback.
21. Compare External Secrets Operator and Secrets Store CSI Driver.
22. What is workload identity?
23. Explain a safe credential rotation sequence.
24. How do you verify that a Pod can access a Secret without printing its value?

## Scenario questions

25. A Pod reports `CreateContainerConfigError`. How do you troubleshoot?
26. A ConfigMap file changed but the app still uses the old setting. Why?
27. A Secret was committed to Git. What is the correct incident response?
28. A service account can list all Secrets. How would you reduce permissions?
29. How would you rotate a database password without downtime?
30. How would you design secret delivery for a multi-tenant cluster?

## Commands

```bash
kubectl get configmaps,secrets -n <ns>
kubectl describe configmap <name> -n <ns>
kubectl describe secret <name> -n <ns>
kubectl describe pod <pod> -n <ns>
kubectl auth can-i get secrets -n <ns> --as=system:serviceaccount:<ns>:<sa>
kubectl rollout restart deployment/<name> -n <ns>
kubectl rollout status deployment/<name> -n <ns>
```
