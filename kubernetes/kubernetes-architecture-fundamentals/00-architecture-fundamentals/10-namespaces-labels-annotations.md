# Namespaces, Labels and Annotations

## 1. Namespaces

Namespaces provide a scope for namespaced API objects and a mechanism for organizing resources within a cluster. They are commonly used to separate teams, applications or environments, but they are not a complete security boundary by themselves.

Examples:

```bash
kubectl get namespaces
kubectl create namespace learning
kubectl get pods -n learning
kubectl get deployments --all-namespaces
```

A namespace does not isolate every resource. Nodes, PersistentVolumes and Namespaces themselves are cluster-scoped. Network isolation requires appropriate network policy and a supporting CNI; API access control requires authorization such as RBAC.

## 2. Labels

Labels are key/value metadata used to identify and select groups of objects. Controllers and Services commonly use selectors to find the objects they manage or target.

Example:

```yaml
metadata:
  labels:
    app.kubernetes.io/name: payments
    app.kubernetes.io/instance: payments-prod
    app.kubernetes.io/component: api
    environment: production
```

Query by label:

```bash
kubectl get pods -n learning -l app.kubernetes.io/name=payments
kubectl get pods -n learning -l 'environment in (staging,production)'
```

Selectors support equality-based and set-based requirements. Label values are strings and must comply with Kubernetes label syntax.

## 3. Annotations

Annotations attach non-identifying metadata that tools, controllers or integrations can read. Unlike labels, annotations are not intended for selection.

Examples include deployment metadata, documentation links, checksums, tool configuration and integration-specific settings.

```yaml
metadata:
  annotations:
    example.com/change-ticket: "CHG-1042"
    example.com/owner: "platform-team"
```

Do not store secrets or large unbounded data in annotations.

## 4. Standard labels

Kubernetes recommends a set of common labels, including:

- `app.kubernetes.io/name`
- `app.kubernetes.io/instance`
- `app.kubernetes.io/version`
- `app.kubernetes.io/component`
- `app.kubernetes.io/part-of`
- `app.kubernetes.io/managed-by`

Use a consistent labeling scheme across deployments, services, monitoring and automation.

## 5. Namespace design

Common patterns include:

- Namespace per environment: `dev`, `staging`, `production`.
- Namespace per team or application domain.
- Shared platform namespaces for cluster add-ons.

Choose a model that aligns with RBAC, quotas, network policy, cost allocation and operational ownership. Too many namespaces can increase operational overhead; too few can make access and resource governance difficult.

## 6. Practical example

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: learning
  labels:
    environment: lab
    team: platform
---
apiVersion: v1
kind: Pod
metadata:
  name: web
  namespace: learning
  labels:
    app.kubernetes.io/name: web
    app.kubernetes.io/component: frontend
  annotations:
    documentation.example.com/runbook: "https://example.invalid/runbooks/web"
spec:
  containers:
    - name: nginx
      image: nginx:1.27
```

The `.invalid` domain is reserved for examples; replace it with a real internal runbook URL if adapting the manifest.

Apply and inspect:

```bash
kubectl apply -f namespace-and-pod.yaml
kubectl get pods -n learning --show-labels
kubectl get pods -n learning -l app.kubernetes.io/name=web
kubectl get pod web -n learning -o jsonpath='{.metadata.annotations}'
```

## 7. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `NotFound` in a namespace | Command targets wrong namespace | Add `-n` or inspect current context |
| Service has no endpoints | Selector does not match Pod labels | Compare Service selector and Pod labels |
| Label query returns nothing | Key/value mismatch | Inspect `--show-labels` |
| RBAC appears correct but access fails | RoleBinding is in another namespace or subject differs | Inspect binding namespace, subject and roleRef |
| Namespace stuck Terminating | Finalizers or remaining resources | Inspect namespace conditions and finalizers carefully |

## 8. Interview questions

**Q1. Are namespaces security boundaries?**  
They provide scope and support policy boundaries, but strong isolation also requires RBAC, network policies, Pod security and appropriate cluster design.

**Q2. What is the difference between labels and annotations?**  
Labels are intended for selection and grouping. Annotations store additional metadata and are not used by label selectors.

**Q3. Can a Pod exist without a namespace?**  
A namespaced object without an explicit namespace is created in the request's default namespace, usually `default` if no other namespace is selected.

**Q4. Are all Kubernetes resources namespaced?**  
No. Use `kubectl api-resources` to inspect scope.

## References

- [Namespaces](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)
- [Labels and selectors](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/)
- [Annotations](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/)
- [Recommended labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/common-labels/)
