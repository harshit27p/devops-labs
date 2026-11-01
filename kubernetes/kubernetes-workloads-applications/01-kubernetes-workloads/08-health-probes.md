# 08 — Health Probes: Startup, Readiness, Liveness

## Why probes matter

A process being alive does not necessarily mean an application is initialized or able to serve requests. Probes let kubelet evaluate container health and readiness.

## Probe types

| Probe | Question | Failure effect |
|---|---|---|
| Startup | Has the app completed startup? | Container is restarted after configured failure threshold |
| Liveness | Is the app stuck or unhealthy enough to restart? | Container is restarted |
| Readiness | Can the app currently receive traffic? | Pod is marked not ready; matching Service endpoints exclude it |

A startup probe suppresses liveness and readiness checks until startup succeeds. This is useful for slow-starting applications.

## Probe mechanisms

- `httpGet`: HTTP endpoint, commonly `/healthz` or `/readyz`.
- `tcpSocket`: verifies a TCP connection can be established.
- `exec`: runs a command in the container.
- `grpc`: checks gRPC health where supported by the cluster version.

## Example

See [`manifests/pod-probes.yaml`](manifests/pod-probes.yaml).

## Configuration fields

- `initialDelaySeconds`: delay before the first probe.
- `periodSeconds`: probe interval.
- `timeoutSeconds`: time allowed for a probe.
- `successThreshold`: consecutive successes needed after failure (readiness can use values above one).
- `failureThreshold`: consecutive failures before action.
- `terminationGracePeriodSeconds`: optional per-probe termination grace period where supported.

## Common design mistakes

1. **Liveness checks an external database.** A database outage can restart every app Pod, worsening an incident. Liveness should generally test whether the process can make progress.
2. **Readiness is too shallow.** A listening socket may not mean the app can serve useful traffic.
3. **Probe timeout is too aggressive.** CPU contention or transient latency can cause false failures.
4. **Startup has no allowance.** Slow initialization can trigger liveness restarts before the app is ready.
5. **Probe endpoint is expensive.** Health checks should be fast and low overhead.

## Troubleshooting

```bash
kubectl describe pod <pod> -n <ns>
kubectl get pod <pod> -n <ns> -o jsonpath='{.status.containerStatuses[*].restartCount}'
kubectl get endpointslices -n <ns>
kubectl logs <pod> -n <ns> --previous
```

For a readiness failure, inspect probe events and confirm the endpoint, port, path, response code, and application startup sequence. For liveness restarts, inspect previous logs and restart count.

## Reference

- [Configure liveness, readiness and startup probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)
