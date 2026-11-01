# 00 — Architecture & Fundamentals

This module establishes the mental model required to understand every later Kubernetes topic. It focuses on the control plane, node agents, API interactions, the object model and the operational interface.

## Learning outcomes

After completing this module, you should be able to:

1. Explain the responsibilities and boundaries of control-plane and worker-node components.
2. Trace a declarative workload request from `kubectl` to a running container.
3. Distinguish the API server, etcd, scheduler, controllers, kubelet and container runtime.
4. Explain desired state, observed state, reconciliation and eventual convergence.
5. Read and validate Kubernetes manifests.
6. Inspect cluster state safely using `kubectl`, contexts and namespaces.
7. Diagnose basic API connectivity, scheduling and node-agent issues.

## Topic index

| File | What it covers |
|---|---|
| [01 — Kubernetes overview](01-kubernetes-overview.md) | What Kubernetes is, problems it solves, architecture principles and boundaries |
| [02 — Cluster architecture](02-cluster-architecture.md) | Control plane, nodes, cluster topology, HA and communication paths |
| [03 — Control-plane components](03-control-plane-components.md) | API server, etcd, scheduler, controller manager and cloud controller manager |
| [04 — Worker-node components](04-worker-node-components.md) | kubelet, runtime, CRI, CNI, CSI and service proxy responsibilities |
| [05 — API request lifecycle](05-api-request-lifecycle.md) | Authentication, authorization, admission, persistence, watches and reconciliation |
| [06 — Kubernetes object model](06-kubernetes-object-model.md) | Objects, `spec`, `status`, metadata, ownership and API resources |
| [07 — Declarative vs imperative management](07-declarative-vs-imperative.md) | Apply workflows, field ownership, idempotency and operational trade-offs |
| [08 — YAML manifest fundamentals](08-yaml-manifest-fundamentals.md) | Manifest structure, schema validation, labels, selectors and safe authoring |
| [09 — kubectl and kubeconfig](09-kubectl-and-kubeconfig.md) | Contexts, namespaces, discovery, inspection, output formats and safe command patterns |
| [10 — Namespaces, labels and annotations](10-namespaces-labels-annotations.md) | Scope, organization, selection and metadata conventions |

## Practical labs

- [Lab 01 — Inspect a Kubernetes cluster](labs/01-inspect-a-cluster.md)
- [Lab 02 — Apply and inspect a declarative workload](labs/02-apply-a-declarative-workload.md)

## Manifests and diagrams

- [nginx-deployment.yaml](manifests/nginx-deployment.yaml)
- [Cluster architecture diagram source](diagrams/cluster-architecture.mmd)
- [API request lifecycle diagram source](diagrams/api-request-lifecycle.mmd)

## Prerequisites

- A Kubernetes cluster: Minikube, kind, Docker Desktop Kubernetes, kubeadm or a managed cluster.
- A compatible `kubectl` binary.
- A kubeconfig that grants permission to inspect and create resources in a non-production namespace.
- Basic familiarity with containers, Linux processes, IP networking and YAML.

> **Safety:** Perform the labs in a disposable development cluster or a dedicated namespace. Do not test deletion, privilege escalation or cluster-wide changes against a production cluster.

## Recommended completion order

Read files 01–05 first to understand the system architecture and request lifecycle. Then read files 06–10 to understand the API object model and day-to-day CLI workflow. Finish both labs and use the troubleshooting sections as revision material.

## Non-duplication map

This module explains the Kubernetes platform and API fundamentals. Detailed Pod and Deployment behavior belongs in Module 01; Service and CNI behavior belongs in Module 02; RBAC policy design belongs in Module 07; and cluster installation or upgrades belong in Module 12 and Module 10 respectively.
