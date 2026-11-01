# Kubernetes Overview

## 1. What Kubernetes is

Kubernetes is an extensible platform for orchestrating containerized workloads. It exposes an API through which users and automation declare the resources they want. Control-plane components and controllers continuously observe the cluster and work to move the actual state toward the declared state.

Kubernetes is not simply a container runtime, a virtual machine manager, or a single deployment command. It is a distributed control system made up of an API, persistent cluster state, controllers, schedulers, node agents and extensible networking and storage integrations.

## 2. The problems it addresses

A single container can be started with a runtime command, but operating many services across multiple machines introduces recurring problems:

- Placement: choosing a suitable machine for each workload.
- Recovery: replacing failed workloads and reacting to node failures.
- Scaling: changing replica counts as demand changes.
- Discovery: allowing services to find changing workload instances.
- Configuration: separating application configuration from container images.
- Rollouts: changing application versions while controlling availability.
- Resource governance: expressing CPU and memory requests, limits and policies.
- Extensibility: integrating custom controllers, storage systems and platform tools.

Kubernetes provides primitives for these tasks. It does not automatically make every application highly available or secure; workload design, cluster configuration and operational practices still matter.

## 3. Core design principles

### Declarative desired state

A manifest describes the target configuration. For example, a Deployment may declare three replicas. The system attempts to maintain that target as Pods fail, nodes change or users update the manifest.

### Reconciliation

Controllers compare observed state with desired state and take corrective actions. Reconciliation is continuous, asynchronous and generally idempotent. Do not assume that all changes happen immediately after an API request succeeds.

### API-centric architecture

The Kubernetes API is the central interface for cluster objects. `kubectl`, controllers, operators and automation tools interact with the API server rather than editing cluster state files directly.

### Extensibility

CustomResourceDefinitions (CRDs), admission webhooks, API aggregation, controllers and operators allow platforms to add domain-specific APIs and automation. These are covered in the advanced modules.

## 4. What Kubernetes does not provide automatically

- It does not build application images; use a build system or CI pipeline.
- It does not guarantee that application code is fault-tolerant.
- It does not provide durable application storage merely because a Pod is rescheduled.
- It does not make an exposed Service secure by default.
- It does not replace centralized logging, monitoring, backup or incident response.
- It does not guarantee zero downtime from every rollout configuration.

## 5. Typical deployment flow

1. A developer packages an application into a container image.
2. The image is pushed to a registry.
3. A manifest describes the workload and related resources.
4. A client submits the desired objects to the API server.
5. The API server authenticates, authorizes and validates the request.
6. Controllers create dependent objects and the scheduler assigns eligible Pods to nodes.
7. Kubelets ask the container runtime to create the containers.
8. Networking and storage integrations provide connectivity and volumes.
9. Controllers continue reconciling the system as conditions change.

## 6. Example: a declarative application target

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
  namespace: learning
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
        - name: nginx
          image: nginx:1.27
          ports:
            - name: http
              containerPort: 80
```

This manifest declares a Deployment and a Pod template. It does not directly create three containers on a particular node. The Deployment and ReplicaSet controllers, scheduler, kubelets and runtime participate in reaching the target.

For a production environment, pin an approved image version or digest, define resource requests and limits, add suitable probes, and apply security controls. Those details are covered in the workload and security modules.

## 7. Useful commands

```bash
kubectl version
kubectl cluster-info
kubectl get nodes -o wide
kubectl get namespaces
kubectl api-resources
kubectl explain deployment.spec
```

## 8. Common misconceptions

| Misconception | Correct interpretation |
|---|---|
| Kubernetes runs containers directly | The kubelet coordinates with a CRI-compatible container runtime |
| A successful `kubectl apply` means the app is ready | It means the API accepted the object; readiness must be checked separately |
| A Pod is a durable application identity | Pods are replaceable; use higher-level controllers and persistent storage when required |
| Kubernetes is a complete PaaS | It provides primitives; platform capabilities are assembled through configuration and integrations |
| All clusters have identical internals | Distributions and providers can change component deployment and networking implementation |

## 9. Troubleshooting starting points

- `kubectl` cannot connect: inspect current context, kubeconfig, API endpoint, VPN and credentials.
- No nodes are Ready: inspect node conditions, kubelet health and control-plane connectivity.
- Objects are accepted but Pods do not start: inspect Deployment, ReplicaSet, Pod events and scheduling conditions.
- Application is running but unreachable: continue with the networking module; do not assume the API server controls the application data path.

## 10. Interview questions

**Q1. What is Kubernetes?**  
Kubernetes is an extensible container orchestration platform that exposes an API for declaring and managing workloads and cluster resources through controllers and node agents.

**Q2. What is the difference between Docker and Kubernetes?**  
A container runtime builds or runs containers. Kubernetes coordinates workloads across a cluster and integrates runtimes through the Container Runtime Interface. Docker Engine is not required on every Kubernetes node.

**Q3. What is desired state?**  
Desired state is the configuration declared in an API object, commonly in its `spec`. Controllers compare it with observed state and attempt to reconcile differences.

**Q4. Does Kubernetes guarantee zero downtime?**  
No. Availability depends on replica count, readiness behavior, disruption budgets, topology, application behavior, rollout strategy and infrastructure health.

## References

- [Kubernetes concepts](https://kubernetes.io/docs/concepts/)
- [Kubernetes components](https://kubernetes.io/docs/concepts/overview/components/)
- [Kubernetes cluster architecture](https://kubernetes.io/docs/concepts/architecture/)
