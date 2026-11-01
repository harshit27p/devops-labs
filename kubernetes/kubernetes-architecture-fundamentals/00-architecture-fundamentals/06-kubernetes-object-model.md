# Kubernetes Object Model

## 1. What is a Kubernetes object?

A Kubernetes object is a persistent record of intent describing a resource in the cluster. Objects represent workloads, configuration, networking, storage, policies and cluster-level resources.

Examples include Pods, Deployments, Services, ConfigMaps, Secrets, Nodes, Namespaces and PersistentVolumeClaims.

Objects are created and managed through the Kubernetes API. A manifest is a declarative representation of an object, usually written in YAML.

## 2. Standard object structure

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
  namespace: learning
  labels:
    app.kubernetes.io/name: web
spec:
  replicas: 2
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
status: {}
```

### `apiVersion`

Identifies the API group and version used for the resource. For example, `apps/v1` is the stable API version for Deployments.

### `kind`

Identifies the resource type, such as `Deployment`, `Pod` or `Service`.

### `metadata`

Contains object identity and metadata such as name, namespace, labels and annotations. The API server also manages fields such as UID, resource version and creation timestamp.

### `spec`

Describes desired configuration. Its schema differs by resource type.

### `status`

Reports observed state. It is generally populated by Kubernetes components and controllers rather than manually authored by users.

## 3. Desired state versus observed state

For a Deployment with `spec.replicas: 2`, the desired state is two replicas. The controller observes the current state and creates or removes dependent resources as needed. The status may report available replicas, updated replicas and conditions.

`spec` is intent; `status` is observation. The system continually reconciles differences, but convergence may take time and can be blocked by constraints or failures.

## 4. Namespaced and cluster-scoped resources

Some resources are namespaced, such as Pods, Deployments and Services. Others are cluster-scoped, such as Nodes, PersistentVolumes and Namespaces themselves.

Check resource scope rather than assuming:

```bash
kubectl api-resources
kubectl api-resources --namespaced=true
kubectl api-resources --namespaced=false
```

## 5. Object identity and metadata

An object's name is unique within its scope. A UID identifies a specific object instance and changes if an object is deleted and recreated with the same name. `resourceVersion` is an opaque value used by the API for concurrency and watch semantics; do not parse it as a timestamp or assume it is a globally increasing integer.

Labels support selection and grouping. Annotations attach non-identifying metadata for tools and integrations. Their detailed conventions are covered in [10 — Namespaces, labels and annotations](10-namespaces-labels-annotations.md).

## 6. Ownership and dependent resources

Controllers commonly create dependent objects. For example, a Deployment manages ReplicaSets, which manage Pods. Owner references allow Kubernetes garbage collection and controllers to understand relationships.

Inspect ownership:

```bash
kubectl get pod POD_NAME -n learning -o yaml
kubectl get rs -n learning -o yaml
kubectl get deployment web -n learning -o yaml
```

Avoid manually changing controller-managed child objects unless performing a deliberate diagnostic action. Change the owning resource's desired state instead.

## 7. Discover and inspect schemas

```bash
kubectl api-resources
kubectl api-versions
kubectl explain deployment
kubectl explain deployment.spec
kubectl explain deployment.spec.template.spec.containers
kubectl get deployment web -n learning -o yaml
kubectl get deployment web -n learning -o json
```

`kubectl explain` uses API schema information and is useful for checking valid fields for the connected cluster version.

## 8. Common errors

| Error | Meaning | Next step |
|---|---|---|
| `no matches for kind` | API version or CRD not served | Check `apiVersion`, `kubectl api-resources`, CRD installation |
| `unknown field` | Field not in the schema or wrong nesting | Use `kubectl explain`; validate YAML indentation |
| `AlreadyExists` | Object name already exists in scope | Inspect existing object and decide whether to update |
| `NotFound` | Object or API endpoint not found | Check name, namespace, API group/version |
| `Forbidden` | Caller lacks authorization | Check identity and `kubectl auth can-i` |

## 9. Interview questions

**Q1. What is the difference between `spec` and `status`?**  
`spec` describes desired state; `status` reports observed state.

**Q2. What is a UID?**  
A unique identifier for a particular object instance, distinct from its reusable name.

**Q3. What is `resourceVersion` used for?**  
It supports API concurrency and watch behavior. Clients should treat it as opaque.

**Q4. Are all Kubernetes resources namespaced?**  
No. Resources can be namespaced or cluster-scoped.

## References

- [Objects in Kubernetes](https://kubernetes.io/docs/concepts/overview/working-with-objects/)
- [Kubernetes API concepts](https://kubernetes.io/docs/concepts/overview/kubernetes-api/)
- [API resource reference](https://kubernetes.io/docs/reference/kubernetes-api/)
