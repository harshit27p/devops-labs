# Kubernetes ConfigMaps & Secrets

Advanced, practical notes for managing application configuration and sensitive data in Kubernetes. Covers object design, environment injection, mounted files, update behavior, security controls, encryption, and external secret workflows.

> Prerequisites: [00 — Architecture & Fundamentals](../00-architecture-fundamentals/README.md), [01 — Workloads & Applications](../01-kubernetes-workloads/README.md), and [02 — Networking & Services](../02-networking-services/README.md).

## Learning outcomes

- Separate application configuration from container images.
- Choose between ConfigMaps, Secrets, environment variables, and mounted files.
- Understand immutable objects and configuration rollout patterns.
- Explain Secret types, Base64 encoding, RBAC, encryption at rest, and audit controls.
- Integrate external secret managers using supported controllers or CSI providers.
- Troubleshoot missing keys, stale mounts, environment configuration, and access failures.

## Module map

| File | Coverage |
|---|---|
| [01 Configuration fundamentals](01-configuration-fundamentals.md) | Twelve-factor configuration, object model |
| [02 ConfigMaps](02-configmaps.md) | Creation, data keys, use cases |
| [03 ConfigMap injection](03-configmap-injection.md) | Environment variables, envFrom, command args |
| [04 ConfigMap volumes](04-configmap-volume-mounts.md) | Mounted files, update propagation, subPath |
| [05 Secrets](05-secrets.md) | Secret model, types, creation |
| [06 Secret injection](06-secret-injection.md) | Env vars, file mounts, optional keys |
| [07 Secret security](07-secret-security.md) | Base64, RBAC, encryption, audit |
| [08 Immutable objects](08-immutable-config.md) | Immutable ConfigMaps and Secrets |
| [09 Configuration updates](09-configuration-updates.md) | Restart behavior, rollout patterns |
| [10 External secret management](10-external-secrets.md) | Vault, cloud secret stores, CSI patterns |
| [11 Troubleshooting](11-config-troubleshooting.md) | Diagnosis and recovery |
| [12 Production patterns](12-production-config-patterns.md) | Design checklist and anti-patterns |

## Labs

1. [ConfigMap through environment variables](labs/01-configmap-environment-lab.md)
2. [Mounted configuration and update behavior](labs/02-configmap-volume-lab.md)
3. [Secret injection and access control](labs/03-secret-security-lab.md)
4. [Immutable configuration and rollout](labs/04-immutable-rollout-lab.md)

## Manifests

- `manifests/configmap-app.yaml`
- `manifests/configmap-env-deployment.yaml`
- `manifests/configmap-volume-deployment.yaml`
- `manifests/secret-demo.yaml`
- `manifests/secret-env-deployment.yaml`
- `manifests/immutable-configmap.yaml`

## Security warning

Never commit real passwords, API tokens, private keys, or production Secret values to Git. The sample Secret manifest contains only an explicitly fake lab value to demonstrate Kubernetes encoding. Base64 is encoding, not encryption. Prefer a secret manager or a sealed/encrypted GitOps workflow for real environments.

## Quick start

```bash
kubectl config current-context
kubectl create namespace config-lab
kubectl apply -f manifests/configmap-app.yaml
kubectl get configmap -n config-lab
kubectl describe configmap app-settings -n config-lab
```

## Core principles

1. ConfigMaps are for non-confidential configuration.
2. Secrets are intended for sensitive values, but are not automatically safe merely because they are Secret objects.
3. Base64 is not encryption.
4. Restrict Secret access using least-privilege RBAC.
5. Enable and verify encryption at rest for the Kubernetes datastore.
6. Avoid exposing secrets through logs, shell history, process arguments, or broad environment dumps.
7. Plan how applications reload configuration; mounted file updates do not automatically guarantee application reload.
8. Prefer immutable, versioned configuration for reproducible deployments where appropriate.

## Official references

- [ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/)
- [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
- [Configure a Pod to use a ConfigMap](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/)
- [Good practices for Kubernetes Secrets](https://kubernetes.io/docs/concepts/security/secrets-good-practices/)
- [Encrypting Confidential Data at Rest](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/)
