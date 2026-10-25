# Docker Zero to Hero --- Part 1: Fundamentals, Installation, Build, Run & Push

> **Video:** [Day-24 \| Docker Zero to Hero Part-1 --- Abhishek
> Veeramalla](https://www.youtube.com/watch?v=wodLpta-hoQ)\
> **Playlist:** [DevOps Zero to
> Hero](https://www.youtube.com/playlist?list=PLdpzxOOAlwvIc1TjTwopNSjRJkzES2ZXk)\
> **Suggested path:** `02-docker-fundamentals/README.md`\
> **Prerequisites:** Basic Linux commands and the concepts in
> [`01-containerization-introduction`](../01-containerization-introduction/README.md).

These notes expand the video's practical Docker workflow with current
official documentation, troubleshooting, security guidance, and reusable
examples. To keep the playlist notes non-repetitive, the
VM-versus-container comparison is summarized here and explained in depth
in the containerization introduction. Advanced image optimization and
multi-stage builds belong in a dedicated follow-up note.

------------------------------------------------------------------------

## Table of contents

-   [1. Learning outcomes and scope](#1-learning-outcomes-and-scope)
-   [2. Docker in one picture](#2-docker-in-one-picture)
-   [3. Core Docker terminology](#3-core-docker-terminology)
-   [4. Docker architecture and request
    flow](#4-docker-architecture-and-request-flow)
-   [5. Docker image lifecycle](#5-docker-image-lifecycle)
-   [6. Lab prerequisites: Ubuntu on AWS
    EC2](#6-lab-prerequisites-ubuntu-on-aws-ec2)
-   [7. Install Docker Engine on
    Ubuntu](#7-install-docker-engine-on-ubuntu)
-   [8. Start, verify, and inspect
    Docker](#8-start-verify-and-inspect-docker)
-   [9. Run your first container](#9-run-your-first-container)
-   [10. Create a Python application](#10-create-a-python-application)
-   [11. Write a Dockerfile](#11-write-a-dockerfile)
-   [12. Build, tag, and run the image](#12-build-tag-and-run-the-image)
-   [13. Docker Hub: publish and pull an
    image](#13-docker-hub-publish-and-pull-an-image)
-   [14. Docker CLI command reference](#14-docker-cli-command-reference)
-   [15. Common errors and
    troubleshooting](#15-common-errors-and-troubleshooting)
-   [16. Security and operational best
    practices](#16-security-and-operational-best-practices)
-   [17. Hands-on assignment](#17-hands-on-assignment)
-   [18. Interview questions and
    answers](#18-interview-questions-and-answers)
-   [19. What belongs in later notes](#19-what-belongs-in-later-notes)
-   [20. References](#20-references)

------------------------------------------------------------------------

## 1. Learning outcomes and scope

After completing this note, you should be able to:

1.  Describe Docker's client, daemon, image, container, and registry
    roles.
2.  Install Docker Engine on a supported Ubuntu EC2 instance using
    Docker's official APT repository.
3.  Understand why `sudo docker ...` works when an unprivileged Docker
    command returns a permission error.
4.  Package a small Python application into a Docker image.
5.  Build and run the image, inspect its output, and distinguish an
    image from a container instance.
6.  Tag an image using a Docker Hub namespace and push it to a registry.
7.  Diagnose common installation, permission, build, and registry
    problems.
8.  Apply safe defaults when exposing a container or publishing an
    image.

**Scope boundary:** This is the Docker fundamentals and first-image
workflow note. It does not attempt to fully teach multi-stage builds,
image-size optimization, volumes, networking, Compose, or Kubernetes;
those deserve separate notes.

## 2. Docker in one picture

Docker provides tools and workflows for building, distributing, and
running containers. Containers share the host kernel in common Linux
setups; see the [containerization
introduction](../01-containerization-introduction/README.md) for the
deeper operating-system explanation.

``` text
Application source + dependencies
              |
              v
          Dockerfile
              |
          docker build
              |
              v
          Docker image
              |
          docker run
              |
              v
        Container process
              |
       logs / inspect / stop
```

A team can publish a built image to a registry and then pull the same
artifact on another compatible host. That is useful for repeatable
deployment and CI/CD.

## 3. Core Docker terminology

  -------------------------------------------------------------------------
  Term                    Meaning                 Example
  ----------------------- ----------------------- -------------------------
  Docker CLI / client     Command-line tool that  `docker build`,
                          sends requests to       `docker run`
                          Docker's API            

  Docker daemon           Background service that Docker Engine service
  (`dockerd`)             manages Docker objects  

  Docker Engine           Docker's engine         Docker Engine on Ubuntu
                          components for building 
                          and managing containers 

  Dockerfile              Text instructions for   `FROM`, `COPY`, `CMD`
                          building an image       

  Image                   Built artifact used to  `python-demo:1.0`
                          create containers       

  Container               An instance created     `python-demo-container`
                          from an image and       
                          runtime configuration   

  Registry                Service that stores and Docker Hub or a private
                          distributes images      registry

  Repository              A named collection of   `username/python-demo`
                          image versions/tags in  
                          a registry              

  Tag                     Human-readable image    `1.0`, `latest`
                          label, often used for a 
                          version                 

  Image digest            Content-addressed       `sha256:...`
                          identifier for a        
                          specific image manifest 

  Build context           Files made available to Current directory
                          the image build,        
                          usually selected by the 
                          final `.`               

  Port publishing         Mapping a host port to  `-p 8080:8000`
                          a container port        
  -------------------------------------------------------------------------

### Image tag versus digest

A tag such as `python-demo:1.0` is convenient, but a tag can be moved to
point to a different image. A digest identifies a specific
content-addressed manifest. In controlled production pipelines, record
or deploy a digest when exact artifact identity matters.

### Docker Hub versus Docker Engine

Docker Engine runs and manages local containers. Docker Hub is a
registry service where images can be stored and shared. A Docker Hub
account is not required to run a local image, but authentication is
needed for operations that require it, such as pushing to a private or
owned repository.

## 4. Docker architecture and request flow

A simplified architecture:

``` text
Terminal / CI job
       |
       v
   Docker CLI
       |
       | Docker API over Unix socket or configured endpoint
       v
   Docker daemon (dockerd)
       |
       +--> builds and stores images
       +--> creates and manages containers
       +--> manages networks and volumes
       +--> pulls from / pushes to registries
       |
       v
 container runtime + host kernel facilities
```

### Example: `docker run hello-world`

1.  The CLI sends a request to the Docker daemon.
2.  The daemon checks whether the requested image is available locally.
3.  If necessary, it pulls the image from a registry.
4.  The daemon creates a container from the image and requested
    configuration.
5.  The container's main process runs and prints the test message.
6.  The process exits; the container remains listed as an exited
    container until it is removed.

### Why the daemon matters

The Docker daemon is a central management component in the conventional
Docker Engine workflow. If the CLI cannot communicate with it, commands
may fail even if the CLI binary is installed.

Do not overgeneralize this into "every running container always dies if
the daemon is unavailable." The impact depends on configuration and
runtime behavior. Docker has a live-restore feature for eligible
standalone Linux containers during certain daemon outages; see the
official documentation in the references.

## 5. Docker image lifecycle

``` text
Source files
    |
    v
Dockerfile + build context
    |
    | docker build -t name:tag .
    v
Local image
    |
    | docker run name:tag
    v
Container instance
    |
    +--> logs / inspect / exec
    +--> stop / start / remove
    |
    v
Optional image sharing
    |
    | docker tag + docker push
    v
Registry (e.g. Docker Hub)
    |
    | docker pull
    v
Another compatible host
```

Remember:

-   `docker build` creates an image.
-   `docker run` creates and starts a container from an image.
-   `docker ps` lists running containers.
-   `docker ps -a` also shows stopped/exited containers.
-   `docker push` uploads an image tag to a registry; it does not upload
    the running container's writable filesystem as a general backup.

## 6. Lab prerequisites: Ubuntu on AWS EC2

This lab follows the video's Ubuntu-on-EC2 approach. You can also use a
supported Ubuntu VM or local Linux machine.

### Recommended lab setup

-   A supported Ubuntu LTS EC2 image.
-   An EC2 instance size with enough memory and disk for Docker plus the
    test app.
-   SSH access to the instance.
-   An IAM and network setup appropriate for your lab.
-   A Docker Hub account if you want to publish the image.

### Network access

For SSH, allow inbound TCP port `22` from **your own public IP** where
possible. Do not expose SSH to the entire internet (`0.0.0.0/0`) unless
there is a temporary, controlled reason and you understand the risk.

The sample Python app below prints a message and exits; it does not need
an inbound application port. If you later run a web server, allow only
the required port and intended source ranges in the EC2 security group
and host firewall.

**Cost reminder:** EC2 instances, attached storage, and public IPv4
usage may incur charges. Stop or terminate lab resources when finished,
as appropriate for your learning goals. Terminating an instance can
destroy data on its root volume depending on configuration.

## 7. Install Docker Engine on Ubuntu

Use the official Docker APT repository for a repeatable package-based
installation. Commands below follow Docker's current Ubuntu installation
guidance; check the official page if Ubuntu releases or package names
change.

### Step 1 --- Connect to the instance

From a machine with the correct private key:

``` bash
ssh -i /path/to/key.pem ubuntu@EC2_PUBLIC_IP
```

Replace `/path/to/key.pem` and `EC2_PUBLIC_IP` with your actual values.
On Ubuntu EC2 images, the default SSH user is commonly `ubuntu`.

### Step 2 --- Update packages and install prerequisites

``` bash
sudo apt update
sudo apt install -y ca-certificates curl
```

### Step 3 --- Add Docker's official signing key

``` bash
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
```

### Step 4 --- Add the Docker APT repository

``` bash
sudo tee /etc/apt/sources.list.d/docker.sources > /dev/null <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF
```

Refresh package metadata:

``` bash
sudo apt update
```

### Step 5 --- Install Docker Engine and plugins

``` bash
sudo apt install -y docker-ce docker-ce-cli containerd.io \
  docker-buildx-plugin docker-compose-plugin
```

This installs the Engine, CLI, containerd dependency, Buildx, and the
Compose plugin. Exact package availability depends on supported Ubuntu
releases and architecture.

### Step 6 --- Verify the service

``` bash
sudo systemctl status docker --no-pager
sudo docker version
sudo docker info
```

If the service is not running:

``` bash
sudo systemctl start docker
sudo systemctl enable docker
```

On Ubuntu, the package installation commonly starts Docker
automatically; the explicit commands above help verify and enable
startup.

### Step 7 --- Run the test container

``` bash
sudo docker run --rm hello-world
```

Expected behavior: Docker downloads the test image if needed, prints a
success message, and exits. The `--rm` flag removes the test container
after it exits.

**Why use `sudo` first?** By default, the Docker daemon's Unix socket is
controlled by root. A regular user may not have permission to access it
until permissions are configured.

## 8. Start, verify, and inspect Docker

Useful commands:

``` bash
# Client and server versions
docker version

# Detailed engine information
sudo docker info

# Service status
sudo systemctl status docker --no-pager

# Start, stop, restart, and enable at boot
sudo systemctl start docker
sudo systemctl stop docker
sudo systemctl restart docker
sudo systemctl enable docker

# Recent daemon logs
sudo journalctl -u docker --since "15 minutes ago" --no-pager
```

`docker version` shows client and server sections when both are
reachable. If only the client section appears with a daemon connection
error, investigate service status, Docker context, socket permissions,
or endpoint configuration.

## 9. Run your first container

### Run a simple test image

``` bash
docker run --rm hello-world
```

If you have not configured non-root access yet, use:

``` bash
sudo docker run --rm hello-world
```

### Run a shell in a temporary container

``` bash
docker run --rm -it alpine:3.21 sh
```

Inside the container, try:

``` sh
cat /etc/os-release
whoami
exit
```

This starts a shell as the container's main process. When you exit, the
container is removed because `--rm` was specified.

### Understand container states

``` bash
docker ps
docker ps -a
```

A container can be running, exited, created, restarting, or in other
states. A container whose main process has finished is not necessarily a
failed container. For one-shot commands, exiting is expected.

## 10. Create a Python application

Create a project directory:

``` bash
mkdir -p ~/python-docker-demo
cd ~/python-docker-demo
```

Create `app.py`:

``` bash
cat <<'EOF' > app.py
import os
import platform
import socket

def main():
    print("Hello from a Python application running in Docker!")
    print(f"Python: {platform.python_version()}")
    print(f"Hostname: {socket.gethostname()}")
    print(f"APP_ENV: {os.getenv('APP_ENV', 'not-set')}")

if __name__ == "__main__":
    main()
EOF
```

Run it directly on Ubuntu (optional, if Python is installed):

``` bash
python3 app.py
```

The hostname inside a container will normally differ from the host's
hostname. Environment variables can be supplied when a container starts.

## 11. Write a Dockerfile

Create `Dockerfile`:

``` bash
cat <<'EOF' > Dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY app.py .

ENV PYTHONDONTWRITEBYTECODE=1

CMD ["python", "app.py"]
EOF
```

### Explain each instruction

  -----------------------------------------------------------------------
  Instruction                         Purpose
  ----------------------------------- -----------------------------------
  `FROM python:3.12-slim`             Selects a Python base image. The
                                      `slim` variant is a smaller
                                      distribution-based image, not a
                                      guarantee of minimum size or
                                      maximum security.

  `WORKDIR /app`                      Sets the working directory for
                                      subsequent instructions and the
                                      default command.

  `COPY app.py .`                     Copies the application file from
                                      the build context into the image.

  `ENV PYTHONDONTWRITEBYTECODE=1`     Sets an environment variable to
                                      avoid writing `.pyc` bytecode files
                                      in normal Python execution.

  `CMD ["python", "app.py"]`          Defines the default command
                                      executed when the container starts.
  -----------------------------------------------------------------------

### `CMD` versus `RUN`

-   `RUN` executes a command during image building and its filesystem
    changes become part of the image.
-   `CMD` defines the default command or arguments for a container at
    runtime.
-   `ENTRYPOINT` defines the executable used to start the container; it
    is useful when building an image around a fixed command-line tool.

For this small example, there is no need to install third-party
packages. If the application later needs dependencies, define them in a
requirements file and install them in a deliberate build step.

### Build context and `.dockerignore`

The final `.` in `docker build -t python-demo:1.0 .` means the current
directory is the build context. Only files in the context can normally
be copied by `COPY` or `ADD`.

For a larger project, create `.dockerignore` so secrets, Git history,
virtual environments, caches, and irrelevant files are not sent as part
of the build context. Never put credentials in an image or its build
context.

Example `.dockerignore`:

``` bash
cat <<'EOF' > .dockerignore
.git
.venv
__pycache__
*.pyc
.env
EOF
```

## 12. Build, tag, and run the image

### Step 1 --- Build

From the directory containing `Dockerfile` and `app.py`:

``` bash
docker build -t python-demo:1.0 .
```

If non-root Docker access is not configured, prefix the command with
`sudo`.

What the flags mean:

-   `build`: build an image from a build definition and context.
-   `-t python-demo:1.0`: name the image `python-demo` and give it the
    tag `1.0`.
-   `.`: use the current directory as build context.

### Step 2 --- Verify the image

``` bash
docker image ls
docker image inspect python-demo:1.0
```

### Step 3 --- Run a container

``` bash
docker run --name python-demo-container python-demo:1.0
```

Expected output will resemble:

``` text
Hello from a Python application running in Docker!
Python: 3.12.x
Hostname: <container-id-or-hostname>
APP_ENV: not-set
```

The Python version and hostname depend on the actual image and runtime.

### Step 4 --- Inspect the container after it exits

``` bash
docker ps
docker ps -a
docker logs python-demo-container
docker inspect python-demo-container
```

Because the app prints its output and exits, it will usually appear
under `docker ps -a`, not `docker ps`.

### Step 5 --- Pass an environment variable

``` bash
docker run --rm -e APP_ENV=development python-demo:1.0
```

This demonstrates runtime configuration without rebuilding the image.

### Step 6 --- Cleanup

``` bash
docker rm python-demo-container
docker image rm python-demo:1.0
```

If you need to keep the image for the registry exercise, do not remove
it yet. `docker rm` removes a container; `docker image rm` removes a
local image reference when it is no longer in use.

## 13. Docker Hub: publish and pull an image

This section publishes the image built in the previous section.
**Replace `YOUR_DOCKERHUB_USERNAME` with your actual Docker Hub
namespace.** Never type your password or access token directly into a
shell command.

### Step 1 --- Create a repository

1.  Sign in to Docker Hub.
2.  Create a repository, for example `python-demo`.
3.  Choose whether it should be public or private. Public repositories
    allow others to pull the image without being granted
    private-repository access.

### Step 2 --- Authenticate

``` bash
docker login
```

Follow the prompts and use the authentication method supported by Docker
Hub. Prefer a personal access token where applicable, with only the
permissions needed. Do not commit credentials or Docker's credential
configuration to Git.

### Step 3 --- Tag the image for your namespace

``` bash
docker tag python-demo:1.0 YOUR_DOCKERHUB_USERNAME/python-demo:1.0
```

The fully qualified name contains the registry namespace, repository,
and tag. Docker Hub is implied when no other registry hostname is
supplied.

### Step 4 --- Push the image

``` bash
docker push YOUR_DOCKERHUB_USERNAME/python-demo:1.0
```

Docker uploads the layers required by that image tag. The first upload
may take longer than later pushes because layers can be reused when they
already exist in the registry.

### Step 5 --- Verify it on Docker Hub

Open the repository in Docker Hub and check that the `1.0` tag exists. A
successful CLI message is useful, but checking the registry confirms the
image is visible where expected.

### Step 6 --- Pull and run it

On another compatible machine with Docker installed:

``` bash
docker pull YOUR_DOCKERHUB_USERNAME/python-demo:1.0
docker run --rm YOUR_DOCKERHUB_USERNAME/python-demo:1.0
```

If the repository is private, the pulling user must have permission and
authenticate.

### Image sharing workflow

``` text
Local source + Dockerfile
         |
      docker build
         |
         v
   python-demo:1.0
         |
      docker tag
         |
         v
username/python-demo:1.0
         |
      docker push
         |
         v
      Docker Hub
         |
      docker pull
         |
         v
Another compatible host
```

### Registry safety

-   Do not publish secrets, `.env` files, private keys, or customer data
    in an image.
-   Choose public versus private visibility intentionally.
-   Use meaningful version tags rather than relying only on `latest`.
-   For production, track the image digest as well as the human-readable
    tag.
-   Scan images and keep base images updated.
-   Log out on shared machines when appropriate: `docker logout`.

## 14. Docker CLI command reference

  -------------------------------------------------------------------------
  Goal                                Command
  ----------------------------------- -------------------------------------
  Show client/server versions         `docker version`

  Show engine details                 `docker info`

  Download an image                   `docker pull IMAGE:TAG`

  List local images                   `docker image ls`

  Build an image                      `docker build -t NAME:TAG .`

  Start a container                   `docker run --name NAME IMAGE:TAG`

  Run and remove after exit           `docker run --rm IMAGE:TAG`

  List running containers             `docker ps`

  List all containers                 `docker ps -a`

  View logs                           `docker logs CONTAINER`

  Follow logs                         `docker logs -f CONTAINER`

  Inspect metadata                    `docker inspect CONTAINER_OR_IMAGE`

  Execute a command in a running      `docker exec -it CONTAINER sh`
  container                           

  Stop a container                    `docker stop CONTAINER`

  Start a stopped container           `docker start CONTAINER`

  Remove a stopped container          `docker rm CONTAINER`

  Tag an image                        `docker tag SOURCE TARGET`

  Push an image                       `docker push NAME:TAG`

  Remove a local image                `docker image rm IMAGE:TAG`

  Authenticate to a registry          `docker login`

  Sign out from a registry            `docker logout`
  -------------------------------------------------------------------------

The commands above are a quick reference. More advanced cleanup,
storage, networking, and orchestration commands should be documented in
their dedicated topic files.

## 15. Common errors and troubleshooting

### Error: permission denied connecting to Docker socket

Typical message:

``` text
permission denied while trying to connect to the Docker daemon socket
```

**Why it happens:** the current user cannot access the daemon socket.
Docker commonly requires root or membership in the `docker` group.

First test with `sudo`:

``` bash
sudo docker ps
```

If that works and you intentionally want persistent non-root CLI access,
review the next section. Do not use broad socket permissions such as
`chmod 666 /var/run/docker.sock`.

### Configure the `docker` group (convenience, but powerful)

``` bash
sudo groupadd docker
sudo usermod -aG docker "$USER"
newgrp docker
docker run --rm hello-world
```

If `groupadd` says the group already exists, that is normally fine.
Alternatively, log out and reconnect via SSH so group membership
refreshes.

**Security warning:** membership in the `docker` group grants root-level
privileges on a conventional rootful Docker Engine host. Only add
trusted users. For stronger privilege separation, consider Docker
rootless mode or an isolated lab VM. See the official post-installation
documentation.

If a prior `sudo docker` invocation created root-owned files under your
home directory, Docker CLI configuration can also produce a permission
warning. Inspect ownership before changing it:

``` bash
ls -ld "$HOME/.docker"
ls -l "$HOME/.docker"
```

If the directory is yours to manage and contains no intentionally
root-owned data, repair its ownership carefully:

``` bash
sudo chown -R "$USER":"$USER" "$HOME/.docker"
```

Do not delete the directory blindly if it contains useful Docker
configuration.

### Error: Cannot connect to the Docker daemon

Check:

``` bash
sudo systemctl status docker --no-pager
sudo systemctl start docker
sudo journalctl -u docker -n 100 --no-pager
docker context ls
docker context show
```

Confirm that the selected Docker context and endpoint are the ones you
intended to use. If Docker Desktop is involved, verify that it is
running.

### Error: `docker build` cannot find Dockerfile

Check the current directory and filenames:

``` bash
pwd
ls -la
```

The default filename is exactly `Dockerfile` with a capital `D` and no
file extension. If it has another name, specify it with `-f`.

### Error: `COPY` failed or source file not found

Check that the file exists within the build context and that the path is
correct. A `.dockerignore` rule can exclude files from the context.

``` bash
find . -maxdepth 2 -type f -print
cat .dockerignore
```

### Error: container exits immediately

This may be expected if the main process completes. Inspect it:

``` bash
docker ps -a
docker logs CONTAINER_NAME
docker inspect CONTAINER_NAME
```

A container is not a virtual machine that stays running just because it
was started. Its lifecycle is tied to the configured main process.

### Error: Docker Hub push denied

Check the image name, namespace, repository existence, tag, account
permissions, and authentication:

``` bash
docker image ls
docker login
docker push YOUR_DOCKERHUB_USERNAME/python-demo:1.0
```

Make sure you tagged the image with the correct namespace. Do not
include credentials in the command or repository files.

### Error: SSH timeout to EC2

Check the EC2 instance state, public address, route table, network ACLs,
security group inbound rule for TCP/22, local network restrictions, and
private-key path/permissions. Docker installation does not fix an SSH
networking issue.

## 16. Security and operational best practices

### Host and access

-   Use a supported Ubuntu release and install from Docker's official
    repository.
-   Apply OS security updates and keep Docker components maintained.
-   Restrict SSH ingress to trusted source addresses.
-   Limit membership in the `docker` group because it grants powerful
    host access.
-   Avoid exposing the Docker API over an unauthenticated network
    endpoint.

### Application image

-   Keep the build context small and exclude secrets using
    `.dockerignore`.
-   Prefer maintained base images and update them deliberately.
-   Pin dependencies and record versions for reproducible builds.
-   Do not embed credentials in `Dockerfile`, source code, build
    arguments, or image layers.
-   Run the application as a non-root user where practical; the tiny
    teaching example is not a complete production hardening recipe.
-   Scan images and dependencies before deployment.

### Runtime

-   Publish only necessary ports.
-   Avoid privileged containers unless a specific requirement justifies
    the risk.
-   Configure logs and monitoring.
-   Keep durable application data in volumes or external services, not
    only in a disposable container layer.
-   Design for restarts and graceful shutdown.

### Registry

-   Use private repositories for artifacts that should not be public.
-   Use scoped credentials or access tokens where supported.
-   Rotate credentials and avoid sharing accounts.
-   Promote tested images through environments instead of rebuilding a
    different image for each environment.
-   Prefer digest-based identity in tightly controlled production
    releases.

## 17. Hands-on assignment

Complete these tasks and save the commands and observed outputs in your
lab journal.

### Task 1 --- Installation validation

-   [ ] Install Docker Engine on Ubuntu.
-   [ ] Verify `docker version`, `docker info`, and service status.
-   [ ] Run `hello-world`.
-   [ ] Explain why the first command may require `sudo`.

### Task 2 --- Build an application image

-   [ ] Create `app.py` and a `Dockerfile`.
-   [ ] Build `python-demo:1.0`.
-   [ ] Run it and capture the output.
-   [ ] Use `docker ps -a`, `docker logs`, and `docker inspect`.
-   [ ] Explain why the container exits after printing its message.

### Task 3 --- Registry workflow

-   [ ] Create a Docker Hub repository.
-   [ ] Tag the image with your namespace.
-   [ ] Push it.
-   [ ] Verify the tag in Docker Hub.
-   [ ] Pull and run it from a second machine if available.

### Task 4 --- Troubleshooting practice

Explain how you would diagnose each case:

1.  Docker CLI is installed but the daemon is unavailable.
2.  `docker ps` returns a socket permission error.
3.  A build fails because `app.py` cannot be found.
4.  The container exits after one second.
5.  Docker Hub rejects a push.
6.  An EC2 instance is running but SSH times out.

### Task 5 --- Reflection

Write short answers:

-   Why does the image make deployment more repeatable?
-   What is the difference between `docker build` and `docker run`?
-   Why is Docker Hub not the same thing as Docker Engine?
-   What security risk is associated with unrestricted access to the
    Docker socket?
-   Why should secrets not be copied into an image?

## 18. Interview questions and answers

**1. What is Docker?**\
Docker is a platform and toolset used to build, distribute, and run
containerized applications.

**2. What is the Docker daemon?**\
`dockerd` is the background service that receives API requests and
manages Docker resources such as images, containers, networks, and
volumes.

**3. What is the Docker client?**\
The Docker CLI is the command-line client that sends requests to a
Docker daemon or configured endpoint.

**4. What is the difference between an image and a container?**\
An image is the reusable build artifact. A container is an instance
created from an image and runtime configuration.

**5. What does a Dockerfile do?**\
It declares instructions used to build an image, such as choosing a base
image, copying files, setting a working directory, and defining a
default command.

**6. What is a Docker registry?**\
A registry stores and distributes container images. Docker Hub is one
example; organizations can use other hosted or self-managed registries.

**7. What is the purpose of `docker build -t app:1.0 .`?**\
It builds an image from the current build context and tags it `app:1.0`.

**8. What does `docker run` do?**\
It creates and starts a container from an image, using the requested
runtime configuration.

**9. Why does `docker ps` not show a container that has exited?**\
By default, `docker ps` lists running containers. Use `docker ps -a` to
include stopped or exited containers.

**10. Why can `docker` commands fail without `sudo` on Linux?**\
The user may not have permission to access the Docker daemon's Unix
socket. The default rootful daemon is controlled by root.

**11. Is adding a user to the `docker` group harmless?**\
No. On a conventional rootful setup, it effectively grants root-level
privileges on the host. Restrict membership to trusted users.

**12. What is a Docker Hub repository?**\
A named location in Docker Hub for storing image tags under an account
or organization namespace.

**13. Why must an image be tagged before pushing?**\
The tag identifies the target registry namespace, repository, and
version to which the image should be uploaded.

**14. What is the difference between `docker tag` and `docker push`?**\
`docker tag` creates another local name/reference for an image;
`docker push` uploads the tagged image to a registry.

**15. What is a build context?**\
The set of files made available to the image build. The `.` at the end
of a build command selects the current directory.

**16. Why use `.dockerignore`?**\
It excludes irrelevant or sensitive files from the build context,
reducing unnecessary transfer and lowering the chance of accidentally
including secrets.

**17. Does a container always keep running after `docker run`?**\
No. It normally runs while its main process is running. A one-shot
program can complete and leave an exited container record.

**18. Should the `latest` tag be used as a guaranteed version?**\
No. It is a mutable tag convention, not a guarantee that it points to
the newest or intended artifact. Use explicit version tags and record
digests when needed.

**19. Does Docker Hub run the application?**\
No. The registry stores and distributes images. A Docker Engine or
compatible runtime on a host runs the container.

**20. What should you check if a Docker Hub push is denied?**\
Verify login state, repository namespace and name, tag, repository
permissions, and whether the account is authorized to push.

## 19. What belongs in later notes

To keep the GitHub playlist notes clear and non-repetitive, use separate
topic files:

  ---------------------------------------------------------------------------
  Future note                             Put these topics there
  --------------------------------------- -----------------------------------
  `03-dockerfiles-and-builds/README.md`   `RUN`, `COPY`, `ADD`, `CMD`,
                                          `ENTRYPOINT`, cache,
                                          `.dockerignore`, multi-stage
                                          builds, image optimization,
                                          BuildKit

  `04-docker-storage/README.md`           Writable layer, volumes, bind
                                          mounts, persistence, backup and
                                          restore

  `05-docker-networking/README.md`        Bridge, host and overlay networks,
                                          port publishing, DNS, network
                                          isolation

  `06-docker-compose/README.md`           `compose.yaml`, service
                                          definitions, dependencies,
                                          environment configuration,
                                          multi-container lifecycle

  `07-container-security/README.md`       Non-root users, capabilities,
                                          secret handling, image scanning,
                                          supply chain, runtime hardening

  `08-docker-troubleshooting/README.md`   Deeper daemon, networking, DNS,
                                          storage, performance, and
                                          container-debugging scenarios
  ---------------------------------------------------------------------------

The next video in this playlist focuses on Django containerization,
followed by multi-stage builds and persistent storage. Link to those
notes when they are created rather than copying their full tutorials
into this document.

## 20. References

### Video and playlist

-   [Abhishek Veeramalla --- Day-24: Docker Zero to Hero
    Part-1](https://www.youtube.com/watch?v=wodLpta-hoQ)
-   [DevOps Zero to Hero
    playlist](https://www.youtube.com/playlist?list=PLdpzxOOAlwvIc1TjTwopNSjRJkzES2ZXk)
-   [Previous note: Introduction to
    Containerization](../01-containerization-introduction/README.md)

### Official documentation

-   [Install Docker Engine on
    Ubuntu](https://docs.docker.com/engine/install/ubuntu/)
-   [Linux post-installation steps for Docker
    Engine](https://docs.docker.com/engine/install/linux-postinstall/)
-   [Docker
    overview](https://docs.docker.com/get-started/docker-overview/)
-   [Docker CLI
    reference](https://docs.docker.com/reference/cli/docker/)
-   [Docker Hub: push images to a
    repository](https://docs.docker.com/docker-hub/repos/manage/hub-images/push/)
-   [Docker image push
    command](https://docs.docker.com/reference/cli/docker/image/push/)
-   [Docker Python guide](https://docs.docker.com/guides/python/)
-   [Docker build best
    practices](https://docs.docker.com/build/building/best-practices/)
-   [Docker live
    restore](https://docs.docker.com/engine/daemon/live-restore/)

------------------------------------------------------------------------

## Attribution and update note

These are original study notes based on the subject of the linked video
and supplementary official documentation, not a verbatim transcript.
Installation instructions and package availability can change; use the
official Docker documentation for the latest supported Ubuntu releases
and security guidance.

**Suggested commit message:**
`docs: add Docker fundamentals and first image lab`
