# Declarative vs Imperative Kubernetes Management

## 1. Two management styles

### Imperative management

An imperative command describes an action to perform now.

```bash
kubectl create deployment web --image=nginx:1.27
kubectl scale deployment web --replicas=3
kubectl expose deployment web --port=80 --target-port=80
```

This is useful for exploration, quick diagnostics and controlled one-off operations. However, command history alone is a weak source of truth for a team or production environment.

### Declarative management

A declarative manifest describes the intended configuration. Kubernetes and its controllers work toward that state.

```bash
kubectl apply -f deployment.yaml
```

The manifest can be reviewed, version-controlled, tested, promoted between environments and reconciled repeatedly.

## 2. Comparison

| Dimension | Imperative | Declarative |
|---|---|---|
| Describes | Action | Desired object state |
| Typical interface | `kubectl create`, `scale`, `set` | `kubectl apply -f` |
| Repeatability | Depends on command and current state | Designed for repeatable desired-state management |
| Review | Harder without captured commands | Diff and code review friendly |
| Version control | Requires extra discipline | Natural fit |
| Automation | Possible, but scripts must encode sequence | Strong fit for GitOps and CI/CD |
| Best use | Exploration and targeted operations | Team and production configuration |

## 3. Apply workflow

Create a manifest:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
  namespace: learning
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
          ports:
            - containerPort: 80
```

Validate and preview:

```bash
kubectl apply --dry-run=client -f deployment.yaml
kubectl diff -f deployment.yaml
```

Apply and verify:

```bash
kubectl apply -f deployment.yaml
kubectl rollout status deployment/web -n learning
kubectl get deployment web -n learning
```

Client-side dry-run checks locally known structure. Server-side dry-run sends a request to the API server without persisting the object and can exercise server-side validation and admission:

```bash
kubectl apply --dry-run=server -f deployment.yaml
```

Server-side dry-run requires a reachable cluster and compatible admission webhooks.

## 4. Apply and field ownership

Modern `kubectl apply` commonly uses server-side apply when requested with `--server-side`. Server-side apply tracks field ownership in managed fields and can report conflicts when different managers attempt to own the same fields.

Example:

```bash
kubectl apply --server-side -f deployment.yaml
kubectl get deployment web -n learning -o yaml
```

Do not casually use `--force-conflicts` in shared environments. First inspect which manager owns the conflicting fields and agree on the source of truth.

## 5. Avoid configuration drift

Configuration drift occurs when live cluster state diverges from the reviewed source configuration. Causes include manual edits, multiple automation systems managing the same fields, undocumented hotfixes and environment-specific differences.

Reduce drift by:

- Keeping manifests or Helm/Kustomize sources in version control.
- Reviewing changes through pull requests.
- Assigning clear ownership to resources and fields.
- Avoiding multiple competing reconcilers for the same object.
- Using GitOps for continuous reconciliation where appropriate.
- Recording emergency changes and back-porting them to source control.

## 6. Kustomize and Helm boundaries

Kustomize composes and patches Kubernetes manifests. Helm packages templates and values into versioned charts. Both are covered in the extensibility and packaging module; this page focuses on the management model.

## 7. Troubleshooting

| Symptom | Possible cause | Response |
|---|---|---|
| `kubectl diff` shows unexpected changes | Live drift or different source version | Inspect diff and managed fields |
| Apply reports field conflict | Another manager owns fields | Identify manager; coordinate ownership |
| Apply succeeds but workload is not ready | Reconciliation or runtime issue | Inspect rollout, Pods and events |
| Manual change disappears | Controller or GitOps reconciler restores declared state | Change source of truth, not only live object |
| Different environments behave differently | Values, API versions or cluster capabilities differ | Track environment overlays and versions |

## 8. Interview questions

**Q1. Why is declarative management preferred for production?**  
It makes desired configuration reviewable, repeatable and version-controlled, and supports reconciliation and automation.

**Q2. Does `kubectl apply` guarantee application readiness?**  
No. It reports API object operations. Check controller status, Pod readiness and application health separately.

**Q3. What is configuration drift?**  
A difference between the approved source configuration and live cluster state.

**Q4. What is server-side apply?**  
An API mechanism that tracks field ownership and merges declarative configurations, surfacing ownership conflicts.

## References

- [Object management](https://kubernetes.io/docs/concepts/overview/working-with-objects/object-management/)
- [Declarative configuration](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/declarative-config/)
- [Server-side apply](https://kubernetes.io/docs/reference/using-api/server-side-apply/)
