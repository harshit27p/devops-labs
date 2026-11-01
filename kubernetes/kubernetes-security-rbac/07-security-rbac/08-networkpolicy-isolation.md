# 08 — NetworkPolicy and Network Isolation

NetworkPolicy controls allowed Pod communication at L3/L4 when enforced by a compatible network plugin.

## Default deny
A policy selecting Pods and declaring ingress or egress policy types with no allow rules isolates that direction by default.

See:
- `manifests/networkpolicy-default-deny.yaml`
- `manifests/networkpolicy-allow-dns-web.yaml`

## Policy design
1. Identify workload labels and namespaces.
2. Define required ingress sources and ports.
3. Define required egress destinations and ports.
4. Account for DNS, monitoring, service meshes, and external dependencies.
5. Test both allowed and denied flows.

## Important behavior
- NetworkPolicy is additive: traffic is allowed if it matches an applicable allow rule.
- Policies apply to connections involving selected Pods.
- Standard NetworkPolicy is L3/L4, not an application-layer firewall.
- Enforcement depends on the CNI; creating a policy object does not guarantee enforcement.
- Host-network behavior and some advanced scenarios vary by implementation.

## Debug
```bash
kubectl get networkpolicy -A
kubectl describe networkpolicy -n <namespace> <policy>
kubectl get pods -o wide --show-labels
```
Validate from actual test Pods and consult CNI-specific diagnostics.
