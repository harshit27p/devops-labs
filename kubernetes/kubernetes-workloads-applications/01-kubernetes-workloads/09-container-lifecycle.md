# 09 — Container Lifecycle and Graceful Termination

## Container states

Kubernetes reports container states:
- `Waiting`: startup work is pending, such as image pull or configuration.
- `Running`: container process is executing.
- `Terminated`: process has exited, with exit code and reason.

Pod phases and container states are different levels of status. Use `kubectl describe pod` and container status fields to diagnose.

## Restart policy

| Policy | Behavior |
|---|---|
| `Always` | Restart terminated containers regardless of exit code |
| `OnFailure` | Restart only after non-zero exit |
| `Never` | Do not restart the terminated container |

Controllers and workload type influence the appropriate policy. Deployments require `Always`; Jobs typically use `Never` or `OnFailure`.

## Lifecycle hooks

- `postStart`: invoked after container creation; execution ordering relative to the container entrypoint is not guaranteed.
- `preStop`: invoked before container termination; consumes time from the Pod's termination grace period.

Hooks should be short, reliable, and safe to retry. Do not use them as a substitute for proper application shutdown handling.

## Graceful termination sequence

When a Pod is deleted, Kubernetes sets a deletion timestamp and starts the grace period. Kubelet asks the runtime to stop containers, typically sending `SIGTERM` to the main process. If processes remain after the grace period, they are forcibly killed (`SIGKILL`). The default grace period is commonly 30 seconds unless configured otherwise.

Applications should:
- Handle `SIGTERM`.
- Stop accepting new work.
- Finish or safely abandon in-flight requests.
- Flush buffers and close connections.
- Exit before the grace period expires.

## Example settings

```yaml
spec:
  terminationGracePeriodSeconds: 45
  containers:
    - name: app
      image: example.invalid/my-app:1.0 # replace with your approved image
      lifecycle:
        preStop:
          exec:
            command: ["/bin/sh", "-c", "sleep 5"]
```

The placeholder image is intentionally non-runnable. A sleep in `preStop` is only illustrative; use an application-specific drain action where appropriate.

## Troubleshooting restarts

```bash
kubectl get pods -n <ns>
kubectl describe pod <pod> -n <ns>
kubectl logs <pod> -n <ns> --previous
kubectl get pod <pod> -n <ns> -o jsonpath='{range .status.containerStatuses[*]}{.name}{" "}{.lastState.terminated.reason}{" "}{.lastState.terminated.exitCode}{"\n"}{end}'
```

Investigate exit codes, OOMKilled, probe failures, signals, application logs, and node pressure.

## Reference

- [Pod lifecycle](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/)
