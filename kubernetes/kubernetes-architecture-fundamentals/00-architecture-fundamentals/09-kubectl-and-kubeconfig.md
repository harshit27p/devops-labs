# kubectl and kubeconfig

## 1. What kubectl does

`kubectl` is the primary command-line client for communicating with the Kubernetes API. It creates, inspects, updates and deletes API objects; reads logs; executes commands in containers; and performs selected cluster administration operations.

It does not bypass the API server. Its requests are subject to the configured authentication, authorization and admission controls.

## 2. kubeconfig structure

A kubeconfig file contains clusters, users, contexts and the current context.

- **Cluster**: API server endpoint and cluster certificate authority information.
- **User**: authentication information or an exec credential plugin configuration.
- **Context**: combination of cluster, user and optional default namespace.
- **Current context**: context used when a command does not specify another context.

Default path is usually `$HOME/.kube/config`. `KUBECONFIG` or `--kubeconfig` can select other files.

## 3. Context management

```bash
kubectl config get-contexts
kubectl config current-context
kubectl config use-context CONTEXT_NAME
kubectl config view --minify
kubectl config view --raw
```

Treat `kubectl config view --raw` as sensitive because it can expose credentials. Do not paste its output into tickets, chat or Git repositories.

## 4. Safe command habits

Before changing a cluster:

```bash
kubectl config current-context
kubectl cluster-info
kubectl get nodes
kubectl get namespaces
```

Use explicit context and namespace for sensitive operations:

```bash
kubectl --context=dev-cluster -n learning get pods
kubectl --context=dev-cluster -n learning apply -f deployment.yaml
```

For destructive commands, inspect the target first and use explicit names:

```bash
kubectl get deployment web -n learning
kubectl delete deployment web -n learning
```

Avoid broad deletion commands such as `kubectl delete all --all` unless you fully understand the scope and dependencies.

## 5. Common inspection commands

```bash
# Cluster and API discovery
kubectl cluster-info
kubectl get nodes -o wide
kubectl api-resources
kubectl api-versions

# Objects
kubectl get pods -A
kubectl get deployments -n learning
kubectl describe pod POD_NAME -n learning
kubectl get pod POD_NAME -n learning -o yaml

# Events and logs
kubectl get events -n learning --sort-by=.lastTimestamp
kubectl logs POD_NAME -n learning
kubectl logs POD_NAME -n learning --previous

# Resource usage (requires Metrics API)
kubectl top nodes
kubectl top pods -A

# API permissions
kubectl auth can-i get pods -n learning
kubectl auth can-i create deployments -n learning
```

`kubectl top` depends on a functioning Metrics API, commonly provided by Metrics Server. It is not a replacement for a full monitoring stack.

## 6. Output formats and filtering

```bash
kubectl get pods -o wide
kubectl get pods -o yaml
kubectl get pods -o json
kubectl get pods -l app=web
kubectl get pods --field-selector=status.phase=Running
kubectl get pods -o custom-columns=NAME:.metadata.name,NODE:.spec.nodeName,PHASE:.status.phase
```

JSONPath can extract fields:

```bash
kubectl get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.conditions[-1].type}{"\n"}{end}'
```

For scripts, prefer stable structured output and handle errors explicitly. Do not rely on human-readable column order as a machine interface.

## 7. Namespace defaults

```bash
kubectl config set-context --current --namespace=learning
kubectl config view --minify
```

A context's default namespace changes the scope of commands that omit `-n`. For repeatable scripts and production operations, specifying `--namespace` explicitly is often safer.

## 8. Troubleshooting

| Error | Likely cause | Check |
|---|---|---|
| `connection refused` | API endpoint unavailable or wrong | Current context, endpoint, VPN, cluster status |
| `Unauthorized` | Credentials invalid/expired | User config or exec credential plugin |
| `Forbidden` | Identity lacks permission | `kubectl auth can-i`, RBAC bindings |
| `no context exists` | Wrong kubeconfig or context name | `KUBECONFIG`, `config get-contexts` |
| `x509` certificate error | CA, certificate or endpoint mismatch | Trusted CA and correct cluster configuration |
| `the server doesn't have a resource type` | Wrong API resource/version or CRD absent | `api-resources`, `api-versions` |

## 9. Interview questions

**Q1. What is a kubeconfig context?**  
A named combination of a cluster, user and optional namespace.

**Q2. Where does kubectl find its configuration?**  
Usually `$HOME/.kube/config`, unless `KUBECONFIG` or `--kubeconfig` overrides it.

**Q3. What is the difference between `get` and `describe`?**  
`get` retrieves resource representations; `describe` presents a human-oriented summary including related events where available.

**Q4. Why should `kubectl top` not replace Prometheus?**  
It provides a current resource-usage view through the Metrics API, not long-term time-series storage, alerting and broad observability.

## References

- [kubectl overview](https://kubernetes.io/docs/reference/kubectl/)
- [kubectl command reference](https://kubernetes.io/docs/reference/kubectl/generated/)
- [Organizing cluster access using kubeconfig](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/)
