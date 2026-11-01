# 09 — Kubernetes Cluster DNS

## CoreDNS role

Most Kubernetes clusters use CoreDNS to provide service discovery. Pods are configured to use cluster DNS through their resolver configuration. CoreDNS watches Kubernetes API resources and answers queries for Service and Pod records according to its configuration.

The exact DNS implementation, cluster domain, and Pod resolver settings can vary.

## Common Service DNS formats

- Same namespace: `service-name`
- Another namespace: `service-name.namespace`
- Fully qualified: `service-name.namespace.svc.cluster-domain`

For a headless Service, DNS can return endpoint addresses rather than one virtual IP.

## Inspect DNS configuration

```bash
kubectl get pods -n kube-system -l k8s-app=kube-dns
kubectl get svc -n kube-system
kubectl get configmap coredns -n kube-system -o yaml
kubectl exec -n <ns> <pod> -- cat /etc/resolv.conf
```

Label selectors for CoreDNS Pods can differ between distributions.

## Test DNS

```bash
kubectl run dns-test -n <ns> --rm -it --restart=Never --image=busybox:1.36 -- nslookup kubernetes.default
kubectl run dns-test -n <ns> --rm -it --restart=Never --image=busybox:1.36 -- nslookup <service>.<namespace>.svc
```

Use an approved diagnostic image if public image pulls are disabled.

## DNS troubleshooting sequence

1. Confirm the Pod has a valid `/etc/resolv.conf`.
2. Test lookup of `kubernetes.default`.
3. Test the target Service's fully qualified name.
4. Check Service exists and has the expected name/namespace.
5. Check CoreDNS Pods and Service endpoints.
6. Inspect CoreDNS logs and configuration.
7. Check NetworkPolicy egress to DNS (UDP and TCP port 53).
8. Check node-level DNS, upstream resolver, and forwarding configuration.

DNS uses both UDP and TCP port 53. Large responses and fallback behavior make TCP important; do not allow only UDP in restrictive policies.

## `ndots` and search paths

Pod resolver configuration commonly includes search domains and an `ndots` option. Short names may be expanded against search domains before absolute lookup. This can generate additional queries and latency in some applications. Use fully qualified names where appropriate and tune only after measuring.

## Reference

- [DNS for Services and Pods](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)
