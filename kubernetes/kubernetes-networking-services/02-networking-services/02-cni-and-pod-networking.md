# 02 — CNI and Pod Networking

## 1. What is CNI?

The Container Network Interface (CNI) is a specification and plugin ecosystem used by container runtimes to configure network connectivity for containers. In Kubernetes, the runtime invokes CNI plugins as Pods are created and removed, according to the runtime and cluster integration.

CNI is not itself one specific network product. Implementations include plugins and platforms such as Cilium, Calico, Flannel, and cloud-provider networking solutions.

## 2. Typical responsibilities

- Create or attach a network interface for a Pod.
- Allocate and release Pod IP addresses (IPAM).
- Configure routes, bridges, tunnels, or native routing.
- Optionally enforce network policy or provide observability, depending on product.
- Integrate with host networking and the cluster's routing fabric.

The precise division of responsibilities varies by CNI implementation and version.

## 3. Common architecture approaches

| Approach | Concept | Trade-off |
|---|---|---|
| Overlay | Encapsulates Pod traffic across nodes | Simplifies routing integration; adds encapsulation overhead |
| Native routing | Routes Pod CIDRs through the underlay | Can be efficient; requires compatible network routing |
| Cloud VPC-native | Integrates Pod IPs with cloud networking | Cloud-specific limits and configuration |
| eBPF dataplane | Uses eBPF programs for networking/policy/observability | Powerful integration; kernel and product requirements apply |

## 4. IP address management (IPAM)

IPAM allocates Pod addresses and prevents collisions. Address planning must account for:
- Node and Pod CIDRs.
- Service CIDR.
- VPC/VNet and on-premises networks.
- VPN, peered networks, and corporate routes.
- Maximum Pods per node and cloud interface/IP limits.

Overlapping CIDRs can break connectivity in ways that are difficult to diagnose.

## 5. CNI troubleshooting approach

```bash
kubectl get pods -n kube-system -o wide
kubectl get daemonsets -n kube-system
kubectl describe node <node>
kubectl get events -A --sort-by=.metadata.creationTimestamp
```

On a node, with appropriate administrator access, inspect runtime and CNI logs using the operating system's service manager and the runtime-specific paths. Do not edit CNI configuration files on a live node without understanding the distribution's lifecycle and rollback process.

## 6. Common symptoms

- Pod stuck in `ContainerCreating`: CNI ADD failure, IP exhaustion, sandbox creation failure.
- Cross-node only connectivity failure: routing, encapsulation, firewall, MTU, or node-specific CNI issue.
- NetworkPolicy appears ineffective: CNI may not enforce NetworkPolicy, or policy selectors/ports do not match.
- Intermittent packet loss: MTU, conntrack pressure, node overload, or dataplane issues.

## References

- [Network plugins](https://kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/)
- [CNI specification](https://github.com/containernetworking/cni)
