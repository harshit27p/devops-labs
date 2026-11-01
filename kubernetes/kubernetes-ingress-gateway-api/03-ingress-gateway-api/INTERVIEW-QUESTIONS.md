# Kubernetes Ingress & Gateway API — Interview Questions

## Ingress

1. What is an Ingress resource?
2. Why is an Ingress controller required?
3. Compare Ingress and IngressClass.
4. Explain host-based and path-based routing.
5. Compare Exact, Prefix, and ImplementationSpecific path types.
6. How does TLS termination work with Ingress?
7. Why is Ingress API described as frozen?
8. Does Ingress support arbitrary TCP/UDP protocols?

## Gateway API

9. What problem does Gateway API solve?
10. Explain GatewayClass, Gateway, Listener, and HTTPRoute.
11. What is the role-oriented design of Gateway API?
12. How does an HTTPRoute attach to a Gateway?
13. What is `allowedRoutes`?
14. What is ReferenceGrant and when is it required?
15. Explain backendRefs and weighted traffic splitting.
16. Compare TLS termination and passthrough.
17. What are HTTPRoute filters?

## Operations and security

18. Why is installing Gateway API CRDs not enough to route traffic?
19. How do you troubleshoot an HTTPRoute that is not accepted?
20. What is the impact of a missing backend EndpointSlice?
21. How should TLS certificates be renewed and protected?
22. Why must route creation be controlled in a multi-tenant cluster?
23. What is the ingress-nginx retirement and what should existing users do?

## Scenario questions

24. Ingress exists but has no address. What do you inspect?
25. A request returns 404. How do you identify whether host/path matching failed?
26. HTTPS returns the wrong certificate. What do you check?
27. Gateway is accepted but not programmed. What could cause this?
28. A route references a Service in another namespace. What permission is required?
29. How would you safely migrate production traffic from Ingress to Gateway API?
30. How would you implement a 90/10 canary rollout and validate it?

## Commands

```bash
kubectl get ingressclass
kubectl get ingress -A
kubectl describe ingress <name> -n <ns>
kubectl get gatewayclass
kubectl get gateway -A
kubectl describe gateway <name> -n <ns>
kubectl get httproute -A
kubectl describe httproute <name> -n <ns>
kubectl get svc,endpointslices -n <ns>
```
