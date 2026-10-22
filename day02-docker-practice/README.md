# Docker Fundamentals & DevOps Lab — Day 02

Hands-on Docker labs for the **PGCP-ITISS DevOps course**, based on the supplied Day 02 lab guides and Session 1 / Session 2 notes.

The labs use **Windows 10/11, Docker Desktop with the WSL 2 backend, and Git Bash**. PowerShell can also be used, but shell path syntax may differ.

## Table of Contents

- [Learning Objectives](#learning-objectives)
- [Prerequisites](#prerequisites)
- [Docker Architecture and Core Concepts](#docker-architecture-and-core-concepts)
- [1. Install and Verify Docker Desktop](#1-install-and-verify-docker-desktop)
- [2. Container Lifecycle and CLI](#2-container-lifecycle-and-cli)
- [3. Apache Container and Live File Updates](#3-apache-container-and-live-file-updates)
- [4. Application A — Static Nginx Website](#4-application-a--static-nginx-website)
- [5. Application B — Flask REST API](#5-application-b--flask-rest-api)
- [6. Docker Hub: Tag, Push, and Pull](#6-docker-hub-tag-push-and-pull)
- [7. Docker Storage](#7-docker-storage)
- [8. Docker Networking](#8-docker-networking)
- [9. Multi-Stage Builds](#9-multi-stage-builds)
- [10. Interactive Containers and Non-Root Execution](#10-interactive-containers-and-non-root-execution)
- [11. Troubleshooting on Windows](#11-troubleshooting-on-windows)
- [12. Cleanup](#12-cleanup)
- [Self-Assessment Checklist](#self-assessment-checklist)

## Learning Objectives

By completing these labs, you will practise:

- Explaining containerization and comparing containers with virtual machines.
- Understanding Docker Client, Docker Daemon, images, containers, registries, image layers, namespaces, and cgroups.
- Installing and validating Docker Desktop with WSL 2.
- Managing container lifecycle, logs, processes, ports, and files with the Docker CLI.
- Building custom images for a static Nginx website and a Flask REST API.
- Publishing tagged images to Docker Hub.
- Comparing named volumes, bind mounts, and `tmpfs`.
- Using Docker networks and container-name DNS on user-defined bridge networks.
- Applying multi-stage builds and non-root execution practices.

## Prerequisites

- Windows 10/11 64-bit.
- Hardware virtualization enabled in BIOS/UEFI.
- WSL 2 installed and updated.
- Docker Desktop installed and running with the Linux container engine.
- Git Bash or PowerShell.
- A Docker Hub account for the publishing exercise.
- Python is optional for local Flask testing; the Flask container can install its dependencies during image build.

## Docker Architecture and Core Concepts

Docker follows a client-server architecture:

- **Docker CLI / client:** accepts commands such as `docker run` and `docker build`.
- **Docker daemon (`dockerd`):** manages images, containers, networks, and volumes.
- **Docker registry:** stores and distributes images, for example Docker Hub.
- **Images:** read-only templates made from layers.
- **Containers:** running instances of images, with a thin writable layer.
- **Namespaces:** isolate process IDs, networking, mount points, IPC, hostnames, and user mappings.
- **cgroups:** limit and account for resources such as CPU and memory.

Containers use OS-level virtualization and share the host kernel provided by the container runtime environment. A traditional VM includes its own guest OS kernel and runs through a hypervisor.

### Common Dockerfile instructions

| Instruction | Purpose |
|---|---|
| `FROM` | Selects the base image. |
| `LABEL` | Adds image metadata. |
| `WORKDIR` | Sets the working directory inside the image. |
| `COPY` | Copies files from the build context into the image. |
| `RUN` | Executes commands while building the image. |
| `EXPOSE` | Documents the container port the application uses. It does not publish the port by itself. |
| `CMD` | Supplies the default command or arguments when a container starts. |
| `ENTRYPOINT` | Defines the executable that the container runs. |

Docker image layers are read-only. A container adds a writable layer; changes to that layer do not modify the original image.

## 1. Install and Verify Docker Desktop

1. Open Task Manager with `Ctrl + Shift + Esc`, select **Performance → CPU**, and verify that **Virtualization** is enabled.
2. In an elevated PowerShell window, install or update WSL 2 if needed:

   ```powershell
   wsl --install
   wsl --update
   wsl --status
   ```

3. Install Docker Desktop from [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/).
4. During setup, use the WSL 2 backend when available.
5. Start Docker Desktop and wait for the engine to become ready.
6. Verify the CLI from Git Bash:

   ```bash
   docker --version
   docker info
   docker context ls
   ```

`docker info` should display both client and server information. If the server information is missing, Docker Desktop's engine may not be running or the active context may be incorrect.

## 2. Container Lifecycle and CLI

### First container

```bash
docker run hello-world
```

Docker downloads the image if necessary, runs the test container, prints its confirmation, and exits.

### Run Nginx in detached mode

```bash
docker run -d -p 8080:80 --name my-first-web nginx:alpine
```

- `-d`: runs in the background.
- `-p 8080:80`: maps **host port 8080** to **container port 80**.
- `--name`: assigns a memorable container name.
- `nginx:alpine`: selects the lightweight Nginx Alpine image.

Open [http://localhost:8080](http://localhost:8080).

### Useful lifecycle commands

```bash
docker ps                         # Running containers
docker ps -a                      # All containers, including stopped ones
docker stop my-first-web          # Stop a running container
docker start my-first-web         # Start an existing stopped container
docker restart my-first-web       # Restart a container
docker logs my-first-web          # View logs
docker logs -f my-first-web       # Follow logs until Ctrl+C
docker inspect my-first-web       # Detailed container metadata
docker stats                      # Live resource usage
docker images                     # Local images
docker pull nginx:alpine          # Download an image
docker exec -it my-first-web //bin/sh  # Interactive shell from Git Bash
```

**Git Bash note:** Git Bash may convert `/bin/sh` into a Windows path. Use `//bin/sh` or run `MSYS_NO_PATHCONV=1 docker exec -it my-first-web /bin/sh`.

## 3. Apache Container and Live File Updates

This exercise uses Apache HTTP Server (`httpd`) and the document root `/usr/local/apache2/htdocs`.

### Start Apache

```bash
docker run -d -p 8000:80 --name web5 httpd:alpine
```

Create `index.html` in Git Bash:

```bash
cat <<'EOF' > index.html
<!DOCTYPE html>
<html>
<head><title>Web5 Apache Server</title></head>
<body style="font-family: Arial; text-align: center; margin-top: 50px;">
    <h1>Welcome to Web5 Container</h1>
    <p>Version: 1.0 (Initial Copy)</p>
</body>
</html>
EOF
```

Copy the file into the running container:

```bash
docker cp index.html web5:/usr/local/apache2/htdocs/index.html
```

Open [http://localhost:8000](http://localhost:8000).

### Update the page without rebuilding the image

Replace the local file with a new version:

```bash
cat <<'EOF' > index.html
<!DOCTYPE html>
<html>
<head><title>Web5 Apache Server</title></head>
<body style="font-family: Arial; text-align: center; margin-top: 50px; background-color: #e0f7fa;">
    <h1 style="color: #00796b;">Welcome to Web5 Container</h1>
    <p>Version: 2.0 (LIVE HOT UPDATE via docker cp)</p>
    <p>Timestamp: Updated Successfully!</p>
</body>
</html>
EOF

docker cp index.html web5:/usr/local/apache2/htdocs/index.html
```

Refresh the browser. The running container serves the copied file; no image rebuild is required.

## 4. Application A — Static Nginx Website

Suggested project layout:

```text
static-website/
├── Dockerfile
├── index.html
└── style.css
```

Create a project directory:

```bash
mkdir -p ~/devops-labs/day02-docker/static-website
cd ~/devops-labs/day02-docker/static-website
```

### `index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Cloud Native DevOps Portal</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>Cloud Native DevOps Portal</h1>
        <p class="subtitle">Custom Containerized Web Service</p>
        <div class="card">
            <h3>Container Details</h3>
            <p><strong>Base Server:</strong> Nginx Alpine</p>
            <p><strong>Runtime:</strong> Docker Engine on Windows</p>
            <p><strong>Port:</strong> 80</p>
        </div>
    </div>
</body>
</html>
```

### `style.css`

```css
body {
    font-family: 'Segoe UI', Tahoma, sans-serif;
    background: #0f172a;
    color: #f8fafc;
    margin: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}

.container {
    text-align: center;
}

h1 {
    color: #38bdf8;
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}

.subtitle {
    color: #94a3b8;
    font-size: 1.1rem;
    margin-bottom: 2rem;
}

.card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 2rem;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
    display: inline-block;
    text-align: left;
}
```

### `Dockerfile`

```dockerfile
FROM nginx:alpine
LABEL maintainer="student@cdac.in"
LABEL application="static-website"

RUN rm -rf /usr/share/nginx/html/*

COPY index.html /usr/share/nginx/html/index.html
COPY style.css /usr/share/nginx/html/style.css

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Build, run, and test

Run these commands from the `static-website` directory:

```bash
docker build -t static-website:v1 .
docker run -d -p 8080:80 --name my-custom-web static-website:v1
docker ps
docker logs my-custom-web
```

Open [http://localhost:8080](http://localhost:8080).

To stop and remove the container:

```bash
docker stop my-custom-web
docker rm my-custom-web
```

## 5. Application B — Flask REST API

Keep the Flask API in its **own directory** so its Dockerfile does not overwrite the static website's Dockerfile.

Suggested layout:

```text
flask-api/
├── Dockerfile
├── app.py
└── requirements.txt
```

### `requirements.txt`

```text
Flask==3.0.0
```

### `app.py`

```python
from flask import Flask, jsonify
import socket
import datetime

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "message": "Welcome to the DevOps Flask REST API Microservice",
        "container_hostname": socket.gethostname(),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    })


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "UP",
        "service": "flask-api",
        "code": 200
    }), 200


@app.route("/api/info", methods=["GET"])
def info():
    return jsonify({
        "module": "DevOps Day-02",
        "version": "1.0.0",
        "author": "CDAC Student",
        "endpoints": ["/", "/api/health", "/api/info"]
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

### `Dockerfile`

```dockerfile
FROM python:3.10-slim
LABEL maintainer="student@cdac.in"
LABEL service="flask-rest-api"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000
CMD ["python", "app.py"]
```

### Build, run, and test

From the `flask-api` directory:

```bash
docker build -t flask-api:v1 .
docker run -d -p 5000:5000 --name my-flask-service flask-api:v1
docker ps
docker logs my-flask-service
```

API endpoints:

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `http://localhost:5000/` | Welcome message, hostname, and timestamp |
| `GET` | `http://localhost:5000/api/health` | Health status |
| `GET` | `http://localhost:5000/api/info` | Module, version, author, and endpoint list |

Test with curl:

```bash
curl http://localhost:5000/
curl http://localhost:5000/api/health
curl http://localhost:5000/api/info
```

The guide's Flask example uses the built-in development server. For production deployment, use a production WSGI server and appropriate application-server configuration.

## 6. Docker Hub: Tag, Push, and Pull

1. Create or sign in to an account at [Docker Hub](https://hub.docker.com/).
2. Create a **Personal Access Token** in Docker Hub account security settings with the required permissions.
3. Log in from Git Bash. Use the token when prompted for a password:

   ```bash
   docker login -u YOUR_DOCKERHUB_USERNAME
   ```

4. Tag the local images with your Docker Hub username:

   ```bash
   docker tag static-website:v1 YOUR_DOCKERHUB_USERNAME/static-website:v1
   docker tag static-website:v1 YOUR_DOCKERHUB_USERNAME/static-website:latest

   docker tag flask-api:v1 YOUR_DOCKERHUB_USERNAME/flask-api:v1
   docker tag flask-api:v1 YOUR_DOCKERHUB_USERNAME/flask-api:latest
   ```

5. Push the images:

   ```bash
   docker push YOUR_DOCKERHUB_USERNAME/static-website:v1
   docker push YOUR_DOCKERHUB_USERNAME/static-website:latest
   docker push YOUR_DOCKERHUB_USERNAME/flask-api:v1
   docker push YOUR_DOCKERHUB_USERNAME/flask-api:latest
   ```

6. Verify the repositories and tags at [hub.docker.com/repositories](https://hub.docker.com/repositories).

7. Test the published static website image by running it on a different host port:

   ```bash
   docker run -d -p 9090:80 --name cloud-web YOUR_DOCKERHUB_USERNAME/static-website:v1
   ```

   Open [http://localhost:9090](http://localhost:9090).

Replace `YOUR_DOCKERHUB_USERNAME` with your actual Docker Hub ID. Do not commit access tokens or passwords to source control.

## 7. Docker Storage

Container writable-layer data is tied to the container. Removing the container removes data stored only in that layer. Use the storage mechanism that matches the purpose.

| Storage type | Managed by / location | Typical use |
|---|---|---|
| Named volume | Managed by Docker | Persistent application data and databases |
| Bind mount | A specific host file or directory | Local development, live code updates, host configuration |
| `tmpfs` mount | Memory (RAM) | Temporary data and sensitive caches that should not be written to container storage |

### Named volume: persist data across container removal

```bash
docker volume create pg-database-volume
docker volume ls
docker volume inspect pg-database-volume

docker run -d --name writer-container \
  -v pg-database-volume:/app/storage \
  alpine sh -c "echo 'TRANSACTION_ID=TX9982,AMOUNT=450.00,STATUS=CONFIRMED' > /app/storage/ledger.csv; sleep 3600"

docker exec -it writer-container cat /app/storage/ledger.csv
docker rm -f writer-container

docker run --rm --name reader-container \
  -v pg-database-volume:/app/storage \
  alpine cat /app/storage/ledger.csv
```

The record should remain available because it is stored in the named volume.

### Bind mount: live development

Run from the directory containing your website files:

```bash
docker run -d -p 8081:80 --name live-web-server \
  -v "$(pwd)":/usr/share/nginx/html \
  nginx:alpine
```

Open [http://localhost:8081](http://localhost:8081). Changes made to the host files should be visible without rebuilding the image.

For read-only access:

```bash
docker rm -f live-web-server

docker run -d -p 8081:80 --name secure-web-server \
  -v "$(pwd)":/usr/share/nginx/html:ro \
  nginx:alpine
```

The `:ro` option makes the mount read-only from inside the container.

### `tmpfs`: temporary in-memory storage

```bash
docker run -d --name memory-container \
  --tmpfs /app/secure-cache:rw,noexec,nosuid,size=32m \
  alpine sleep 3600

docker exec -it memory-container df -h /app/secure-cache
docker rm -f memory-container
```

The mount uses RAM and is temporary. Do not treat `tmpfs` alone as a complete secrets-management solution.

## 8. Docker Networking

Common network drivers covered in the lab:

- **Bridge:** default network driver for containers on one Docker host.
- **Host:** shares the host network namespace where supported.
- **None:** disables external container networking except loopback.
- **Overlay:** connects services across multiple Docker hosts in supported setups.
- **Macvlan:** gives a container a MAC address so it can appear directly on a physical network.

### Default bridge versus user-defined bridge

The default bridge does not provide the same automatic container-name DNS service as a user-defined bridge. A user-defined bridge provides embedded DNS and container-name resolution.

Create and inspect a custom bridge:

```bash
docker network create --driver bridge devops-internal-net
docker network inspect devops-internal-net
```

Run containers on it:

```bash
docker run -d --name backend-redis --network devops-internal-net redis:alpine
docker run -d --name frontend-app --network devops-internal-net alpine sleep 3600
```

Test name resolution from the frontend container (the Alpine image may need a ping utility installed; if `ping` is unavailable, use a suitable diagnostic image or test with a client that has DNS tools):

```bash
docker exec -it frontend-app ping -c 3 backend-redis
```

Remove the lab containers and network when finished:

```bash
docker rm -f frontend-app backend-redis
docker network rm devops-internal-net
```

## 9. Multi-Stage Builds

Multi-stage builds use one stage to compile or build an application and a smaller stage to run the output. This can reduce the final image size and avoid shipping build tools in the runtime image.

Example from the lab: compile a small C application in a GCC stage and copy only the compiled binary into a `scratch` image.

`hello.c`:

```c
#include <stdio.h>

int main(void) {
    printf("DevOps Docker C-Application Executed Successfully!\n");
    return 0;
}
```

`Dockerfile`:

```dockerfile
FROM gcc:latest AS builder
WORKDIR /src
COPY hello.c .
RUN gcc -static -o hello hello.c

FROM scratch
COPY --from=builder /src/hello /hello
CMD ["/hello"]
```

Build and run:

```bash
docker build -t devops-c-app:v1 .
docker run --rm devops-c-app:v1
```

Expected output:

```text
DevOps Docker C-Application Executed Successfully!
```

## 10. Interactive Containers and Non-Root Execution

### Interactive terminal

The `-i` flag keeps standard input open, and `-t` allocates a pseudo-terminal:

```bash
docker run -it --rm ubuntu:22.04 /bin/bash
```

Exit the shell to remove the temporary container.

### Run as a non-root user

For production images, prefer a dedicated unprivileged user where the base image and application support it. This reduces the impact of a compromised application process. Ensure the application has appropriate ownership and permissions for its required files and ports.

## 11. Troubleshooting on Windows

### Docker daemon or engine is unreachable

Symptoms include errors mentioning `dockerDesktopLinuxEngine`, a missing named pipe, or inability to connect to the daemon.

1. Open Docker Desktop and wait for it to finish starting.
2. Check:

   ```bash
   docker context ls
   docker context show
   docker info
   ```

3. If appropriate for your setup, switch to the existing `desktop-linux` context:

   ```bash
   docker context use desktop-linux
   docker info
   ```

4. If the engine remains unreachable, restart Docker Desktop and retry. Do not delete containers or volumes as a first troubleshooting step.

### `kubectl` has no current context

This is a Kubernetes configuration issue rather than a Docker container command issue. For the Docker Desktop Kubernetes cluster, enable/start Kubernetes in Docker Desktop if available, then inspect:

```bash
kubectl config get-contexts
kubectl config current-context
kubectl get nodes
```

Use `kubectl config use-context docker-desktop` only if that context exists.

### `docker-credential-desktop` is not found

If Docker reports that `docker-credential-desktop` cannot be found, inspect Docker's configuration and confirm whether the helper executable exists before changing settings:

```bash
cat ~/.docker/config.json
where.exe docker-credential-desktop
```

Prefer repairing Docker Desktop's installation or PATH when the helper should be installed. Do not expose or commit registry credentials.

### Git Bash changes Linux paths

Git Bash can rewrite paths such as `/bin/sh` as Windows paths. For Docker commands, use:

```bash
docker exec -it my-first-web //bin/sh
```

or:

```bash
MSYS_NO_PATHCONV=1 docker exec -it my-first-web /bin/sh
```

### Host port is already in use

Stop the container or process that owns the port, or map a different host port. For example, use `-p 8085:80` instead of `-p 8080:80`.

### Container exits or a page is unavailable

```bash
docker ps -a
docker logs CONTAINER_NAME
docker inspect CONTAINER_NAME
```

Check that the container is running, the application listens on the expected container port, and the `-p HOST_PORT:CONTAINER_PORT` mapping is correct.

## 12. Cleanup

Inspect resources before removing them:

```bash
docker ps -a
docker images
docker volume ls
docker network ls
```

Stop and remove the lab containers you created (only run names that exist in your environment):

```bash
docker rm -f my-first-web web5 my-custom-web my-flask-service cloud-web
docker rm -f writer-container reader-container live-web-server secure-web-server memory-container
docker rm -f frontend-app backend-redis client-one client-two
```

Remove a lab network after disconnecting its containers:

```bash
docker network rm devops-internal-net
```

Remove a named volume only when you no longer need its data:

```bash
docker volume rm pg-database-volume
```

Use `docker system prune` cautiously: it can remove unused Docker resources. Do not remove volumes or images containing work you need to keep.

## Self-Assessment Checklist

- [ ] Verified virtualization and WSL 2.
- [ ] Installed and started Docker Desktop.
- [ ] Ran `hello-world` and an Nginx container.
- [ ] Practised `ps`, `stop`, `start`, `restart`, `logs`, `exec`, `inspect`, and `cp`.
- [ ] Updated an Apache-served HTML page with `docker cp`.
- [ ] Built and ran the custom Nginx website image.
- [ ] Built and tested the Flask REST API endpoints.
- [ ] Tagged and pushed both images to Docker Hub, then pulled and ran a published image.
- [ ] Demonstrated data loss in a container writable layer and persistence with a named volume.
- [ ] Used a bind mount and a `tmpfs` mount.
- [ ] Compared Docker network drivers and tested name resolution on a user-defined bridge.
- [ ] Built and ran a multi-stage C application.
- [ ] Practised interactive container access and reviewed non-root execution.
- [ ] Cleaned up lab resources without deleting data that must be retained.

## Source Material

This README consolidates the four supplied course PDFs:

- `Lab-Guide.pdf` — Day 02 Windows lab guide: Docker Desktop, CLI lifecycle, Nginx, Flask, and Docker Hub publishing.
- `Lab-Guide-Session-2.pdf` — Advanced Docker labs: volumes, bind mounts, `tmpfs`, networking, multi-stage builds, interactive containers, and non-root execution.
- `Session-1.pdf` — Docker architecture, containerization concepts, image layers, CLI commands, and Dockerfile instructions.
- `Session-2.pdf` — Storage mechanisms, network drivers, application packaging, and image best practices.

Course material credited in the PDFs to **Vinod Kumar Kayartaya** — [vinod.co](https://vinod.co/).
