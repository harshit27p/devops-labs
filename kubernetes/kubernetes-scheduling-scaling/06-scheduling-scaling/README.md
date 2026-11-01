# Kubernetes Scheduling & Scaling

Advanced module covering Pod scheduling, resource management, placement constraints, QoS, topology spread, priority/preemption, autoscaling, and troubleshooting.

## Learning path
1. [Scheduling fundamentals](01-scheduling-fundamentals.md)
2. [Scheduler architecture and scheduling cycle](02-scheduler-architecture.md)
3. [Resource requests, limits and QoS](03-resource-requests-limits-qos.md)
4. [Node selectors and node affinity](04-node-selectors-node-affinity.md)
5. [Pod affinity and anti-affinity](05-pod-affinity-anti-affinity.md)
6. [Taints and tolerations](06-taints-and-tolerations.md)
7. [Topology spread constraints](07-topology-spread-constraints.md)
8. [Priority classes and preemption](08-priority-preemption.md)
9. [Horizontal Pod Autoscaler](09-horizontal-pod-autoscaler.md)
10. [Vertical Pod Autoscaler](10-vertical-pod-autoscaler.md)
11. [Cluster Autoscaler and node scaling](11-cluster-autoscaler-node-scaling.md)
12. [Scaling strategies and production design](12-scaling-strategies-production.md)
13. [Scheduling and scaling troubleshooting](13-troubleshooting.md)
14. [Interview questions](14-interview-questions.md)

## Labs
- [01 — Inspect scheduling and node resources](labs/01-inspect-scheduler-resources.md)
- [02 — Placement constraints](labs/02-placement-constraints.md)
- [03 — HPA with Metrics Server](labs/03-hpa-metrics-server.md)
- [04 — Priority and preemption](labs/04-priority-preemption.md)

## Manifests
See `manifests/`. HPA requires a working Metrics API (commonly Metrics Server) and resource requests on relevant containers. VPA and Cluster Autoscaler require separately installed components and compatible infrastructure; they are not built into every cluster.

## Prerequisites
- Working Kubernetes cluster and `kubectl`.
- Permission to inspect nodes, Pods, events, and metrics.
- A test cluster for taint, priority, and autoscaling experiments.
- Familiarity with Pods, Deployments, and Services from earlier modules.

## Important distinctions
- Scheduler places Pods; it does not itself add cluster nodes.
- HPA changes desired replica count; it does not provision nodes.
- Cluster Autoscaler changes node capacity when supported infrastructure integration is installed.
- VPA recommends or adjusts container resource requests; its behavior depends on mode and installation.

## Official references
- https://kubernetes.io/docs/concepts/scheduling-eviction/kube-scheduler/
- https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
- https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/
- https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/
- https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/
- https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/
- https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/
- https://github.com/kubernetes/autoscaler/tree/master/vertical-pod-autoscaler
- https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler
