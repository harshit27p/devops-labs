# Introduction to Containerization --- DevOps Notes

> **Video:** [Day-23 \| Introduction to Containers --- Abhishek
> Veeramalla](https://www.youtube.com/watch?v=7JZP345yVjw)\
> **Playlist:** [Complete DevOps
> Course](https://www.youtube.com/playlist?list=PLdpzxOOAlwvIc1TjTwopNSjRJkzES2ZXk)\
> **Purpose:** Understand *why* containerization exists, how it differs
> from virtual machines, the basic Docker image lifecycle, and where
> Buildah and OCI fit into the container ecosystem.

These notes combine the video's main ideas with additional technical
context and practical learning checkpoints. The later sections introduce
advanced concepts only at a high level; detailed Docker commands,
Dockerfiles, storage, networking, Compose, and orchestration should live
in separate topic folders so the repository does not repeat itself.

------------------------------------------------------------------------

## Table of contents

-   [1. Learning objectives](#1-learning-objectives)
-   [2. Why containerization was
    needed](#2-why-containerization-was-needed)
-   [3. Virtualization: physical servers to
    VMs](#3-virtualization-physical-servers-to-vms)
-   [4. What is a container?](#4-what-is-a-container)
-   [5. Virtual machines vs
    containers](#5-virtual-machines-vs-containers)
-   [6. How containers work under
    Linux](#6-how-containers-work-under-linux)
-   [7. Docker and its architecture](#7-docker-and-its-architecture)
-   [8. The Docker image lifecycle](#8-the-docker-image-lifecycle)
-   [9. Images, layers, containers, and
    registries](#9-images-layers-containers-and-registries)
-   [10. Docker Engine availability and the SPOF
    discussion](#10-docker-engine-availability-and-the-spof-discussion)
-   [11. Buildah and daemonless image
    building](#11-buildah-and-daemonless-image-building)
-   [12. OCI: portability standards](#12-oci-portability-standards)
-   [13. Containerization in real DevOps
    workflows](#13-containerization-in-real-devops-workflows)
-   [14. Security and production
    considerations](#14-security-and-production-considerations)
-   [15. Hands-on learning lab](#15-hands-on-learning-lab)
-   [16. Troubleshooting starting
    points](#16-troubleshooting-starting-points)
-   [17. Interview questions and
    answers](#17-interview-questions-and-answers)
-   [18. Key takeaways](#18-key-takeaways)
-   [19. Suggested next topics](#19-suggested-next-topics)
-   [20. References](#20-references)

------------------------------------------------------------------------

## 1. Learning objectives

After studying these notes, you should be able to:

1.  Explain the resource-utilization problem that virtualization
    addressed and the remaining overhead that containers can reduce.
2.  Compare VMs and containers without claiming that one replaces the
    other in every scenario.
3.  Explain the relationship between a Dockerfile, an image, a
    container, and a registry.
4.  Describe Docker's client/daemon architecture and why the daemon is
    an operational dependency.
5.  Explain what Buildah does and why daemonless image building can be
    useful.
6.  Recognize the role of OCI specifications in container image and
    runtime interoperability.
7.  Identify the main security, persistence, and reliability concerns
    before using containers in production.

## 2. Why containerization was needed

### The deployment problem

An application rarely consists of source code alone. It may depend on a
language runtime, system libraries, certificates, configuration, and
particular package versions. Installing these dependencies manually on
every server can lead to inconsistent environments.

Typical problems include:

-   **Environment drift:** development, test, and production machines
    have different packages or configuration.
-   **Dependency conflicts:** two applications require incompatible
    versions of the same library.
-   **Slow provisioning:** setting up each new server takes time and
    manual effort.
-   **Difficult rollback:** restoring a previous working combination of
    application and dependencies is error-prone.
-   **Poor utilization:** a server assigned to one workload may have
    significant unused CPU or memory.

Containerization packages an application with its required user-space
dependencies into a standardized image. That image can be distributed
and started on compatible container hosts.

### A simplified evolution

``` text
Physical server
    |
    v
Virtualization: multiple virtual machines on one host
    |
    v
Containerization: isolated application environments share a host kernel
    |
    v
Orchestration: coordinate many containers across hosts
```

This is an evolution of deployment approaches, not a rule that every
organization must use every layer. VMs remain valuable, and containers
commonly run *inside* VMs.

## 3. Virtualization: physical servers to VMs

A hypervisor allows multiple virtual machines to share one physical
server. Each VM has virtual hardware and its own guest operating system.

``` text
Physical hardware
└── Hypervisor
    ├── VM 1: Guest OS + Application A
    ├── VM 2: Guest OS + Application B
    └── VM 3: Guest OS + Application C
```

### Benefits of VMs

-   Strong isolation boundary compared with ordinary shared-kernel
    containers.
-   Different guest operating systems can run on the same physical host,
    subject to hypervisor support.
-   Independent guest kernels and OS-level configuration.
-   Useful for legacy applications, infrastructure services, and
    security boundaries.

### Costs and trade-offs

Every VM needs memory and disk space for its guest OS, and guest
operating systems need patching and administration. Startup and
provisioning are generally heavier than starting a container, though
actual performance depends on the workload and platform.

**Important distinction:** unused resources are not automatically wasted
just because they are allocated to a VM. The problem is that workloads
may not use all the capacity provisioned for them, while each VM still
carries guest-OS overhead.

## 4. What is a container?

A **container** is an isolated process environment created using
operating-system features. A container image packages an application and
its user-space dependencies; a container is a running (or stopped)
instance created from an image plus runtime configuration.

A typical application image can contain:

-   Application code and executable files
-   Language runtime, such as Python, Node.js, or Java
-   Required user-space libraries and tools
-   Default configuration and startup command

It does **not** normally contain a separate booted guest kernel. On a
Linux container host, containers share the host's Linux kernel while
receiving isolated views of selected resources.

### Why containers are useful

-   **Consistency:** the same image can be tested and promoted between
    environments.
-   **Portability:** an image can run on compatible hosts that support
    its required architecture and runtime features.
-   **Speed:** containers usually start faster than full VMs because
    they do not boot a guest OS.
-   **Density:** multiple isolated workloads can share a host kernel.
-   **Repeatability:** an image tag or digest provides a reference to a
    defined build artifact.
-   **Automation:** container images fit naturally into CI/CD pipelines.

### What portability does not mean

A container is not universally runnable on every device. CPU
architecture, operating-system kernel features, image format, runtime
support, networking, external services, and permissions still matter. A
Linux image generally needs a Linux kernel environment; on Windows or
macOS, Docker Desktop commonly supplies a Linux VM for Linux containers.

## 5. Virtual machines vs containers

  -----------------------------------------------------------------------
  Area                    Virtual machine         Container
  ----------------------- ----------------------- -----------------------
  Isolation model         Virtual hardware and    Process isolation with
                          separate guest kernel   shared host kernel in
                                                  common Linux setups

  OS                      Each VM runs a guest OS Packages user space;
                                                  does not usually boot
                                                  its own kernel

  Startup                 Usually heavier         Usually lighter and
                                                  faster

  Resource footprint      Includes guest OS       Often smaller,
                          overhead                depending on image and
                                                  workload

  Kernel choice           Guest kernel can differ Must be compatible with
                          from host kernel        the host kernel
                                                  environment

  Density                 Often fewer instances   Often higher workload
                          per host for comparable density
                          small workloads         

  Security boundary       Often stronger by       Shared-kernel risks
                          default for kernel      require careful
                          separation              hardening

  Best fit                OS diversity, strong    Repeatable app
                          isolation, legacy       packaging,
                          workloads               microservices, CI/CD

  Relationship            Can host container      Commonly deployed
                          platforms               inside VMs
  -----------------------------------------------------------------------

Neither technology is universally superior. A common production design
is to use VMs for infrastructure boundaries and run containers inside
them.

## 6. How containers work under Linux

Containers are not simply small VMs. They are processes isolated and
constrained using kernel capabilities.

### Linux namespaces --- isolation

Namespaces control what a process can see. Common examples include:

-   **PID namespace:** process ID visibility.
-   **Network namespace:** network interfaces, routes, and related
    network state.
-   **Mount namespace:** filesystem mount view.
-   **UTS namespace:** hostname and domain-name view.
-   **IPC namespace:** inter-process communication resources.
-   **User namespace:** user and group ID mappings.

### cgroups --- resource accounting and limits

Control groups (cgroups) let the system account for and limit resources
such as CPU and memory, depending on the cgroup version and
configuration. They help prevent one workload from consuming all host
resources.

### Additional security controls

-   **Linux capabilities:** split traditional root privileges into more
    granular permissions.
-   **seccomp:** restricts the system calls a process may make.
-   **SELinux/AppArmor:** mandatory access-control systems that can
    restrict processes.
-   **Namespaces and cgroups:** provide isolation and resource control
    but are not, by themselves, a complete security solution.

Conceptually:

``` text
Container process
├── Namespaces: what the process can see
├── cgroups: resource accounting and limits
├── Capabilities / seccomp: privilege and syscall restrictions
├── SELinux / AppArmor: additional access controls
└── Host Linux kernel: shared kernel in a normal Linux container setup
```

This is a conceptual view. Actual implementation details vary by
runtime, kernel, distribution, and configuration.

## 7. Docker and its architecture

Docker is a platform and toolset for building, distributing, and running
containers. It is not the same thing as a container itself.

A simplified Docker Engine workflow:

``` text
Developer / CI pipeline
        |
        v
Docker CLI (docker build / pull / run)
        |
        | Docker API
        v
Docker daemon (dockerd)
        |
        +--> Build images
        +--> Manage containers
        +--> Manage networks and volumes
        |
        v
Container runtime and Linux kernel facilities
```

The Docker client sends requests to the Docker daemon. The daemon
manages Docker objects, including images, containers, networks, and
volumes. A registry stores and distributes images; Docker Hub is one
public registry option. See the official Docker overview in the
references.

### Important terms

-   **Docker CLI:** command-line client used to send requests.
-   **Docker daemon (`dockerd`):** background service that manages
    Docker objects.
-   **Docker Engine:** the Docker engine components used to build and
    run containers.
-   **Container runtime:** software involved in creating and running
    container processes.
-   **Registry:** service for storing and distributing container images.
-   **Docker Compose:** tool for defining and running multi-container
    applications; detailed usage belongs in a later section of your
    notes.

Docker Desktop on macOS and Windows generally uses a managed Linux
environment for Linux containers. This explains why the kernel used by a
Linux container is not simply the native Windows or macOS kernel.

## 8. The Docker image lifecycle

The core workflow introduced in the video is:

``` text
Dockerfile
   |
   | docker build
   v
Image
   |
   | docker run
   v
Container
```

### Step 1 --- Write a Dockerfile

A Dockerfile is a text file containing instructions for building an
image. It commonly specifies a base image, working directory,
dependencies, application files, and the default startup command.

### Step 2 --- Build an image

The build process evaluates the Dockerfile and build context to produce
an image.

``` bash
docker build -t demo-app:1.0 .
```

-   `-t demo-app:1.0` assigns a name and tag.
-   `.` selects the current directory as the build context.

### Step 3 --- Run a container

``` bash
docker run --name demo-container demo-app:1.0
```

This creates and starts a container from the image, subject to the
selected command and configuration. For a web application, port
publishing may also be needed.

### Step 4 --- Inspect and manage

``` bash
docker image ls
docker ps
docker ps -a
docker logs demo-container
docker inspect demo-container
docker stop demo-container
docker rm demo-container
```

These commands are a preview only. Keep the full command reference in a
separate `docker-fundamentals` topic so that it can expand without
bloating the introductory notes.

## 9. Images, layers, containers, and registries

### Image

An image is an immutable-style template used to create containers. It
includes metadata and filesystem content. Images are commonly assembled
from reusable layers.

### Layer

A layer represents filesystem changes associated with an image build.
Reusing unchanged layers can reduce build time and repeated downloads. A
layer is not the same thing as a complete VM disk.

**A practical nuance about "too many layers":** layer count alone is not
a reliable measure of image quality. Large files, duplicated
dependencies, poor cache ordering, and unnecessary build tools are often
more important. Some changes also create new layers without removing
data stored in earlier layers. Multi-stage builds and good build
practices help keep the final image lean.

### Container

A container is an instance created from an image plus configuration. Its
writable container layer is generally ephemeral: deleting the container
can remove changes stored only in that layer. Data that must survive
container replacement should use appropriate persistent storage, such as
a volume or an external data service.

### Registry

A registry stores and distributes images. A team can pull a tested image
onto a deployment host rather than rebuilding the application
independently on every server.

Typical image path:

``` text
Source code
  -> Build image
  -> Test image
  -> Tag image
  -> Push to registry
  -> Pull on target environment
  -> Run container
```

In a production pipeline, use controlled tags and preferably record the
image digest so the deployed artifact can be identified precisely.

## 10. Docker Engine availability and the SPOF discussion

The video raises the **single point of failure (SPOF)** concern: if a
central component is unavailable, operations that depend on it may be
disrupted.

In a conventional single-host Docker setup, the Docker daemon is an
important management dependency. If it fails, commands that rely on the
daemon cannot operate normally, and recovery or orchestration may be
affected.

### Important technical qualification

It is too broad to say that *all running containers always stop whenever
the Docker daemon goes down*. Docker's default behavior is to shut down
running containers when the daemon terminates, but Docker supports a
**live-restore** option for keeping standalone Linux containers running
during certain daemon outages. Live restore has limitations and does not
remove every host-level failure mode.

Read the official live-restore documentation before treating it as an
availability guarantee.

### Reliability practices

-   Configure and test an appropriate restart policy.
-   Use health checks and monitoring.
-   Keep application data outside the disposable container layer.
-   Automate recovery and redeployment.
-   Avoid treating one container or one host as the entire
    high-availability strategy.
-   Use an orchestrator when the application needs scheduling,
    rescheduling, scaling, and multi-host recovery.
-   Understand the failure domains: application process, container,
    daemon, host, storage, network, and region.

A daemonless image builder addresses the **image-building workflow**,
not every runtime-availability concern. Buildah does not, by itself,
provide high availability for running applications.

## 11. Buildah and daemonless image building

**Buildah** is an open-source tool for building OCI-compatible container
images. It can build images from a `Dockerfile` or `Containerfile`, as
well as through lower-level commands for working with image filesystems
and configuration.

### Why it matters

A Docker-based workflow often uses the Docker daemon to coordinate image
builds. Buildah can build images without requiring a long-running Docker
daemon for that image-building workflow. This can be useful in Linux
automation, build systems, and environments designed around daemonless
tools.

### Example workflow

On a supported Linux system where Buildah is installed:

``` bash
# Build from a Dockerfile or Containerfile
buildah bud -t demo-app:1.0 .

# List locally available images
buildah images

# Inspect Buildah's available commands
buildah --help
```

`buildah bud` is a commonly used alias for building from a Dockerfile;
`buildah build` is also available in current documentation. Consult the
documentation for your installed version.

### Docker and Buildah are not identical

  -----------------------------------------------------------------------
  Topic                   Docker workflow         Buildah workflow
  ----------------------- ----------------------- -----------------------
  Main role               Broad container         Primarily image
                          development and runtime building and image
                          platform                manipulation

  Image build             Commonly through Docker Can build without a
                          Engine / BuildKit       long-running Docker
                                                  daemon

  Run containers          Docker CLI/Engine       Often paired with
                          provides a familiar run Podman or another
                          lifecycle               runtime tool

  Build instructions      Dockerfile              Dockerfile or
                                                  Containerfile

  Interoperability        Supports OCI-compatible Builds OCI images and
                          image workflows         supports common
                                                  container image
                                                  workflows
  -----------------------------------------------------------------------

### Does Buildah eliminate all Docker limitations?

No. It offers an alternative image-building approach and can avoid
dependence on a Docker daemon for that task. It does not eliminate the
need for a runtime, solve every image-size issue automatically, or
guarantee that the resulting application is highly available.

Buildah, Podman, and Skopeo are commonly encountered in the same
ecosystem but have different roles:

-   **Buildah:** build and modify images.
-   **Podman:** run and manage containers and pods, with a daemonless
    architecture for many workflows.
-   **Skopeo:** inspect, copy, and move container images between
    registries and storage locations.

## 12. OCI: portability standards

The **Open Container Initiative (OCI)** maintains open specifications
that help different container tools interoperate.

The main specifications are:

-   **Image Specification:** defines the structure and contents of an
    OCI image, including manifests, configuration, and filesystem
    layers.
-   **Runtime Specification:** defines how to configure and run a
    container from an unpacked filesystem bundle.
-   **Distribution Specification:** defines protocols for distributing
    container images through registries.

Why OCI matters:

1.  Teams are less dependent on a single tool's private image format.
2.  Build, registry, and runtime tools can interoperate when they
    support the relevant specifications.
3.  Images can be built with one compatible tool and run using another
    compatible runtime.

OCI compatibility does not mean every tool has identical features or
that every image will run on every operating system. CPU architecture,
kernel requirements, runtime configuration, and tool-specific behavior
still matter.

## 13. Containerization in real DevOps workflows

Containerization is useful because it creates a repeatable artifact that
can move through a delivery pipeline.

``` text
Developer commit
      |
      v
CI: test source code
      |
      v
Build image
      |
      v
Scan and test image
      |
      v
Push image to registry
      |
      v
Deploy the same image to an environment
      |
      v
Observe health, logs, and metrics
```

### Benefits for CI/CD

-   Build once and promote the same artifact through environments.
-   Reduce "works on my machine" differences.
-   Version application artifacts and support controlled rollbacks.
-   Make deployment steps automatable.
-   Separate build-time dependencies from runtime requirements.

### What containers do not solve automatically

Containers do not automatically provide secrets management, persistent
storage, service discovery, load balancing, zero-downtime deployments,
backups, or multi-host scheduling. Those capabilities require explicit
design and supporting tools.

## 14. Security and production considerations

Containerization is a packaging and isolation mechanism, not a
substitute for security engineering.

### Image security

-   Prefer trusted, maintained base images.
-   Minimize unnecessary packages and files.
-   Rebuild images to incorporate security updates.
-   Scan images and dependencies.
-   Pin versions or digests when reproducibility requires it.
-   Never bake credentials, private keys, or tokens into images.
-   Use `.dockerignore` to keep secrets and irrelevant files out of the
    build context.

### Runtime security

-   Run as a non-root user where practical.
-   Drop unnecessary Linux capabilities.
-   Avoid privileged mode unless there is a justified requirement.
-   Apply CPU and memory limits.
-   Use read-only filesystems where appropriate.
-   Apply SELinux/AppArmor and seccomp policies where supported.
-   Limit access to the container engine socket; access to it can confer
    powerful host-level control.
-   Keep the host kernel and container tooling patched.

### Reliability

-   Keep persistent data outside the container's writable layer.
-   Make applications handle termination signals and shut down
    gracefully.
-   Use health checks and monitoring.
-   Design for container replacement rather than depending on manual
    changes inside a running container.
-   Test backup and recovery, not only initial deployment.

For detailed build optimization and secure Dockerfile practices, create
a separate note linked from the next-topic section rather than repeating
all those instructions here.

## 15. Hands-on learning lab

This lab demonstrates the difference between a reusable image and a
container instance. Run it only in a development environment where
Docker is installed and working.

### Lab A --- Run a published image

``` bash
docker pull hello-world
docker image ls
docker run --name hello-demo hello-world
docker ps -a
docker inspect hello-demo
docker rm hello-demo
```

**Observe:** the image can remain locally available after the container
is removed. The container is an instance; the image is the reusable
template.

### Lab B --- Build your own tiny image

Create a folder named `container-intro-lab`, then create a file named
`Dockerfile` inside it:

``` dockerfile
FROM alpine:3.21
CMD ["sh", "-c", "echo Hello from a container; sleep 5"]
```

Build and run:

``` bash
docker build -t intro-demo:1.0 .
docker image ls
docker run --name intro-demo intro-demo:1.0
docker ps -a
docker logs intro-demo
docker rm intro-demo
```

The container may exit after the command finishes. This is normal: a
container's main process determines whether it remains running.

For reproducible or production builds, review base-image pinning and
update practices before using this sample as a deployment image.

### Lab C --- Compare Docker and Buildah

On a supported Linux host with Buildah installed, run:

``` bash
buildah bud -t intro-demo-buildah:1.0 .
buildah images
```

The same Dockerfile can often be used by both builders. Verify the
output and behavior in your environment rather than assuming all flags
and runtime behaviors are identical.

### Lab questions

1.  What remains after a container is removed: the image, the container,
    or both?
2.  Why does a container usually start faster than a VM?
3.  Which host resource do ordinary Linux containers share?
4.  What is the difference between a Dockerfile and an image?
5.  Why might a build pipeline choose Buildah?
6.  Why is daemonless image building not the same as high availability?
7.  What data would be lost if an application stored important files
    only in the container writable layer?

## 16. Troubleshooting starting points

  -----------------------------------------------------------------------
  Symptom                             First checks
  ----------------------------------- -----------------------------------
  Docker CLI cannot connect           Check whether Docker Desktop or the
                                      Docker daemon is running and
                                      whether the CLI context is correct.

  Image build fails                   Read the first failing build step,
                                      verify the build context,
                                      Dockerfile syntax, network access,
                                      and package repositories.

  Image pull fails                    Check the image name/tag, registry
                                      connectivity, authentication, and
                                      rate limits.

  Container exits immediately         Check `docker ps -a`,
                                      `docker logs <name>`, the startup
                                      command, and the exit code.

  Application is unreachable          Check process health, port
                                      publishing, application bind
                                      address, host firewall, and network
                                      rules.

  Data disappears after recreation    Check whether data was stored only
                                      in the container writable layer
                                      rather than persistent storage.

  Permission denied                   Check the container user, file
                                      ownership, mounted paths,
                                      SELinux/AppArmor policy, and
                                      required capabilities.

  Buildah cannot build                Check Buildah installation/version,
                                      storage configuration, registry
                                      authentication, build context, and
                                      command syntax.
  -----------------------------------------------------------------------

Avoid troubleshooting by blindly adding privileged mode or disabling
security controls. Identify the failing layer first.

## 17. Interview questions and answers

**1. What is containerization?**\
Containerization packages an application and its user-space dependencies
into an image that can run as an isolated process on a compatible host.

**2. Why are containers generally lighter than VMs?**\
Typical containers do not boot a separate guest kernel. They use the
host kernel and isolate processes using OS-level mechanisms.

**3. Do containers include an operating system?**\
Images often contain a user-space filesystem and libraries that resemble
a distribution's root filesystem, but ordinary Linux containers do not
boot their own independent kernel.

**4. Can Linux containers run directly on a Windows kernel?**\
Linux containers need a Linux kernel environment. Docker Desktop
generally supplies a Linux VM for this purpose on Windows and macOS.

**5. What is the difference between a Dockerfile, image, and
container?**\
A Dockerfile describes build instructions; an image is the built
artifact; a container is an instance created from an image and runtime
configuration.

**6. What does a container registry do?**\
It stores and distributes images so developers and deployment systems
can pull specific artifacts.

**7. What are image layers?**\
They are reusable filesystem changes that contribute to an image. Layer
reuse can improve build and distribution efficiency.

**8. What is the Docker daemon?**\
It is the background service that handles Docker API requests and
manages Docker resources.

**9. Is the Docker daemon always a single point of failure for running
containers?**\
It is an important management dependency, but the exact impact depends
on configuration. Docker's default behavior stops containers when the
daemon terminates; live restore can keep eligible standalone Linux
containers running during certain daemon outages.

**10. What is Buildah?**\
Buildah is a tool for building and modifying container images, including
OCI-compatible images, without requiring a long-running Docker daemon
for its build workflow.

**11. What is OCI?**\
The Open Container Initiative maintains specifications for container
image formats, runtime configuration, and image distribution.

**12. Are containers as isolated as VMs?**\
Ordinary Linux containers share a kernel, while VMs generally have
separate guest kernels. The isolation properties and risks differ; the
correct choice depends on the threat model and workload.

**13. Are containers persistent by default?**\
A container's writable layer is normally tied to the container
lifecycle. Important data should use volumes or external persistent
services.

**14. Does a smaller image automatically mean a secure image?**\
No. Size reduction can help reduce unnecessary packages and attack
surface, but trust, patching, vulnerability management, runtime
privileges, secrets, and configuration also matter.

**15. Why use containers in CI/CD?**\
They provide a repeatable artifact that can be tested, versioned, stored
in a registry, and promoted through deployment environments.

## 18. Key takeaways

-   Virtualization improved hardware utilization by allowing multiple
    VMs to share a physical host.
-   Containers reduce per-workload overhead by sharing a host kernel in
    common Linux deployments.
-   VMs and containers are complementary technologies with different
    isolation and operational trade-offs.
-   A Dockerfile describes a build; an image is the artifact; a
    container is an instance.
-   Docker's client and daemon architecture is important for
    understanding management and availability.
-   Buildah provides a daemonless image-building option; it is not a
    complete replacement for every Docker capability.
-   OCI specifications help different tools exchange and run container
    images.
-   Production containers still need security controls, persistent
    storage, observability, and a recovery strategy.

## 19. Suggested next topics

To keep this repository non-repetitive, put each detailed subject in its
own folder:

1.  **Docker fundamentals:** installation, CLI commands, container
    lifecycle, image pulls, tags, logs, inspect, exec, and cleanup.
2.  **Dockerfiles and image builds:** instruction reference, build
    context, layer caching, `.dockerignore`, multi-stage builds, image
    size and build secrets.
3.  **Docker storage:** writable layers, bind mounts, volumes,
    persistence, backup, and restore.
4.  **Docker networking:** bridge networks, port publishing, DNS,
    service-to-service communication, and troubleshooting.
5.  **Docker Compose:** multi-container development environments,
    dependencies, configuration, and lifecycle.
6.  **Container security:** non-root users, capabilities, seccomp,
    SELinux/AppArmor, secrets, scanning, and supply-chain integrity.
7.  **Buildah, Podman, and Skopeo:** compare tool roles and
    build/run/copy workflows.
8.  **Kubernetes introduction:** why orchestration becomes useful when
    workloads span multiple hosts.

Each later README should link back to this introduction for the "why
containers?" explanation rather than repeating it.

## 20. References

### Video and course

-   [Abhishek Veeramalla --- Day-23: Introduction to
    Containers](https://www.youtube.com/watch?v=7JZP345yVjw)
-   [Abhishek Veeramalla --- DevOps course
    playlist](https://www.youtube.com/playlist?list=PLdpzxOOAlwvIc1TjTwopNSjRJkzES2ZXk)

### Official technical documentation

-   [Docker overview and
    architecture](https://docs.docker.com/get-started/docker-overview/)
-   [Docker live
    restore](https://docs.docker.com/engine/daemon/live-restore/)
-   [Docker build best
    practices](https://docs.docker.com/build/building/best-practices/)
-   [Docker multi-stage
    builds](https://docs.docker.com/get-started/docker-concepts/building-images/multi-stage-builds/)
-   [Buildah project](https://buildah.io/)
-   [Buildah documentation](https://github.com/containers/buildah)
-   [Open Container Initiative](https://opencontainers.org/)
-   [OCI image
    specification](https://github.com/opencontainers/image-spec)
-   [OCI runtime
    specification](https://github.com/opencontainers/runtime-spec)
-   [OCI distribution
    specification](https://github.com/opencontainers/distribution-spec)

------------------------------------------------------------------------

## Notes and attribution

These are original study notes based on the video's subject and the
linked technical documentation, not a verbatim transcript. Refer to the
original video and official documentation for context, version-specific
details, and updates.

**Suggested repository path:**
`01-containerization-introduction/README.md`
