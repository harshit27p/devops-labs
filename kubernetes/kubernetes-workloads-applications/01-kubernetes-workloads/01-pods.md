# 01 — Pods

## 1. What is a Pod?

A Pod is the smallest deployable unit in Kubernetes. It represents one or more containers that are scheduled together and share a network namespace, IP address, port space, and explicitly mounted volumes. Containers in a Pod are co-located on the same node and are intended to form one tightly coupled application unit.

The common pattern is **one application container per Pod**. Multi-container Pods are appropriate when containers have a close lifecycle and need local coordination.

## 2. Pod lifecycle and identity

Pods are ephemeral. A replacement Pod is a new object with a new UID and normally a different IP address; do not treat Pod names or IPs as durable application identity. Use a Service for stable network access (covered in the Networking module).

Typical Pod phases:
- `Pending`: accepted but not yet fully running; may be waiting for scheduling, image pulls, or setup.
- `Running`: bound to a node and at least one primary container is running or starting.
- `Succeeded`: all containers terminated successfully and will not be restarted.
- `Failed`: all containers terminated and at least one failed.
- `Unknown`: state cannot be obtained, often due to node communication problems.

A phase is a high-level summary, not a complete health diagnosis. Inspect container state and Events.

## 3. Multi-container patterns

| Pattern | Purpose | Example |
|---|---|---|
| Sidecar | Adds supporting capability beside the main app | log shipper, proxy |
| Ambassador | Proxies/abstracts external connections | local proxy |
| Adapter | Normalizes output or interface | metrics/log format adapter |

Prefer separate Deployments when components can scale, deploy, or fail independently. Shared Pod fate is a deliberate trade-off.

### Init containers

Init containers run to completion before application containers start. They are useful for setup tasks such as preparing files or waiting for a dependency, but avoid using them as an excuse for fragile dependency orchestration.

### Sidecar containers

Modern Kubernetes supports restartable sidecars expressed as init containers with `restartPolicy: Always` (stable in recent Kubernetes releases). Check cluster version and API support before relying on this behavior. A traditional sidecar can also be declared as a regular container, but startup and shutdown ordering differs.

## 4. Example: multi-container Pod

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-with-sidecar
  labels:
    app: web-with-sidecar
spec:
  initContainers:
    - name: prepare
      image: busybox:1.36
      command: ["sh", "-c", "echo prepared > /work/status"]
      volumeMounts:
        - name: shared
          mountPath: /work
  containers:
    - name: web
      image: nginx:1.27
      ports:
        - name: http
          containerPort: 80
      volumeMounts:
        - name: shared
          mountPath: /usr/share/nginx/html/status
          subPath: status
    - name: log-agent
      image: busybox:1.36
      command: ["sh", "-c", "while true; do date; sleep 30; done"]
  volumes:
    - name: shared
      emptyDir: {}
```

This is a learning example, not a production logging design. Pin images to approved versions/digests and configure security contexts and resource requests/limits.

## 5. Pod restart policy

`Always`, `OnFailure`, and `Never` control container restart behavior within a Pod. Workload types constrain valid values: Deployments use `Always`; Jobs commonly use `OnFailure` or `Never`.

Do not confuse a container restart with Pod replacement. A container can restart inside the same Pod; a controller can create a new Pod when the Pod itself is lost or deleted.

## 6. Useful commands

```bash
kubectl get pods -A -o wide
kubectl get pod <pod> -n <ns> -o yaml
kubectl describe pod <pod> -n <ns>
kubectl logs <pod> -n <ns>
kubectl logs <pod> -n <ns> -c <container>
kubectl logs <pod> -n <ns> --previous
kubectl exec -it <pod> -n <ns> -c <container> -- sh
kubectl get events -n <ns> --sort-by=.metadata.creationTimestamp
```

## 7. Common failure states

- `Pending`: insufficient CPU/memory, taints, affinity constraints, PVC not bound.
- `ErrImagePull` / `ImagePullBackOff`: image name/tag, registry auth, network, rate limit.
- `CrashLoopBackOff`: process exits repeatedly; inspect current and previous logs, command, config, probes, and exit code.
- `CreateContainerConfigError`: missing ConfigMap/Secret or invalid reference.
- `OOMKilled`: memory limit exceeded; profile usage and set realistic requests/limits.

## 8. Best practices

- Prefer controllers over standalone Pods for long-running applications.
- Define resource requests; set limits deliberately based on workload behavior.
- Add readiness and liveness probes only when they measure meaningful application states.
- Use non-root users, read-only root filesystems where possible, dropped Linux capabilities, and appropriate seccomp profiles.
- Avoid storing durable state in the writable container layer or `emptyDir`.
- Keep one clear responsibility per container; use multi-container Pods only for tightly coupled components.

## Further reading

- [Pods](https://kubernetes.io/docs/concepts/workloads/pods/)
- [Pod lifecycle](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/)
- [Init containers](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/)
