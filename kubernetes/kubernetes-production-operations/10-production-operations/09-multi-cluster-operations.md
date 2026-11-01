# 09 — Multi-Cluster and Regional Operations

## Why multiple clusters?

Multiple clusters may provide isolation, regulatory boundaries, regional presence, blast-radius reduction, separate lifecycle control, or distinct environments. They also increase operational complexity.

## Design choices

- one cluster per environment vs shared clusters;
- regional clusters vs a single global cluster;
- active/passive vs active/active traffic;
- centralized vs per-cluster observability;
- shared identity and policy vs cluster-specific controls.

## Fleet consistency

Use standardized cluster provisioning, version policies, add-on baselines, policy bundles, and GitOps repositories. Avoid assuming every cluster is identical; document intentional differences.

## Service discovery and traffic

Cross-cluster networking and service discovery require explicit solutions: service mesh federation, global load balancing, DNS-based routing, or provider-specific networking. Kubernetes Services are cluster-scoped by default and do not automatically provide cross-cluster discovery.

## Data considerations

Stateful multi-region systems require replication, conflict handling, consistency decisions, backup, and recovery design. Compute failover does not automatically fail over databases or persistent volumes.

## Operational checklist

- inventory clusters, owners, versions, and regions;
- standardize identity and access;
- monitor fleet health centrally;
- test cluster replacement and workload redeployment;
- define traffic failover and DNS TTL behavior;
- document data replication and recovery points;
- control configuration drift and version skew.

## Further reading

- https://kubernetes.io/docs/concepts/cluster-administration/
