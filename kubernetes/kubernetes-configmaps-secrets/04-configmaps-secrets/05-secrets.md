# 05 — Kubernetes Secrets

## What is a Secret?

A Secret stores a small amount of sensitive data, such as a password, token, or key. Pods can consume Secret data through environment variables or mounted volumes. Secret objects are namespaced.

Secrets are not automatically encrypted merely because their values are represented as base64. Configure encryption at rest and restrict access.

## Common Secret types

| Type | Use |
|---|---|
| `Opaque` | Arbitrary user-defined data |
| `kubernetes.io/tls` | TLS certificate and private key |
| `kubernetes.io/dockerconfigjson` | Registry authentication configuration |
| `kubernetes.io/basic-auth` | Basic authentication credentials |
| `kubernetes.io/ssh-auth` | SSH authentication data |
| `kubernetes.io/service-account-token` | Legacy/service account token use; prefer projected short-lived tokens |

## Create from prompt or file

```bash
kubectl create secret generic app-credentials \
  --from-literal=username=demo-user \
  --from-file=password=./password.txt \
  -n config-lab
```

Avoid putting real secret values directly into shell command arguments: they may be retained in shell history or visible through process inspection. For real environments, use a secure secret-management workflow.

## Declarative example

The sample [`manifests/secret-demo.yaml`](manifests/secret-demo.yaml) contains a fake lab credential only. It demonstrates how Kubernetes serializes `data` values.

## Inspect metadata safely

```bash
kubectl get secrets -n <ns>
kubectl describe secret <name> -n <ns>
```

Avoid `kubectl get secret -o yaml` in shared terminals, logs, recordings, or screenshots because it exposes encoded data.

## References

- [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
- [Secret types](https://kubernetes.io/docs/concepts/configuration/secret/#secret-types)
