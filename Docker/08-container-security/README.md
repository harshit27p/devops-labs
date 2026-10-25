# Container Security: Hardening Docker Workloads

> **Topic:** Non-root users, Linux capabilities, secrets, mount
> security, SELinux/AppArmor, seccomp, and runtime controls\
> **Suggested repository path:** `08-container-security/README.md`

Container security is a layered discipline. A container is not a virtual
machine and should not be treated as a complete security boundary by
itself. Good security combines a minimal image, least privilege, safe
mounts, controlled network exposure, protected secrets, runtime
restrictions, host security controls, patching, and monitoring.

This note builds on the Docker fundamentals, networking, storage, and
Compose notes in this repository. The emphasis here is security
hardening and practical validation---not a repeat of general Docker
usage.

## Table of contents

-   [1. Learning objectives](#1-learning-objectives)
-   [2. Container security model](#2-container-security-model)
-   [3. Run as a non-root user](#3-run-as-a-non-root-user)
-   [4. Linux capabilities and privileged
    mode](#4-linux-capabilities-and-privileged-mode)
-   [5. Read-only filesystems and writable
    paths](#5-read-only-filesystems-and-writable-paths)
-   [6. Mount security and host-path
    risks](#6-mount-security-and-host-path-risks)
-   [7. Secrets and sensitive
    configuration](#7-secrets-and-sensitive-configuration)
-   [8. SELinux and AppArmor](#8-selinux-and-apparmor)
-   [9. Seccomp and runtime security
    options](#9-seccomp-and-runtime-security-options)
-   [10. Resource limits and denial-of-service
    protection](#10-resource-limits-and-denial-of-service-protection)
-   [11. Image and supply-chain
    security](#11-image-and-supply-chain-security)
-   [12. Practical lab: harden a
    container](#12-practical-lab-harden-a-container)
-   [13. Practical lab: apply security controls in
    Compose](#13-practical-lab-apply-security-controls-in-compose)
-   [14. Troubleshooting security
    restrictions](#14-troubleshooting-security-restrictions)
-   [15. Security checklist](#15-security-checklist)
-   [16. Interview questions and
    answers](#16-interview-questions-and-answers)
-   [17. Scope boundaries](#17-scope-boundaries)
-   [18. Official references](#18-official-references)

## 1. Learning objectives

After completing this note, you should be able to:

-   Explain why containers still need layered security controls.
-   Run applications as non-root users.
-   Understand Linux capabilities and why `--privileged` is risky.
-   Restrict writes with read-only root filesystems and carefully chosen
    mounts.
-   Avoid exposing sensitive host paths and the Docker socket.
-   Handle secrets without baking them into images or committing them to
    Git.
-   Understand SELinux, AppArmor, and seccomp at a practical level.
-   Apply runtime restrictions and resource limits.
-   Troubleshoot permission errors without disabling all security
    controls.

## 2. Container security model

A container typically shares the host kernel while using isolation
mechanisms such as namespaces and cgroups. A container escape or a
dangerous configuration can therefore have consequences for the host.
Security should be applied at multiple layers.

``` text
Secure host + patched kernel
          |
Docker daemon access control
          |
Image provenance + vulnerability management
          |
Least privilege: UID/GID + capabilities
          |
Filesystem + mounts + secrets
          |
Network exposure + resource limits
          |
Monitoring + patching + recovery
```

### Core principles

-   **Least privilege:** give a workload only the access it needs.
-   **Defense in depth:** combine controls instead of depending on a
    single setting.
-   **Minimize attack surface:** use maintained base images and avoid
    unnecessary packages.
-   **Secure defaults:** avoid privileged mode, host networking, and
    broad host mounts unless required.
-   **Verify, don't assume:** inspect the actual runtime configuration
    and test the application.
-   **Patch continuously:** update the host, Docker Engine, base images,
    and application dependencies.
-   **Separate responsibilities:** a developer who needs to build an
    image should not automatically need unrestricted host administration
    rights.

### Important distinction

Running a process as UID 0 inside a container is not identical to being
root in every context, because namespaces and other controls can limit
it. However, container root is still a risky default, especially when
combined with extra capabilities, host mounts, privileged mode, or
access to the Docker socket. Prefer a non-root application user.

## 3. Run as a non-root user

### Why non-root matters

If an attacker exploits the application, a non-root process usually has
fewer permissions inside the container than a root process. This does
not eliminate vulnerabilities, but it reduces the potential impact.

### Dockerfile example

``` dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Create an unprivileged user and group.
RUN groupadd --system appgroup \
    && useradd --system --gid appgroup --create-home appuser

COPY --chown=appuser:appgroup app.py /app/app.py

USER appuser:appgroup

EXPOSE 8000
CMD ["python", "/app/app.py"]
```

Notes:

-   `USER` sets the user for subsequent build instructions and the
    default runtime process.
-   `COPY --chown` gives the copied files suitable ownership.
-   The application should not need to write to its code directory.
-   If the application must write files, create a dedicated writable
    directory and assign it appropriate ownership.
-   Ports below 1024 may require additional privileges depending on the
    environment; using an unprivileged application port such as 8000 is
    often simpler.

### Build and verify

``` bash
docker build -t secure-python-app .
docker run -d --name secure-python-app -p 127.0.0.1:8000:8000 secure-python-app
docker exec secure-python-app id
docker inspect --format '{{.Config.User}}' secure-python-app
docker logs secure-python-app
```

The `id` command should show the configured non-root user. The
application must listen on the correct address and port for the example
mapping to work.

Cleanup:

``` bash
docker rm -f secure-python-app
```

### Runtime user override

You can override the configured user:

``` bash
docker run --rm --user 10001:10001 alpine:3.20 id
```

Use a UID/GID that is appropriate for the image and its mounted files.
Numeric IDs are useful when matching ownership across host and
container, but application-specific directory permissions still need to
be configured.

## 4. Linux capabilities and privileged mode

Linux capabilities split traditional root privileges into smaller units.
Docker removes or restricts many capabilities by default, but the exact
set depends on the runtime configuration and version.

### Drop capabilities

Start from a minimal set of privileges:

``` bash
docker run --rm \
  --cap-drop=ALL \
  alpine:3.20 \
  sh -c 'id; echo "Container started with all optional capabilities dropped"'
```

This simple container can run without extra capabilities. Real
applications may require specific capabilities; add them only after
determining the need.

Example of granting one capability:

``` bash
docker run --rm \
  --cap-drop=ALL \
  --cap-add=NET_BIND_SERVICE \
  alpine:3.20 \
  sh -c 'grep Cap /proc/self/status'
```

`NET_BIND_SERVICE` allows binding to privileged ports on Linux in
applicable configurations. Do not add it merely as a habit; prefer an
unprivileged port if that meets the requirement.

### Why `--privileged` is dangerous

``` bash
# Avoid this for ordinary applications:
docker run --privileged ...
```

Privileged mode grants broad device access and substantially relaxes
security restrictions. It can undermine container isolation and expose
the host to serious risk. Do not use it as a quick fix for permission
problems.

Prefer a specific capability, device, mount, or policy adjustment that
solves the actual need.

### Inspect capabilities

``` bash
docker inspect <container_name>
docker exec <container_name> sh -c 'grep Cap /proc/self/status'
```

The capability mask is a bit field, not a friendly list. Use the runtime
inspection output and platform documentation to understand the
configured capabilities.

## 5. Read-only filesystems and writable paths

A read-only container root filesystem can reduce the places where a
compromised application can alter files. Applications may still need
writable temporary storage, caches, sockets, or runtime directories.

### Test with a read-only root filesystem

``` bash
docker run --rm \
  --read-only \
  --tmpfs /tmp:rw,noexec,nosuid,size=64m \
  alpine:3.20 \
  sh -c 'echo "temporary data" > /tmp/example.txt && cat /tmp/example.txt'
```

The write to `/tmp` should succeed because it is a dedicated temporary
filesystem. A write to a normal root filesystem location should fail.

### Common writable locations

Depending on the application, you may need to provide writable mounts
for:

-   `/tmp`
-   An application cache directory.
-   A runtime directory for PID files or Unix sockets.
-   An upload or data directory.
-   A log directory, although sending logs to stdout/stderr is often
    preferable in containers.

Do not make the entire filesystem writable just because one directory
needs writes.

### Compose example

``` yaml
services:
  app:
    image: example/app:1.0
    read_only: true
    tmpfs:
      - /tmp:rw,noexec,nosuid,size=64m
```

This is a pattern, not a ready-to-run image. Confirm the application
supports a read-only root filesystem and add only the writable paths it
genuinely requires.

## 6. Mount security and host-path risks

Mounts can intentionally expose data to containers. A broad or sensitive
host mount can also allow a compromised container to affect the host.

### Prefer read-only bind mounts when possible

``` bash
docker run --rm \
  --mount type=bind,src="$PWD/site",dst=/usr/share/nginx/html,readonly \
  nginx:alpine
```

This example gives Nginx read access to the host's `site` directory.
Ensure the path exists and is readable by the container process.

### Avoid mounting sensitive host paths

Think carefully before mounting paths such as:

-   `/` or large portions of the host filesystem.
-   `/etc`, `/root`, or host credential directories.
-   Host device nodes.
-   Runtime sockets, especially `/var/run/docker.sock`.
-   Directories containing SSH private keys, cloud credentials, or
    production secrets.

### Docker socket warning

Access to the Docker daemon socket is highly privileged. A process that
can control the daemon may be able to start containers with host mounts
or other settings that compromise the host. Do not mount the socket into
an application container unless a carefully reviewed design requires it.

### File ownership and permissions

A container's UID/GID may not match the host user's IDs. A process can
fail to read or write a bind mount even when the path exists.

Check on the host:

``` bash
ls -ld ./data
ls -l ./data
```

Check in the container:

``` bash
docker exec <container_name> id
docker exec <container_name> ls -ld /path/in/container
```

Fix ownership and permissions narrowly. Avoid `chmod -R 777` as a
generic workaround.

### SELinux mount labels

On SELinux-enabled hosts, bind-mount access can be blocked by SELinux
policy even when traditional Unix permissions appear correct. Docker
supports SELinux relabel options such as `:Z` and `:z` for appropriate
bind-mount use cases on supported Linux environments.

-   `:Z` requests a private, container-specific label.
-   `:z` requests a shared label for content intended to be used by
    multiple containers.

Use these options only when appropriate for the host's SELinux
configuration. Relabeling can change host file labels and should not be
applied blindly to system directories or sensitive paths.

## 7. Secrets and sensitive configuration

Secrets include database passwords, API tokens, private keys,
certificates, signing keys, and cloud credentials.

### Never bake secrets into images

Do not put secrets in a Dockerfile:

``` dockerfile
# BAD — secret can remain in image layers/history or build metadata:
# ENV API_TOKEN=real-secret-value
```

Do not copy secret files into an image unless there is a deliberate,
secure image-build design for non-rotating public material. Credentials
should normally be supplied at runtime through a supported
secret-management mechanism.

### Environment variables: convenient, not automatically secret

Example:

``` yaml
services:
  app:
    image: example/app:1.0
    environment:
      APP_MODE: production
```

Environment variables are useful for non-secret configuration. Secrets
passed as environment variables may be visible to processes with
sufficient access, debugging tools, logs, or container inspection
depending on the environment. Avoid treating `.env` as encryption.

### Compose secrets pattern

Compose supports secrets declarations for supported use cases. For a
local file-backed example:

``` yaml
services:
  app:
    image: example/app:1.0
    secrets:
      - db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

The application must know how to read the secret from the location
provided by Compose. Protect the source file and exclude it from version
control:

``` gitignore
.env
secrets/
*.pem
*.key
```

**Important:** Compose secret behavior and implementation vary by
deployment mode and platform. A local file-backed Compose secret is not
the same as an encrypted, centrally managed secret vault. Verify the
official documentation for the environment you deploy to.

### Better secret-handling practices

-   Use a managed secret store or orchestrator secret facility where
    appropriate.
-   Limit who can read secret source files and runtime values.
-   Rotate secrets and revoke credentials that may have leaked.
-   Never commit real secrets to Git, even in a private repository.
-   Keep secret values out of logs, screenshots, shell history, and
    support tickets.
-   Use separate credentials for development, testing, and production.
-   Give application credentials only the permissions they need.

## 8. SELinux and AppArmor

SELinux and AppArmor are Linux Mandatory Access Control (MAC) systems.
They can restrict what a process may access even when traditional Unix
permissions would allow it.

### SELinux overview

SELinux commonly uses labels and policy rules to control access. On
RHEL-family systems, inspect its status:

``` bash
getenforce
sestatus
ls -Z ./data
```

Common modes:

-   `Enforcing`: policy is enforced.
-   `Permissive`: policy violations are logged but not blocked.
-   `Disabled`: SELinux is disabled.

Do not disable SELinux to make a container work unless a deliberate,
approved diagnostic process requires a temporary change. Prefer
correcting labels or policy based on evidence.

Useful diagnostics on supported systems:

``` bash
sudo ausearch -m AVC -ts recent
sudo journalctl -t setroubleshoot --since "15 minutes ago"
```

Availability and exact commands depend on installed packages and
distribution configuration.

### AppArmor overview

AppArmor uses profiles to constrain process behavior. On systems where
AppArmor is enabled:

``` bash
sudo aa-status
docker info
```

Docker may use a default AppArmor profile depending on the host and
runtime configuration. Custom profiles can provide more restrictive
application-specific controls.

### Troubleshooting approach

If access is denied:

1.  Confirm the path and the container's UID/GID.
2.  Check traditional Unix permissions.
3.  Check SELinux labels and audit logs, or AppArmor status/logs.
4.  Review the actual denial before changing policy.
5.  Make the smallest appropriate correction.
6.  Retest the workload under enforcing policy.

Avoid disabling MAC controls or assigning broad labels as a permanent
workaround.

## 9. Seccomp and runtime security options

Seccomp (secure computing mode) restricts which system calls a process
may invoke. Docker uses a default seccomp profile in supported
configurations, but behavior can vary with Docker version, runtime, and
platform.

### Practical guidance

-   Keep the default seccomp profile unless there is a tested reason to
    change it.
-   Do not use `seccomp=unconfined` simply to suppress an error.
-   If an application needs a syscall blocked by policy, identify the
    syscall and assess the risk before changing the profile.
-   Combine seccomp with non-root execution, capabilities reduction,
    filesystem restrictions, and host MAC policy.

Other runtime controls may include:

-   `no-new-privileges`, which helps prevent processes from gaining
    additional privileges through mechanisms such as set-user-ID
    executables.
-   Capability drops.
-   Read-only root filesystem.
-   Explicit devices and mounts.
-   User namespace remapping or rootless Docker, where supported and
    appropriate.

### Example: no-new-privileges

``` bash
docker run --rm \
  --security-opt=no-new-privileges:true \
  alpine:3.20 \
  sh -c 'id'
```

This simple example verifies the container starts with the option
applied; it is not a complete test of every privilege-escalation path.

## 10. Resource limits and denial-of-service protection

A container that can consume excessive CPU, memory, process IDs, or disk
space can affect other workloads or the host. Set limits based on
observed application needs and monitor the result.

### Example

``` bash
docker run -d --name limited-app \
  --memory=256m \
  --cpus=0.50 \
  --pids-limit=100 \
  nginx:alpine
```

Inspect resource usage:

``` bash
docker stats limited-app
docker inspect limited-app
```

Remove the test container:

``` bash
docker rm -f limited-app
```

Considerations:

-   Too-low memory limits can cause out-of-memory kills or unstable
    behavior.
-   CPU limits may increase latency if set too tightly.
-   Process limits can break workloads that legitimately need more
    processes.
-   Disk capacity and log growth also need controls; CPU and memory
    flags do not cap all disk usage.
-   Resource limits do not replace monitoring, alerting, or
    application-level safeguards.

Compose can express resource settings, but supported fields and
enforcement can depend on the Compose implementation and deployment
mode. Validate the rendered configuration and actual runtime behavior.

## 11. Image and supply-chain security

Security begins before a container starts.

### Recommended controls

-   Use trusted, maintained base images.
-   Pin image versions intentionally; use immutable digests where
    reproducibility requirements justify them.
-   Rebuild images to pick up patched base-image packages.
-   Keep the build context small with `.dockerignore`.
-   Avoid embedding build credentials or runtime secrets in image
    layers.
-   Scan images and dependencies for known vulnerabilities.
-   Verify image provenance/signatures when supported by your
    supply-chain process.
-   Generate and retain a software bill of materials (SBOM) where
    useful.
-   Restrict access to image registries and deployment credentials.
-   Remove unnecessary shells, package managers, and tools from runtime
    images when feasible.
-   Separate build and runtime stages where that reduces the production
    attack surface.

Example image inspection:

``` bash
docker image ls
docker image inspect nginx:alpine
docker history nginx:alpine
```

These commands show image metadata and history; they are not
vulnerability scanners. Use a suitable maintained scanner in your
development pipeline and assess findings based on exploitability and
context.

## 12. Practical lab: harden a container

**Goal:** Run a small container with a non-root user, a read-only root
filesystem, dropped capabilities, no-new-privileges, and limited
resources.

### Step 1: Start a hardened diagnostic container

``` bash
docker run -d --name hardened-test \
  --user 10001:10001 \
  --read-only \
  --tmpfs /tmp:rw,noexec,nosuid,size=32m \
  --cap-drop=ALL \
  --security-opt=no-new-privileges:true \
  --memory=128m \
  --cpus=0.50 \
  --pids-limit=64 \
  alpine:3.20 \
  sh -c 'while true; do sleep 3600; done'
```

This is a learning example. The numeric user has no guaranteed name in
the image, and the process is intentionally minimal. Production services
need a suitable user, required writable directories, and
application-specific validation.

### Step 2: Inspect identity and runtime settings

``` bash
docker exec hardened-test id
docker inspect hardened-test
docker stats --no-stream hardened-test
```

Review the inspect output for the configured user, read-only setting,
security options, capabilities, and resource constraints.

### Step 3: Test filesystem behavior

``` bash
# This should normally fail because the root filesystem is read-only:
docker exec hardened-test sh -c 'echo test > /root/test.txt'

# This should succeed because /tmp is writable:
docker exec hardened-test sh -c 'echo test > /tmp/test.txt && cat /tmp/test.txt'
```

A failure to write to `/root` may also involve permissions; the
important test is that a normal root-filesystem path is not writable. Do
not run the test as root inside the container to bypass the intended
user restriction.

### Step 4: Clean up

``` bash
docker rm -f hardened-test
```

### Lab review

Answer these questions in your own words:

1.  Which controls limit the process's identity and privileges?
2.  Why does `/tmp` remain writable?
3.  What changes would be needed for an application that writes to
    `/var/cache/app`?
4.  Why would `--privileged` defeat the purpose of this exercise?
5.  Which checks would you perform on a real application before
    deploying these settings?

## 13. Practical lab: apply security controls in Compose

Use the following as a **configuration template**, not a guaranteed
drop-in configuration for every image. Replace `example/app:1.0` with an
application image that supports non-root execution and read-only
filesystems.

``` yaml
services:
  app:
    image: example/app:1.0
    user: "10001:10001"
    read_only: true
    tmpfs:
      - /tmp:rw,noexec,nosuid,size=64m
    cap_drop:
      - ALL
    security_opt:
      - no-new-privileges:true
    mem_limit: 256m
    cpus: 0.50
    pids_limit: 100
    ports:
      - "127.0.0.1:8080:8080"
    restart: unless-stopped
```

### Validate and inspect

``` bash
docker compose config
docker compose up -d
docker compose ps
docker compose logs -f app
docker inspect <container_name>
```

If the application fails, do not immediately remove all security
controls. Identify the exact requirement:

-   Does it need a writable cache or runtime directory?
-   Does it require a particular capability?
-   Is the port correct?
-   Does the image support the specified UID/GID?
-   Is SELinux/AppArmor denying access?
-   Are the resource limits too low?

Adjust only the relevant control, document why, and test again.

## 14. Troubleshooting security restrictions

### A. `Permission denied`

Check the runtime user and file permissions:

``` bash
docker exec <container_name> id
docker exec <container_name> ls -ld /path/in/container
docker inspect <container_name>
```

Then inspect host-side ownership for bind mounts. Avoid `chmod 777` and
root execution as automatic fixes.

### B. Application fails with a read-only filesystem error

Check whether the application writes to its code directory, `/tmp`, a
cache path, a PID directory, or a log file. Provide a narrowly scoped
writable `tmpfs` or volume only where required. Prefer stdout/stderr for
container logs.

### C. Mount works without SELinux but fails with it enabled

Check SELinux status, file labels, and audit denials. Correct the label
or policy for the intended mount. Do not disable SELinux as a permanent
fix.

### D. Application fails after dropping capabilities

Determine which operation failed and whether the application truly needs
a specific capability. Add only the minimum capability necessary, or
redesign the application to avoid the privileged operation.

### E. Container cannot bind to a low-numbered port

Prefer a high-numbered container port when possible. If the application
must bind a privileged port, evaluate a narrow capability grant such as
`NET_BIND_SERVICE` rather than using privileged mode.

### F. Container is killed or becomes unstable

Check logs, exit status, and resource usage:

``` bash
docker ps -a
docker logs <container_name>
docker inspect <container_name>
docker stats
```

Investigate memory limits, CPU constraints, process limits, and
application-level errors.

### G. Secret appears in an image or Git repository

Treat it as exposed. Revoke or rotate the credential, remove it from
future builds and source control, review access logs, and follow your
repository's secret-remediation procedure. Deleting the latest file or
commit alone may not remove all copies from Git history, clones, caches,
or registry layers.

## 15. Security checklist

Before deploying a container, verify the relevant items:

-   [ ] Base image is trusted, maintained, and intentionally versioned.
-   [ ] Application runs as a non-root user when feasible.
-   [ ] No unnecessary Linux capabilities are granted.
-   [ ] Container is not running in privileged mode without a documented
    need.
-   [ ] Root filesystem is read-only where the application supports it.
-   [ ] Writable directories are limited and explicitly mounted.
-   [ ] Host bind mounts are narrow and read-only where possible.
-   [ ] Docker socket and sensitive host paths are not exposed to the
    workload.
-   [ ] Secrets are not baked into images or committed to Git.
-   [ ] Network ports are published only when required.
-   [ ] SELinux/AppArmor and seccomp protections remain enabled where
    supported.
-   [ ] CPU, memory, process, and storage consumption are considered.
-   [ ] Image and dependencies are scanned and patched.
-   [ ] Logs, monitoring, and incident response are configured.
-   [ ] Backups and recovery are tested for stateful workloads.
-   [ ] Runtime settings are inspected and validated after deployment.

## 16. Interview questions and answers

### 1. Why is running a container as root risky?

A compromised process may have more privileges inside the container. The
risk can increase significantly with privileged mode, broad
capabilities, host mounts, or access to the Docker daemon.

### 2. How do you run a container as a non-root user?

Create a user in the Dockerfile and specify `USER appuser:appgroup`, or
use the runtime `--user` option when appropriate. Ensure application
files and writable paths have suitable ownership.

### 3. What are Linux capabilities?

They divide traditional root privileges into more granular permissions.
A container can drop unnecessary capabilities and add a specific one
only when the workload requires it.

### 4. Why should `--privileged` be avoided?

It grants broad device access and relaxes important isolation controls,
increasing the potential impact of a compromise. Prefer a narrow
capability or specific device permission when justified.

### 5. What does `--read-only` do?

It makes the container's root filesystem read-only. Applications can
still write to explicitly writable mounts or temporary filesystems.

### 6. What is the risk of bind-mounting `/` or `/var/run/docker.sock`?

A broad host mount can expose sensitive host files, and Docker socket
access can allow control over the Docker daemon. Depending on the
configuration, that can enable host-level compromise.

### 7. What is the difference between SELinux and AppArmor?

Both are Linux mandatory access-control systems. SELinux commonly uses
labels and policy rules; AppArmor uses profiles to constrain program
behavior.

### 8. What is seccomp?

A Linux facility that restricts system calls a process can make. Docker
uses a default seccomp profile in supported configurations; avoid
disabling it without a carefully reviewed reason.

### 9. Are environment variables safe for secrets?

Not automatically. They can be exposed through process inspection,
diagnostics, logs, or runtime access. Use an appropriate
secret-management mechanism and restrict access.

### 10. Does a Docker Compose `.env` file encrypt values?

No. It is a text configuration file. Protect it with filesystem
permissions, keep it out of version control, and use a proper secret
manager for production secrets.

### 11. How can a read-only root filesystem still support temporary files?

Mount a dedicated writable temporary filesystem, such as a `tmpfs` at
`/tmp`, and provide other narrowly scoped writable paths if the
application requires them.

### 12. Why can a bind mount fail even if the path exists?

Possible causes include UID/GID mismatch, Unix permissions, SELinux
labels, AppArmor policy, read-only mounts, or an incorrect host path.

### 13. What is `no-new-privileges`?

A runtime security option that prevents a process from gaining
additional privileges through certain privilege-escalation mechanisms,
such as set-user-ID executables.

### 14. How do resource limits improve security?

They reduce the chance that one workload can exhaust host CPU, memory,
or process resources and disrupt other workloads. Limits must be sized
and monitored to avoid harming legitimate service availability.

### 15. Is a container a complete security boundary?

No. Containers share the host kernel in typical configurations.
Isolation depends on namespaces, cgroups, capabilities, MAC policies,
seccomp, runtime configuration, and host security.

### 16. How should you respond to a secret committed to Git?

Assume it may be exposed: revoke or rotate it, investigate usage, remove
it from future content and history where appropriate, and review
registry/build artifacts and cloned copies.

### 17. What should you check if a container works only with privileged mode?

Identify the exact operation that fails. Check permissions,
capabilities, device access, mounts, SELinux/AppArmor, and seccomp.
Replace privileged mode with the narrowest supported permission that
meets the requirement.

### 18. What is image supply-chain security?

It covers the trustworthiness and integrity of base images,
dependencies, build processes, registries, and artifacts. Useful
practices include patching, scanning, provenance verification,
controlled credentials, and reproducible builds.

## 17. Scope boundaries

This README covers container runtime hardening, least privilege, mount
security, secrets, Linux security controls, resource limits, and image
hygiene.

Related topics intentionally reserved for other notes:

-   Docker Compose service orchestration and configuration.
-   Detailed database backup consistency and recovery procedures.
-   Kubernetes Pod Security, NetworkPolicy, Secrets, and admission
    controls.
-   Full host hardening, enterprise SIEM integration, and
    organization-specific compliance frameworks.

## 18. Official references

-   [Docker Engine security](https://docs.docker.com/engine/security/)
-   [Docker run
    reference](https://docs.docker.com/reference/cli/docker/container/run/)
-   [Dockerfile `USER`
    reference](https://docs.docker.com/reference/dockerfile/#user)
-   [Docker Compose file
    reference](https://docs.docker.com/reference/compose-file/)
-   [Docker Compose
    secrets](https://docs.docker.com/compose/how-tos/use-secrets/)
-   [Docker Engine security
    options](https://docs.docker.com/reference/cli/docker/container/run/#security-options)
-   [Docker seccomp
    profiles](https://docs.docker.com/engine/security/seccomp/)
-   [Red Hat SELinux
    documentation](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/)
-   [AppArmor documentation](https://apparmor.net/)

------------------------------------------------------------------------

## Add this note to your GitHub repository

Recommended structure:

``` text
devops-zero-to-hero-notes/
├── 01-containerization-introduction/
├── 02-docker-fundamentals/
├── 03-django-docker/
├── 04-multistage-distroless/
├── 05-docker-storage/
├── 06-docker-networking/
├── 07-docker-compose/
└── 08-container-security/
    └── README.md
```

From the root of your cloned repository:

``` bash
mkdir -p 08-container-security
# Copy this README.md into that directory, then:
git add 08-container-security/README.md
git commit -m "Add container security notes and hardening labs"
git push origin main
```
