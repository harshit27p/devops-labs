# Kubernetes Networking & Services

Advanced, practical notes on Kubernetes networking: Pod connectivity, CNI, Services, EndpointSlices, cluster DNS, NetworkPolicy, and troubleshooting.

> **Prerequisites:** [00 — Architecture & Fundamentals](../00-architecture-fundamentals/README.md) and [01 — Workloads & Applications](../01-kubernetes-workloads/README.md).

## Learning outcomes

- Explain the Kubernetes networking model and Pod IP connectivity.
- Understand the role of CNI plugins and the Service dataplane.
- Select and configure ClusterIP, NodePort, LoadBalancer, headless, and ExternalName Services.
- Understand selectors, EndpointSlices, service discovery, and cluster DNS.
- Apply and test NetworkPolicies with an enforcing CNI plugin.
- Troubleshoot DNS, routing, selectors, endpoints, ports, and policy issues.

## Module map

| File | Coverage |
|---|---|
| [01 Networking model](01-kubernetes-networking-model.md) | Pod network, node network, traffic paths |
| [02 CNI](02-cni-and-pod-networking.md) | CNI responsibilities, IPAM, plugin architecture |
| [03 Services](03-services-overview.md) | Stable virtual IP, selectors, service ports |
| [04 ClusterIP](04-clusterip.md) | Internal service exposure |
| [05 NodePort](05-nodeport.md) | Node-level service access |
| [06 LoadBalancer](06-loadbalancer.md) | External load balancer integration |
| [07 Headless and ExternalName](07-headless-and-externalname.md) | DNS-based discovery and aliases |
| [08 EndpointSlices](08-endpointslices.md) | Backend endpoint tracking |
| [09 Cluster DNS](09-cluster-dns.md) | CoreDNS, search paths, DNS debugging |
| [10 NetworkPolicy](10-networkpolicy.md) | L3/L4 traffic isolation |
| [11 Troubleshooting](11-network-troubleshooting.md) | Layered diagnosis and commands |
| [12 Service selection](12-service-design-patterns.md) | Design decisions and production patterns |

## Labs

- [Lab 01 — Service discovery and ClusterIP](labs/01-service-discovery-clusterip.md)
- [Lab 02 — NodePort exposure](labs/02-nodeport-access.md)
- [Lab 03 — NetworkPolicy isolation](labs/03-networkpolicy-isolation.md)
- [Lab 04 — DNS and connectivity troubleshooting](labs/04-dns-troubleshooting.md)

## Manifests

- `manifests/demo-app.yaml`
- `manifests/clusterip-service.yaml`
- `manifests/nodeport-service.yaml`
- `manifests/headless-service.yaml`
- `manifests/networkpolicy-default-deny.yaml`
- `manifests/networkpolicy-allow-dns-and-web.yaml`

## Quick start

```bash
kubectl config current-context
kubectl get nodes -o wide
kubectl create namespace networking-lab
kubectl apply -f manifests/demo-app.yaml
kubectl apply -f manifests/clusterip-service.yaml
kubectl get pods,svc,endpointslices -n networking-lab -o wide
```

Only use a disposable or approved cluster. NodePort and NetworkPolicy behavior depends on cluster networking and firewall configuration.

## Core networking principles

1. Every Pod receives its own cluster-routable IP address.
2. Pods can communicate with other Pods without NAT in the standard Kubernetes network model.
3. A Service provides a stable abstraction over a changing set of backend Pods.
4. Service implementation is provided by the cluster dataplane; kube-proxy is common but not mandatory.
5. NetworkPolicy enforcement requires a networking implementation that supports it.
6. DNS names are the normal service-discovery interface; avoid hardcoding Pod IPs.

## Out of scope here

Ingress controllers and Gateway API provide HTTP(S) routing from outside the cluster and are covered in [03 — Ingress & Gateway API](../03-ingress-gateway-api/README.md) when that module is created.

## Official references

- [Cluster networking](https://kubernetes.io/docs/concepts/cluster-administration/networking/)
- [Services, Load Balancing, and Networking](https://kubernetes.io/docs/concepts/services-networking/)
- [Services](https://kubernetes.io/docs/concepts/services-networking/service/)
- [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
- [DNS for Services and Pods](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)
