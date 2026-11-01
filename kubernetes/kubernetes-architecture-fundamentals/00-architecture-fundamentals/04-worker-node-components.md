# Kubernetes Worker-Node Components

## 1. Node responsibilities

A Kubernetes Node is a physical or virtual machine that provides compute, memory, storage and networking for Pods. Each node is represented by a Node API object and is managed by the control plane.

Core node components:

1. kubelet
2. Container runtime
3. Container Runtime Interface (CRI) integration
4. CNI networking implementation
5. kube-proxy or an equivalent Service dataplane, depending on the cluster

## 2. kubelet

The kubelet is the node agent. It receives Pod specifications through configured sources and ensures that the containers described by those PodSpecs are running and healthy.

The kubelet:

- Registers or manages node status.
- Watches for Pods assigned to the node.
- Requests container lifecycle operations through the runtime.
- Coordinates volume mounting through storage integrations.
- Reports Pod and node status to the API server.
- Executes configured liveness, readiness and startup probes.

The kubelet does not manage arbitrary containers started outside Kubernetes.

## 3. Container runtime and CRI

The container runtime is responsible for pulling images and running containers. Kubernetes communicates with runtimes through the Container Runtime Interface (CRI).

Common runtimes include containerd and CRI-O. Docker Engine is not required on Kubernetes nodes; the historical dockershim integration was removed from Kubernetes.

The runtime handles container execution, image management, isolation primitives and lifecycle operations. The kubelet coordinates desired Pod state; the runtime performs the low-level container operations.

## 4. CNI networking

The Container Network Interface is a specification and plugin ecosystem used to configure container networking. A CNI implementation typically allocates Pod IP addresses and configures network connectivity.

Examples include Calico, Cilium, Flannel and cloud-provider-specific CNI implementations. Capabilities differ: policy enforcement, encryption, eBPF dataplane, routing mode and observability are implementation-specific.

Do not treat CNI as the same thing as kube-proxy. CNI configures Pod networking; Service forwarding may be implemented by kube-proxy or by an integrated dataplane.

## 5. kube-proxy

kube-proxy implements the Service virtual-IP behavior on nodes using packet-filtering or proxy mechanisms, depending on mode and version. Some network plugins replace kube-proxy's Service functionality, so the process may be absent.

Useful checks:

```bash
kubectl get pods -n kube-system -o wide
kubectl get daemonsets -n kube-system
kubectl get nodes -o wide
```

The precise system Pod names depend on distribution.

## 6. Node conditions and capacity

Inspect node health and allocatable capacity:

```bash
kubectl describe node NODE_NAME
kubectl get nodes -o json
kubectl top nodes
```

Important node conditions include `Ready`, `MemoryPressure`, `DiskPressure` and `PIDPressure`. Resource `capacity` describes total node resources; `allocatable` describes resources available to Pods after system reservations and other deductions.

## 7. Node lifecycle troubleshooting

| Symptom | Potential cause | Checks |
|---|---|---|
| Node NotReady | kubelet stopped, network issue, runtime failure | kubelet service/logs, runtime, node conditions |
| Pods stuck ContainerCreating | image, volume, CNI or runtime issue | Pod events, runtime logs, CNI logs |
| ImagePullBackOff | registry auth, image name, DNS or rate limit | Pod events, image reference and pull secret |
| Pod IP absent | CNI failure or IP exhaustion | CNI DaemonSet, plugin logs, IPAM |
| Node DiskPressure | image/log/ephemeral storage usage | filesystem, image garbage collection, Pod ephemeral usage |
| Pod repeatedly restarts | process failure, probe failure, OOM | previous logs, events, exit code, resource limits |

For self-managed Linux nodes, inspect services with the node's operating-system tools, for example:

```bash
sudo systemctl status kubelet
sudo journalctl -u kubelet -n 200 --no-pager
sudo systemctl status containerd
sudo journalctl -u containerd -n 200 --no-pager
```

These host commands are not available on many managed Kubernetes worker nodes.

## 8. Interview questions

**Q1. What does kubelet do?**  
It ensures that containers described by assigned PodSpecs are running and reports node and Pod status.

**Q2. What is CRI?**  
The Container Runtime Interface is the integration contract through which kubelet communicates with a container runtime.

**Q3. What is the difference between CNI and CRI?**  
CRI integrates container lifecycle operations; CNI integrates network configuration for containers and Pods.

**Q4. Is kube-proxy always present?**  
No. Some networking implementations provide equivalent Service routing functionality.

## References

- [Nodes](https://kubernetes.io/docs/concepts/architecture/nodes/)
- [Container runtimes](https://kubernetes.io/docs/setup/production-environment/container-runtimes/)
- [Network plugins](https://kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/)
- [Kubernetes components](https://kubernetes.io/docs/concepts/overview/components/)
