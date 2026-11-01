# 07 — SecurityContext and Container Hardening

SecurityContext configures security-related settings for a Pod or container.

## Common controls
- `runAsNonRoot`, `runAsUser`, `runAsGroup`
- `allowPrivilegeEscalation: false`
- `readOnlyRootFilesystem: true`
- `capabilities.drop: ["ALL"]`
- Add back only explicitly required capabilities.
- `seccompProfile: RuntimeDefault`
- `privileged: false`
- Avoid host PID, IPC, and network namespaces unless required.

## Example
See `manifests/hardened-pod.yaml`.

## Pod-level vs container-level
Pod-level `securityContext` applies supported settings to containers in the Pod. Container-level settings can override or add container-specific controls. Validate field support and interactions for the Kubernetes version and runtime.

## Read-only root filesystem
Applications may still need writable temporary paths. Mount bounded `emptyDir` volumes at explicitly required paths rather than making the entire root filesystem writable.

## Linux capabilities
Capabilities split traditionally broad root privileges into smaller units. Dropping all capabilities is a strong baseline, but applications may need a specific capability such as `NET_BIND_SERVICE`. Do not add capabilities without a clear requirement.

## Runtime profile
Use `RuntimeDefault` seccomp where supported. AppArmor and SELinux integration varies by node OS/runtime and Kubernetes version; follow the distribution documentation.

## Validation
Run a staging test and inspect logs, file writes, port binding, and health checks before applying restrictive settings to production.
