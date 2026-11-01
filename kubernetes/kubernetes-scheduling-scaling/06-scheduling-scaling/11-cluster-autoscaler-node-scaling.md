# 11 — Cluster Autoscaler and Node Scaling

Cluster Autoscaler adjusts the number of nodes in a node group when Pods cannot be scheduled due to insufficient resources or when nodes are underutilized and workloads can be moved.

## Responsibilities
- HPA: adjusts Pod replicas.
- Cluster Autoscaler: adjusts node group size.
- Cloud/provider autoscaling integration: creates or removes actual compute instances.

Cluster Autoscaler requires supported infrastructure integration and correctly configured node groups. It is not a generic built-in cloud provisioner.

## Scale-up signals
Pending Pods that cannot fit on existing nodes may trigger scale-up if a suitable node group can satisfy their constraints.

## Scale-down considerations
A node may not be removable if it hosts:
- Pods that cannot be evicted or moved.
- Local storage dependencies.
- PDB-constrained workloads.
- System-critical or specially configured Pods.
- Pods with restrictive affinity/anti-affinity or topology rules.

## Operational checks
Inspect Pending Pod events, Cluster Autoscaler logs/status, node group limits, cloud quota, and scheduling constraints. Exact commands depend on distribution and provider.

## Alternatives
Karpenter and provider-native node provisioning systems have different architectures and configuration models. Do not assume their behavior or APIs are interchangeable with Cluster Autoscaler.
