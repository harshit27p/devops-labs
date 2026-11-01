# 03 — Resource Requests, Limits, and QoS

## Requests
Requests represent the resource amount Kubernetes uses for scheduling decisions. They are not a guaranteed performance reservation in every runtime detail, but they influence placement and resource accounting.

## Limits
Limits constrain resource use:
- CPU limits are enforced through throttling.
- Memory limits are enforced through OOM termination when usage exceeds the limit, subject to kernel/runtime behavior.

## Example
```yaml
resources:
  requests:
    cpu: "250m"
    memory: "256Mi"
  limits:
    cpu: "1"
    memory: "512Mi"
```

## CPU units
`1` CPU is one vCPU/core unit; `100m` is one tenth of a CPU. CPU is compressible: contention typically causes throttling rather than immediate termination.

## Memory units
Use `Mi`/`Gi` for binary units. Memory is not compressible; exceeding a container memory limit can result in OOM kill.

## QoS classes
- **Guaranteed:** every container has CPU and memory requests equal to limits (and valid nonzero values).
- **Burstable:** at least one request/limit exists, but not all containers meet Guaranteed criteria.
- **BestEffort:** no CPU or memory requests/limits are specified.

QoS influences eviction behavior under node pressure but does not replace priority or good capacity planning.

## Inspect
```bash
kubectl describe pod <pod>
kubectl get pod <pod> -o jsonpath='{.status.qosClass}{"\n"}'
kubectl top pods
kubectl top nodes
```
Metrics commands require a functioning Metrics API.
