# Kubernetes Control-Plane Components

## 1. Responsibilities at a glance

| Component | Primary responsibility | Key operational concern |
|---|---|---|
| kube-apiserver | Exposes Kubernetes API | Availability, latency, authentication, admission |
| etcd | Stores API state | Quorum, latency, backup and restore |
| kube-scheduler | Binds unscheduled Pods to nodes | Scheduling throughput and constraints |
| kube-controller-manager | Runs core controllers | Reconciliation health and leader election |
| cloud-controller-manager | Cloud-specific controllers | Provider API permissions and availability |

## 2. kube-apiserver

The API server is the front end for the Kubernetes control plane. It serves RESTful API operations and coordinates request processing, authentication, authorization, admission and persistence.

Common responsibilities include:

- API discovery and versioned resource endpoints.
- Authentication of incoming identities.
- Authorization checks for requested verbs and resources.
- Admission control, including built-in admission plugins and configured webhooks.
- Schema and semantic validation.
- Persistence and retrieval through the configured storage layer.
- Watch APIs used by controllers and clients.

The API server is designed to scale horizontally. Multiple instances can serve requests behind a stable API endpoint.

### Operational checks

```bash
kubectl get --raw='/readyz?verbose'
kubectl get --raw='/livez?verbose'
kubectl get --raw='/version'
```

Access to non-resource endpoints may be restricted by authorization policy. A failure may indicate permissions rather than an unhealthy server.

## 3. etcd

etcd is a strongly consistent distributed key-value store used as Kubernetes' backing store. Kubernetes objects are persisted through the API server; users and controllers should not normally modify etcd directly.

Important concepts:

- Raft consensus and quorum.
- Leader election among etcd members.
- Read/write latency and disk I/O.
- Certificates and peer/client authentication.
- Snapshot backup and tested restoration.
- Version compatibility during upgrades.

A three-member etcd cluster can generally tolerate one member failure while retaining quorum. A two-member cluster cannot tolerate one member failure and retain quorum. Plan member count and failure domains deliberately.

Never run ad hoc `etcdctl put` or delete operations against Kubernetes keys. Use the Kubernetes API for supported object operations.

## 4. kube-scheduler

The scheduler watches for Pods that have no assigned node, evaluates eligible nodes and selects a node for each Pod.

Scheduling is more than round-robin placement. The scheduler considers:

- Resource requests and allocatable node resources.
- Node selectors and node affinity.
- Taints and Pod tolerations.
- Pod affinity and anti-affinity.
- Topology spread constraints.
- Volume topology and binding constraints.
- Scheduling gates, priorities and preemption where configured.

The scheduler makes a binding decision; kubelet on the selected node performs the local Pod lifecycle work.

Useful inspection:

```bash
kubectl get pods -A --field-selector=status.phase=Pending
kubectl describe pod POD_NAME -n NAMESPACE
kubectl get events -A --sort-by=.lastTimestamp
```

Look for `FailedScheduling` events to understand why a Pod is unschedulable.

## 5. kube-controller-manager

The controller manager runs multiple logically independent controllers in a consolidated process. Each controller watches relevant objects and reconciles actual state toward desired state.

Examples include:

- Node controller.
- Job controller.
- Namespace controller.
- ServiceAccount controller.
- EndpointSlice controller.
- Deployment and ReplicaSet controllers are controller logic in the Kubernetes control plane ecosystem; implementation and packaging details may vary by release.

A controller is not the same as the scheduler. A Deployment controller ensures the desired ReplicaSet exists; the scheduler selects nodes for Pods that need placement.

## 6. cloud-controller-manager

This optional component separates cloud-specific control logic from core Kubernetes. Depending on the provider integration, it may manage:

- Node lifecycle and provider identity.
- Cloud routes.
- Cloud load balancers for `Service` objects.
- Provider-specific volume integration (historically; CSI is the modern storage integration model).

On-premises and local development clusters may not run a cloud controller manager.

## 7. Leader election

Some replicated control-plane components use leader election so that one active instance performs a given control loop at a time, while other instances remain available for takeover. Leader election reduces duplicate work but does not remove the need to monitor component health and API connectivity.

## 8. Troubleshooting matrix

| Symptom | Likely area | First checks |
|---|---|---|
| API requests time out | API server, network, load balancer | `/readyz`, endpoint reachability, control-plane logs |
| API writes fail | etcd, admission, authorization | API errors, etcd health, webhook availability |
| Pods remain Pending | Scheduler or constraints | Pod events, requests, taints, affinity, PVC state |
| Replica count not converging | Controller reconciliation | Deployment/ReplicaSet status, events, controller logs |
| Cloud LoadBalancer remains pending | Cloud controller/provider | Service events, provider integration and IAM permissions |
| Cluster state unavailable | etcd quorum/storage | etcd member health, disk, network, recovery plan |

## 9. Interview questions

**Q1. What is the role of kube-apiserver?**  
It exposes the Kubernetes API and is the primary interface through which clients and control-plane components read or modify cluster objects.

**Q2. What is the difference between scheduler and controller manager?**  
The scheduler selects nodes for unscheduled Pods. Controllers reconcile specific resources and create or update dependent objects to achieve desired state.

**Q3. Why should etcd be backed up?**  
It stores the cluster's persistent API state. A tested backup is a key part of control-plane disaster recovery.

**Q4. Does etcd store container images?**  
No. Container images are stored in registries and pulled by the node runtime. etcd stores Kubernetes API data.

## References

- [Kubernetes components](https://kubernetes.io/docs/concepts/overview/components/)
- [Cluster architecture](https://kubernetes.io/docs/concepts/architecture/)
- [Scheduler](https://kubernetes.io/docs/concepts/scheduling-eviction/kube-scheduler/)
- [etcd documentation](https://etcd.io/docs/)
