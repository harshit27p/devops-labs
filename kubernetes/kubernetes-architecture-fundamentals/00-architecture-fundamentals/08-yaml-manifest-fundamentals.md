# Kubernetes YAML Manifest Fundamentals

## 1. Purpose of a manifest

A Kubernetes manifest is a YAML or JSON document describing one or more API objects. Manifests are submitted to the API server through tools such as `kubectl`, Helm or automation clients.

YAML is indentation-sensitive. Use spaces, not tabs, and keep nesting consistent.

## 2. Required top-level fields

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: learning
```

- `apiVersion`: API group/version.
- `kind`: object kind.
- `metadata`: name, namespace and metadata.
- `spec`: desired configuration for resources that define a spec.
- `status`: observed state; normally populated by the system.

Not every object has identical fields. Use the API schema for the exact resource and version.

## 3. Labels and selectors

A Deployment selector must match the labels in its Pod template:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
  namespace: learning
  labels:
    app.kubernetes.io/name: api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
        - name: api
          image: nginx:1.27
```

The selector/template mismatch is a common source of invalid Deployments. Selectors for an `apps/v1` Deployment are immutable after creation.

## 4. Multi-document YAML

A single file can contain multiple resources separated by `---`:

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: learning
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: web-config
  namespace: learning
data:
  APP_MODE: "development"
```

Apply the file with:

```bash
kubectl apply -f resources.yaml
```

## 5. Field types and quoting

YAML has strings, numbers, booleans, lists and maps. Quote values when ambiguity is possible, especially values that resemble booleans, numbers, dates or special scalars.

```yaml
data:
  FEATURE_ENABLED: "true"
  HTTP_PORT: "8080"
replicas: 2
```

ConfigMap and Secret `data` values are strings. Other API fields may require integer or boolean values.

## 6. Validate manifests

```bash
kubectl apply --dry-run=client -f manifest.yaml
kubectl apply --dry-run=server -f manifest.yaml
kubectl diff -f manifest.yaml
kubectl explain deployment.spec
```

Use a YAML linter and schema-aware validation in CI where practical. Client-side parsing does not prove the manifest is valid for the target cluster. Server-side validation is more authoritative for the connected API server.

## 7. Common YAML mistakes

| Mistake | Result | Prevention |
|---|---|---|
| Wrong indentation | Parse error or wrong nesting | Use consistent spaces |
| Incorrect `apiVersion` | No matching API resource | Check `kubectl api-versions` and docs |
| Wrong `kind` | API mapping failure | Check `kubectl api-resources` |
| Selector mismatch | Controller cannot manage intended Pods | Match selector and template labels |
| String supplied where integer required | Validation error | Follow API schema |
| Missing namespace | Object created in current namespace | Set `metadata.namespace` or pass `-n` |
| Duplicate keys | Parser-dependent behavior or validation warning | Keep keys unique |

## 8. Practical authoring conventions

- Use meaningful resource names.
- Add standard labels such as `app.kubernetes.io/name`, `app.kubernetes.io/instance` and `app.kubernetes.io/component` where appropriate.
- Keep secrets out of plain-text manifests committed to Git.
- Separate environment-specific values using an overlay or values file.
- Pin container images to an approved version or digest.
- Include resource requests/limits and security context in workload manifests.
- Keep one resource per file when it improves reviewability; group tightly related objects when it improves usability.

## 9. Interview questions

**Q1. What is the purpose of `apiVersion`?**  
It selects the API group and version used to interpret the resource.

**Q2. What is the difference between `metadata` and `spec`?**  
Metadata identifies and annotates the object; spec declares the desired configuration.

**Q3. Can multiple Kubernetes objects exist in one YAML file?**  
Yes. Separate documents with `---`.

**Q4. Why use server-side dry-run?**  
It asks the API server to process the request without persisting it, allowing server-side validation and admission behavior to be checked.

## References

- [Objects in Kubernetes](https://kubernetes.io/docs/concepts/overview/working-with-objects/)
- [API reference](https://kubernetes.io/docs/reference/kubernetes-api/)
- [Configuration best practices](https://kubernetes.io/docs/concepts/configuration/overview/)
