# 10 — NetworkPolicy

## Purpose and limits

NetworkPolicy defines rules for controlling traffic to and from Pods at the IP/port level. Policies are namespace-scoped and select Pods using labels.

**Important:** NetworkPolicy enforcement requires a network plugin that implements it. Creating a NetworkPolicy object on a cluster whose CNI does not enforce policy may have no effect.

NetworkPolicy is not a full application-layer firewall. Standard NetworkPolicy is primarily L3/L4 and does not express HTTP paths, user identities, or TLS content rules.

## Policy behavior

- A Pod is non-isolated for ingress until selected by an ingress policy.
- A Pod is non-isolated for egress until selected by an egress policy.
- Once isolated in a direction, only traffic allowed by applicable policies is permitted in that direction.
- Multiple policies selecting a Pod combine additively; an allow in one applicable policy can permit traffic.
- Ingress and egress isolation are independent.

## Default deny

See [`manifests/networkpolicy-default-deny.yaml`](manifests/networkpolicy-default-deny.yaml).

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny
  namespace: networking-lab
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
```

This selects all Pods in the namespace and isolates them for both directions. It can break DNS and application communication until explicit allow policies are added.

## Allow web traffic and DNS

See [`manifests/networkpolicy-allow-dns-and-web.yaml`](manifests/networkpolicy-allow-dns-and-web.yaml). The sample allows ingress TCP/8080 from Pods labelled `access: allowed` and egress DNS UDP/TCP 53 to Pods labelled `k8s-app: kube-dns` in `kube-system`.

CoreDNS labels and namespace labels vary by cluster. Inspect actual labels before adapting this policy.

## Design checklist

- Start with a clear traffic-flow diagram.
- Identify source and destination Pod labels.
- Include DNS egress when default-deny egress is enabled.
- Include required ingress from gateway, monitoring, and health-check components.
- Test both allowed and denied flows.
- Account for node-originated and host-network traffic according to CNI behavior.
- Keep policies small, reviewed, and version-controlled.

## Debugging

```bash
kubectl get networkpolicy -A
kubectl describe networkpolicy <policy> -n <ns>
kubectl get pods -n <ns> --show-labels
kubectl get pods -n kube-system --show-labels
```

Test connectivity from an explicitly selected source Pod. Confirm the CNI supports enforcement and inspect its policy logs/observability tools.

## Reference

- [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
