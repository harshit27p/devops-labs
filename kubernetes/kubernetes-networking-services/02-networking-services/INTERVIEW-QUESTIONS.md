# Kubernetes Networking & Services — Interview Questions

## Networking model and CNI

1. Explain the Kubernetes networking model.
2. How do containers in the same Pod communicate?
3. What is CNI and what does a CNI plugin configure?
4. Compare overlay networking and native routing.
5. What is IPAM?
6. Why can overlapping Pod CIDRs and VPC CIDRs cause problems?

## Services and endpoints

7. Why are Services needed if Pods already have IP addresses?
8. Compare ClusterIP, NodePort, and LoadBalancer.
9. Explain `port`, `targetPort`, and `nodePort`.
10. What is a headless Service?
11. What is an ExternalName Service?
12. What is an EndpointSlice and why was it introduced?
13. A Service has no endpoints. How do you troubleshoot it?
14. Explain `externalTrafficPolicy: Local` versus `Cluster`.

## DNS

15. What is CoreDNS responsible for?
16. How do you access a Service in another namespace?
17. Why might a DNS lookup succeed while the connection fails?
18. Why must DNS policies account for both UDP and TCP port 53?
19. What are Pod DNS search domains and `ndots`?

## NetworkPolicy

20. Does Kubernetes enforce NetworkPolicy automatically?
21. Explain default-deny ingress and egress.
22. How do multiple NetworkPolicies combine?
23. How would you allow only selected Pods to reach an application?
24. Why can default-deny egress break DNS?

## Scenario questions

25. Pod IP connectivity works but ClusterIP connectivity fails. What do you inspect?
26. A NodePort is allocated but unreachable from outside. What layers do you check?
27. Only cross-node Pod traffic fails. What are likely causes?
28. A LoadBalancer Service remains pending. What infrastructure components do you verify?
29. Small HTTP requests work but large uploads fail. What network property might be involved?
30. How would you isolate a DNS failure from an application listener failure?

## Command quick reference

```bash
kubectl get pods -A -o wide
kubectl get svc -A
kubectl get endpointslices -A
kubectl get networkpolicy -A
kubectl describe svc <name> -n <ns>
kubectl describe networkpolicy <name> -n <ns>
kubectl get pods -n <ns> --show-labels
kubectl get events -A --sort-by=.metadata.creationTimestamp
```
