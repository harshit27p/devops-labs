# 01 — Kubernetes Networking Model

## 1. The network model

Kubernetes defines a networking model rather than a single mandatory implementation. The standard model expects:
- Each Pod to have its own IP address.
- Pods on a node to communicate with one another without NAT.
- Pods on different nodes to communicate without NAT.
- Agents on a node (such as kubelet) to communicate with Pods on that node.

A cluster networking implementation configures the underlying routes, interfaces, encapsulation, or cloud network integration needed to realize this model.

## 2. Main communication paths

| Flow | Typical mechanism |
|---|---|
| Container to container in same Pod | Shared Pod network namespace; communicate over `localhost` |
| Pod to Pod on same node | Pod network interfaces and node dataplane |
| Pod to Pod on different nodes | CNI/network fabric routing or overlay |
| Pod to Service | Service virtual IP/dataplane selects a backend |
| External client to Service | NodePort, LoadBalancer, or an HTTP routing layer |
| Pod to DNS | Cluster DNS Service, usually CoreDNS |

## 3. Important network identities

- **Container port:** port on which a process listens inside its container network namespace.
- **Pod IP:** address assigned to the Pod network namespace.
- **Service port:** stable port exposed by the Service abstraction.
- **Target port:** backend Pod port to which traffic is directed.
- **NodePort:** port exposed on cluster nodes for a NodePort Service.
- **External IP / load balancer address:** externally reachable address supplied by infrastructure or configuration.

A Service's `port` and `targetPort` do not need to be the same. Named target ports can decouple the Service from a numeric backend port.

## 4. Network namespaces

Containers in one Pod share the Pod network namespace. They share the Pod IP and port space, so two containers in the same Pod cannot bind the same IP:port combination. They can communicate using `localhost`.

Different Pods have distinct network namespaces and IPs.

## 5. Packet path overview

For a client Pod connecting to a ClusterIP Service:
1. The client resolves the Service DNS name to a ClusterIP.
2. The packet is sent to the Service IP and port.
3. The service dataplane selects a ready backend endpoint.
4. The packet is forwarded to the selected Pod IP and target port.
5. Return traffic follows the dataplane's connection-tracking and routing behavior.

The exact implementation and packet path depend on kube-proxy mode or an alternative dataplane.

## 6. Useful inspection commands

```bash
kubectl get nodes -o wide
kubectl get pods -A -o wide
kubectl get svc -A
kubectl get endpointslices -A
kubectl describe node <node>
kubectl get pod <pod> -n <ns> -o jsonpath='{.status.podIP}{"\n"}'
```

Inside a diagnostic Pod, use available tools such as `ip addr`, `ip route`, `ss -lntup`, `getent hosts`, `nslookup`, `dig`, `curl`, and `nc`. Minimal images may not include these tools.

## 7. Design implications

- Never use Pod IPs as durable application endpoints.
- Use Services for stable addressing and service discovery.
- Avoid assuming a particular CNI, overlay, or kube-proxy implementation.
- Check MTU and encapsulation when large packets fail but small requests work.
- Consider egress paths, DNS, firewalls, and cloud security controls as well as in-cluster routing.

## References

- [Cluster networking](https://kubernetes.io/docs/concepts/cluster-administration/networking/)
- [Services](https://kubernetes.io/docs/concepts/services-networking/service/)
