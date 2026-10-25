# Docker Compose: Multi-Container Applications

> **Topic:** Compose service configuration, networking, volumes,
> environment variables, health checks, and practical workflows\
> **Course context:** DevOps Zero to Hero --- Docker learning notes\
> **Suggested repository path:** `07-docker-compose/README.md`

Docker Compose lets you define and manage an application made of
multiple containers through a declarative YAML file. Instead of
remembering long `docker run` commands for every component, you describe
services, networks, volumes, configuration, and dependencies in a
`compose.yaml` file, then use the Compose CLI to manage the application
as a unit.

These notes focus on multi-container configuration and daily operations.
They build on the Docker fundamentals, storage, and networking notes
already in this repository.

## Table of contents

-   [1. Learning objectives](#1-learning-objectives)
-   [2. What Docker Compose solves](#2-what-docker-compose-solves)
-   [3. Compose terminology](#3-compose-terminology)
-   [4. Install and verify Compose](#4-install-and-verify-compose)
-   [5. Understand a Compose file](#5-understand-a-compose-file)
-   [6. Practical lab: web app plus
    Redis](#6-practical-lab-web-app-plus-redis)
-   [7. Practical lab: API plus
    PostgreSQL](#7-practical-lab-api-plus-postgresql)
-   [8. Environment variables and
    `.env`](#8-environment-variables-and-env)
-   [9. Networks, service discovery, and
    ports](#9-networks-service-discovery-and-ports)
-   [10. Volumes and persistent data](#10-volumes-and-persistent-data)
-   [11. Startup order and health
    checks](#11-startup-order-and-health-checks)
-   [12. Build your own image with
    Compose](#12-build-your-own-image-with-compose)
-   [13. Essential Compose commands](#13-essential-compose-commands)
-   [14. Troubleshooting](#14-troubleshooting)
-   [15. Production and security
    practices](#15-production-and-security-practices)
-   [16. Docker Compose vs. `docker run`
    vs. Kubernetes](#16-docker-compose-vs-docker-run-vs-kubernetes)
-   [17. Interview questions and
    answers](#17-interview-questions-and-answers)
-   [18. Scope boundaries](#18-scope-boundaries)
-   [19. Official references](#19-official-references)

## 1. Learning objectives

After completing this note, you should be able to:

-   Explain why Compose is useful for applications with multiple
    services.
-   Write and validate a `compose.yaml` file.
-   Configure services, networks, volumes, ports, environment variables,
    and health checks.
-   Build a local image from a Dockerfile and run it through Compose.
-   Understand service-name DNS and why `localhost` inside a container
    refers to that container.
-   Start, stop, inspect, and debug an application stack.
-   Avoid common data-loss and secret-management mistakes.

## 2. What Docker Compose solves

Imagine an application that requires:

-   A web/API container.
-   A Redis cache.
-   A PostgreSQL database.
-   A private network for service-to-service communication.
-   Persistent storage for database data.
-   Configuration that changes between local development and deployment.

Without Compose, you might need to run several long `docker run`
commands, remember all options, create networks and volumes manually,
and start components in the right order. Compose stores this desired
configuration in one YAML file.

### Example architecture

``` text
Host browser / API client
          |
    localhost:8000
          |
     [web service]
          |
    Compose network
       /       \
   [redis]  [postgres]
                 |
          named volume
```

Compose makes local development and repeatable testing easier. It does
not, by itself, guarantee high availability, secure secrets, database
backups, or production-grade orchestration.

## 3. Compose terminology

  -----------------------------------------------------------------------
  Term                                Meaning
  ----------------------------------- -----------------------------------
  Project                             A Compose application grouping its
                                      resources. By default, the project
                                      name is often derived from the
                                      directory name.

  Service                             A declaration describing how to run
                                      a type of container, including its
                                      image/build, configuration, and
                                      network attachments.

  Container                           A runtime instance created for a
                                      service. A service can have one or
                                      more instances.

  Image                               The packaged filesystem and
                                      metadata used to create a
                                      container.

  Network                             The connectivity layer Compose
                                      creates or uses for services.

  Volume                              A managed storage resource that can
                                      persist data beyond a container's
                                      lifetime.

  `ports`                             Publishes container ports through
                                      host ports.

  `expose`                            Documents/makes a service port
                                      available to connected services
                                      without publishing it to the host.
                                      It is not a firewall rule.

  `depends_on`                        Describes dependency/startup
                                      ordering; readiness requires
                                      additional care.

  Health check                        A command or test used to determine
                                      whether a container's service is
                                      healthy.

  `.env`                              A commonly used file for variable
                                      substitution in Compose
                                      configuration; not automatically a
                                      secure secret store.
  -----------------------------------------------------------------------

Compose files use YAML indentation. Spaces matter; tabs should not be
used for indentation. Modern Docker Compose is generally invoked as
`docker compose` (space), not the legacy standalone `docker-compose`
command.

## 4. Install and verify Compose

On systems with Docker Desktop, Compose is generally included. On Linux,
install Docker Engine and the Compose plugin using the official
instructions for your distribution.

Verify:

``` bash
docker --version
docker compose version
docker info
```

Check that Docker is running:

``` bash
docker ps
```

If you see a daemon connection error, start or troubleshoot the Docker
service before debugging the Compose file. On a systemd-based Linux
host:

``` bash
sudo systemctl status docker
sudo systemctl start docker
sudo systemctl enable docker
```

Use the official installation documentation for the correct OS-specific
steps. Avoid mixing packages from unrelated Docker installation methods.

## 5. Understand a Compose file

A modern Compose file can begin directly with `services:`; a top-level
`version:` key is obsolete in current Compose specifications and is
usually unnecessary.

Example:

``` yaml
services:
  web:
    image: nginx:alpine
    ports:
      - "127.0.0.1:8080:80"
    networks:
      - frontend

networks:
  frontend:
```

Important details:

-   `services` declares the containers Compose should manage.
-   `image` chooses an existing image.
-   `build` builds an image from a Dockerfile/context.
-   `ports` publishes ports from the host to the container.
-   `networks` controls which Compose networks the service joins.
-   `volumes` mounts persistent storage or host paths.
-   `environment` sets environment variables inside a container.
-   `healthcheck` defines a service health test.
-   `restart` sets a restart policy for containers; it is not a complete
    process-supervision or high-availability solution.

### Validate before starting

From the directory containing `compose.yaml`:

``` bash
docker compose config
docker compose config --services
docker compose config --images
```

`docker compose config` resolves and renders the configuration. Treat
its output as potentially sensitive if it contains interpolated
credentials.

## 6. Practical lab: web app plus Redis

**Goal:** Run a small web application and Redis together, demonstrate
service-name DNS, and inspect the Compose lifecycle.

This lab uses a tiny Python HTTP server that reports whether it can
resolve the Redis service name. It demonstrates Compose networking; it
is not a real cache integration or production web application.

### Step 1: Create the lab directory

``` bash
mkdir compose-redis-lab
cd compose-redis-lab
```

Create `app.py`:

``` python
from http.server import BaseHTTPRequestHandler, HTTPServer
import socket

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            redis_ip = socket.gethostbyname("redis")
            message = f"Compose DNS resolved redis to {redis_ip}\n"
            status = 200
        except OSError as exc:
            message = f"Could not resolve redis: {exc}\n"
            status = 503

        body = message.encode()
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        print("%s - %s" % (self.address_string(), format % args))

HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
```

Create `Dockerfile`:

``` dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY app.py .
USER 10001:10001
EXPOSE 8000

CMD ["python", "app.py"]
```

The application listens on `0.0.0.0` inside the container so it can
accept traffic through the container network. `EXPOSE` documents the
port but does not publish it.

Create `compose.yaml`:

``` yaml
services:
  web:
    build: .
    ports:
      - "127.0.0.1:8000:8000"
    depends_on:
      redis:
        condition: service_healthy
    networks:
      - app-net

  redis:
    image: redis:7-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5
    networks:
      - app-net

networks:
  app-net:
    driver: bridge
```

For a long-lived deployment, select and test a currently supported Redis
version and define an upgrade plan rather than relying indefinitely on a
tutorial tag.

### Step 2: Validate and start

``` bash
docker compose config
docker compose up -d --build
docker compose ps
```

### Step 3: Test the application

Open `http://127.0.0.1:8000` in a browser or run:

``` bash
curl http://127.0.0.1:8000
```

Expected output resembles:

``` text
Compose DNS resolved redis to 172.x.x.x
```

The exact IP will differ. The important result is that the `web` service
can resolve the name `redis` because both services share `app-net`.

This test confirms DNS resolution, **not** a Redis command or a complete
Redis application connection. In a real application, use a Redis client
library and handle connection errors and timeouts.

### Step 4: Inspect the stack

``` bash
docker compose ps
docker compose logs
docker compose logs -f web
docker compose exec web python -c "import socket; print(socket.gethostbyname('redis'))"
docker compose exec redis redis-cli ping
```

The last command should return `PONG` when Redis is ready.

### Step 5: Stop and remove the lab

``` bash
docker compose down
```

This removes the containers and the default project network. No named
volume is used in this lab. If you later add named volumes,
`docker compose down` normally preserves them unless you explicitly
request volume removal.

## 7. Practical lab: API plus PostgreSQL

**Goal:** Configure a database service with persistent storage, a health
check, and credentials supplied through environment variables.

This example is a database configuration exercise, not a complete
application. It deliberately does not publish PostgreSQL's port to the
host.

Create a directory and a `compose.yaml` file:

``` yaml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_DB: appdb
      POSTGRES_USER: appuser
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:?Set POSTGRES_PASSWORD in .env}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U appuser -d appdb"]
      interval: 5s
      timeout: 3s
      retries: 10
    networks:
      - backend

  admin-client:
    image: postgres:16
    entrypoint: ["sh", "-c", "until pg_isready -h db -U appuser -d appdb; do sleep 2; done; psql -h db -U appuser -d appdb -c 'SELECT current_database(), current_user;'"]
    environment:
      PGPASSWORD: ${POSTGRES_PASSWORD:?Set POSTGRES_PASSWORD in .env}
    depends_on:
      db:
        condition: service_healthy
    networks:
      - backend
    restart: "no"

volumes:
  postgres_data:

networks:
  backend:
    driver: bridge
```

Create a local `.env` file in the same directory:

``` dotenv
POSTGRES_PASSWORD=replace-with-a-strong-local-lab-password
```

Do not commit a real `.env` file containing credentials. Add it to
`.gitignore`:

``` gitignore
.env
```

Use a secure secret-management mechanism appropriate to your deployment
for production credentials. A `.env` file is convenient configuration,
not encrypted secret storage.

Start the lab:

``` bash
docker compose config
docker compose up -d db
docker compose ps
docker compose logs db
```

Run a one-off client query:

``` bash
docker compose run --rm admin-client
```

Expected query output includes the database name `appdb` and user
`appuser`. Exact formatting varies.

Connect interactively if needed:

``` bash
docker compose exec db psql -U appuser -d appdb
```

At the `psql` prompt:

``` sql
CREATE TABLE IF NOT EXISTS notes (
    id SERIAL PRIMARY KEY,
    message TEXT NOT NULL
);

INSERT INTO notes (message) VALUES ('Compose database lab');
SELECT * FROM notes;
\q
```

Confirm the volume exists:

``` bash
docker volume ls
docker volume inspect <PROJECT_NAME>_postgres_data
```

Compose usually prefixes named resources with the project name, so the
actual volume name can differ. Use `docker volume ls` to find it rather
than assuming the exact name.

Clean up the containers and network while preserving the database
volume:

``` bash
docker compose down
```

**Warning:** The following command removes named volumes declared by the
Compose project and can delete the database data. Use it only when you
intentionally want to reset the lab:

``` bash
docker compose down --volumes
```

### Database initialization note

The official PostgreSQL image uses initialization variables and scripts
when initializing a new data directory. Changing `POSTGRES_USER`,
`POSTGRES_PASSWORD`, or initialization scripts later does not
automatically recreate or rewrite an already-initialized database.
Database credential changes should be performed using database
administration procedures.

## 8. Environment variables and `.env`

Compose supports variable substitution in the YAML file:

``` yaml
services:
  web:
    image: "${WEB_IMAGE:-nginx:alpine}"
```

This uses `WEB_IMAGE` if supplied, otherwise the default `nginx:alpine`.

A `.env` file is commonly used to provide interpolation values:

``` dotenv
WEB_IMAGE=nginx:alpine
```

There are two concepts to distinguish:

1.  **Compose interpolation:** variables used to render the Compose
    file, such as `${WEB_IMAGE}`.
2.  **Container environment:** variables passed into the running
    container through `environment:` or `env_file:`.

A variable in `.env` is not automatically injected into every container.
Reference it explicitly in the service configuration when needed.

Example:

``` yaml
services:
  app:
    image: example/app:latest
    environment:
      APP_MODE: ${APP_MODE:-development}
```

Useful commands:

``` bash
docker compose config
docker compose config --environment
```

Review command output before sharing it because resolved configuration
may reveal sensitive values.

### Secret handling rules

-   Never commit production passwords, private keys, API tokens, or
    certificates.
-   `.env` files are plain text unless protected by external controls.
-   Prefer a secret manager or platform-specific secrets mechanism for
    production.
-   Avoid printing secrets in logs or shell history.
-   Rotate credentials if they are accidentally committed or exposed.

## 9. Networks, service discovery, and ports

Compose normally creates a project network and attaches services to it.
Services on the same network can generally reach each other by service
name.

For example, an application connecting to PostgreSQL should normally
use:

``` text
Host: db
Port: 5432
```

It should **not** use `localhost:5432` to reach the `db` container.
Inside a container, `localhost` points back to that same container.

### Publish only what needs host access

``` yaml
services:
  web:
    ports:
      - "127.0.0.1:8080:80"
```

This maps host loopback port 8080 to port 80 in the container. Binding
to loopback is useful for local development. If external clients must
reach the service, make the exposure decision deliberately and configure
host/cloud firewall rules.

A database service typically needs no `ports:` section when only other
Compose services should access it.

### Separate frontend and backend networks

For a more controlled topology:

``` yaml
services:
  proxy:
    image: nginx:alpine
    ports:
      - "127.0.0.1:8080:80"
    networks:
      - frontend

  api:
    image: example/api:latest
    networks:
      - frontend
      - backend

  db:
    image: postgres:16
    networks:
      - backend

networks:
  frontend:
  backend:
    internal: true
```

This illustrates network membership: `proxy` can reach `api`, and `api`
can reach `db`, while `proxy` is not attached to the backend network.
`internal: true` restricts external connectivity for that network; it is
not a complete security boundary. Adapt the topology to actual service
requirements, and do not use placeholder image names as though they were
ready-to-run applications.

## 10. Volumes and persistent data

Container writable layers are tied to container instances. When a
container is removed, data stored only in that layer is not a reliable
persistence strategy.

A named volume is appropriate for database data:

``` yaml
services:
  db:
    image: postgres:16
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

A bind mount maps a host path into a container:

``` yaml
services:
  web:
    image: nginx:alpine
    volumes:
      - ./site:/usr/share/nginx/html:ro
```

Use `:ro` when the container only needs to read the files. Bind-mount
paths and file-sharing behavior vary across operating systems and Docker
Desktop configurations.

Remember:

-   A volume helps persist data beyond a container's lifetime.
-   A volume is **not a backup**.
-   A database backup must account for application/database consistency.
-   `docker compose down` normally keeps named volumes.
-   `docker compose down --volumes` removes project-declared named
    volumes and can cause data loss.

Database backup and recovery procedures belong in the
stateful-containers notes; this section covers only how Compose declares
storage.

## 11. Startup order and health checks

### `depends_on` does not always mean "ready"

A basic dependency:

``` yaml
services:
  api:
    depends_on:
      - db
```

This describes startup order, but it does not guarantee that PostgreSQL
is ready to accept connections when the API starts.

Where supported, use a health check and a readiness condition:

``` yaml
services:
  api:
    depends_on:
      db:
        condition: service_healthy
```

The database service must define a meaningful `healthcheck`. Check the
current Compose specification and CLI documentation for supported
behavior.

### Applications still need retries

Even with health checks, robust applications should:

-   Retry transient connection failures.
-   Use bounded timeouts and backoff.
-   Reconnect when a database or cache restarts.
-   Fail clearly when configuration is invalid.
-   Avoid assuming a dependency stays healthy forever.

A health check reports a condition; it does not repair a broken service
or replace monitoring.

## 12. Build your own image with Compose

A service can build an image from a Dockerfile:

``` yaml
services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
    image: local-api:dev
    ports:
      - "127.0.0.1:8000:8000"
```

Commands:

``` bash
docker compose build
docker compose up -d
docker compose up -d --build
docker compose images
```

-   `context` identifies the build context directory.
-   `dockerfile` selects the Dockerfile path relative to the context
    unless configured otherwise.
-   `image` gives the resulting image a name/tag.
-   Keep secrets, `.git`, virtual environments, caches, and unrelated
    large files out of the build context using `.dockerignore`.

Example `.dockerignore`:

``` text
.git
.env
__pycache__/
*.py[cod]
.venv/
venv/
node_modules/
```

Only exclude paths that your build does not require. If a file is needed
during the build, removing it from the context will make the build fail.

## 13. Essential Compose commands

Run commands from the project directory, or use
`-f path/to/compose.yaml` to specify a file.

  -----------------------------------------------------------------------------
  Task                                Command
  ----------------------------------- -----------------------------------------
  Validate/render configuration       `docker compose config`

  List services                       `docker compose config --services`

  Start services                      `docker compose up -d`

  Build and start                     `docker compose up -d --build`

  View service status                 `docker compose ps`

  Follow all logs                     `docker compose logs -f`

  Follow one service                  `docker compose logs -f web`

  Run a command in a running service  `docker compose exec web sh`

  Start a one-off container           `docker compose run --rm web <command>`

  Stop services                       `docker compose stop`

  Start stopped services              `docker compose start`

  Restart services                    `docker compose restart`

  Stop and remove containers/network  `docker compose down`

  Remove containers and declared      `docker compose down --volumes`
  volumes                             

  Pull configured images              `docker compose pull`

  Build configured images             `docker compose build`

  List project images                 `docker compose images`
  -----------------------------------------------------------------------------

Be careful with `down --volumes`, volume-pruning commands, and any reset
command in a project that contains useful data.

## 14. Troubleshooting

### A. YAML parsing error

``` bash
docker compose config
```

Check:

-   Indentation and spaces.
-   Correct nesting under `services`, service names, and top-level
    `volumes`/`networks`.
-   Quoting values that contain colons or other YAML-significant
    characters.
-   Correct variable syntax such as `${VARIABLE}`.

### B. Container exits immediately

``` bash
docker compose ps -a
docker compose logs <service>
docker inspect <container_name>
```

Check the application command, environment, required files, and exit
code. A service must run a foreground process for its container to
remain running.

### C. Application cannot connect to database

1.  Confirm the database service is running and healthy.
2.  Use the Compose service name as the hostname, e.g. `db`.
3.  Use the database container port, e.g. `5432`, not a host-published
    port.
4.  Confirm both services share a network.
5.  Verify credentials and database name.
6.  Check database logs and application logs.
7.  Add retries and timeouts to the application.

### D. Port is already allocated

``` bash
docker compose ps
docker ps
```

Change the host-side port mapping or stop the conflicting service if
appropriate. For local-only use, consider mapping to `127.0.0.1`.

### E. Changes to environment variables seem ignored

Re-render the config:

``` bash
docker compose config
```

Then recreate the service if required:

``` bash
docker compose up -d --force-recreate <service>
```

Some image initialization variables only apply when a data directory is
first initialized. Recreating a container does not necessarily reset its
named volume or database state.

### F. Data appears to have disappeared

``` bash
docker volume ls
docker volume inspect <volume_name>
docker compose config
```

Check whether the service is using the expected named volume, whether
the project name changed, whether a bind mount points to a different
path, and whether the volume was removed. Do not run cleanup/prune
commands until you understand which resources they will remove.

### G. Container is healthy but application requests fail

A health check may only verify that a process responds to a narrow test.
Check the actual application endpoint, logs, network membership,
listening address, ports, and dependencies.

## 15. Production and security practices

-   **Pin versions intentionally:** choose supported image versions and
    plan updates; avoid relying on `latest` for reproducible
    deployments.
-   **Use non-root users where feasible:** ensure required directories
    and mounted files have appropriate ownership and permissions.
-   **Limit published ports:** publish only the entry points that
    require host access.
-   **Keep databases private:** internal service communication usually
    does not require publishing database ports.
-   **Protect secrets:** `.env` is plain text; keep it out of source
    control and use an appropriate secret manager in production.
-   **Set resource limits thoughtfully:** configure CPU and memory
    constraints based on tested application requirements and supported
    Compose/runtime behavior.
-   **Use health checks:** make them meaningful and avoid tests that are
    too expensive or too frequent.
-   **Use restart policies deliberately:** they can restart exited
    containers but do not replace application resilience, monitoring, or
    an orchestrator.
-   **Back up persistent data:** volumes alone do not protect against
    deletion, corruption, host failure, or ransomware.
-   **Avoid privileged mode:** do not set `privileged: true` unless a
    justified requirement exists and the risk is understood.
-   **Protect the Docker daemon:** Docker control can confer broad host
    privileges.
-   **Review rendered configuration:** `docker compose config` may
    include interpolated values.
-   **Separate development and deployment config:** use controlled
    overrides or environment-specific configuration without duplicating
    the whole stack unnecessarily.
-   **Test recovery:** verify backups by restoring them in a separate
    environment.

Compose is useful for development, testing, and many single-host
deployments. A multi-host production architecture may need a separate
orchestration and operations strategy.

## 16. Docker Compose vs. `docker run` vs. Kubernetes

  -------------------------------------------------------------------------------
  Capability        `docker run`      Docker Compose    Kubernetes
  ----------------- ----------------- ----------------- -------------------------
  Main use          Start an          Define and        Orchestrate containerized
                    individual        operate a         workloads across a
                    container         multi-container   cluster
                                      application       

  Configuration     CLI flags         YAML service      Kubernetes resource
                                      configuration     manifests/API

  Service           Configure         Project networks  Cluster networking and
  networking        manually or use   and service-name  Services
                    Docker networks   discovery         

  Persistent        Mount volumes     Declare volumes   PersistentVolumes,
  storage           manually          in Compose YAML   PersistentVolumeClaims,
                                                        and storage classes

  Scaling           Start additional  Supports scaling  Workload controllers and
                    containers        some services;    scheduling
                    manually          depends on app    
                                      design            

  Multi-node        Not provided by   Not a             Built for cluster
  scheduling        `docker run`      general-purpose   orchestration
                    itself            multi-node        
                                      scheduler         

  Best learning     Container         Local             Cluster orchestration and
  focus             fundamentals      multi-service     operations
                                      applications      
  -------------------------------------------------------------------------------

Compose and Kubernetes solve related but different problems. Compose
knowledge is valuable for understanding services, configuration,
networking, and persistence before learning Kubernetes manifests and
cluster operations.

## 17. Interview questions and answers

### 1. What is Docker Compose?

A tool for defining and managing multi-container applications through a
declarative YAML configuration file and the `docker compose` CLI.

### 2. What is a service in Compose?

A declaration that specifies how to run a component of the application,
including its image or build context, environment, networks, ports, and
storage.

### 3. What is the difference between `image` and `build`?

`image` selects an image to run; `build` tells Compose how to build an
image from a build context and Dockerfile. They can be used together to
assign a name to the built image.

### 4. What does `docker compose up -d` do?

It creates or recreates required resources and starts the services in
detached mode, so the command returns while containers run in the
background.

### 5. What is the purpose of `docker compose down`?

It stops and removes the project's containers and networks. Named
volumes are normally preserved unless volume removal is requested.

### 6. Does `depends_on` guarantee the database is ready?

Not by itself. It can order startup; readiness requires a meaningful
health check and supported `condition: service_healthy` configuration.
Applications should still handle retries.

### 7. How do containers communicate in a Compose project?

Services attached to the same Compose network can generally reach one
another using service names and container ports.

### 8. Why should an API connect to `db:5432` instead of `localhost:5432`?

Within the API container, `localhost` points to the API container
itself. `db` resolves to the database service on the shared Compose
network.

### 9. What is the difference between `ports` and `expose`?

`ports` publishes a container port through a host port. `expose`
documents an internal service port but does not publish it to the host.

### 10. How do you persist database data in Compose?

Declare a named volume and mount it at the database's data directory.
Then define backup and restore procedures separately.

### 11. Is `.env` secure for production passwords?

No. It is plain text configuration and should not be treated as
encrypted secret storage. Use appropriate secret-management controls for
production.

### 12. How do you view logs for a single service?

``` bash
docker compose logs -f <service>
```

### 13. How do you execute a command inside a running service?

``` bash
docker compose exec <service> <command>
```

For a one-off command in a new container, use `docker compose run --rm`.

### 14. How do you rebuild an application image after changing its source?

``` bash
docker compose up -d --build
```

Recreate affected services as needed and verify logs and health.

### 15. Why might a database keep its old password after changing `.env`?

The new environment may be passed to a recreated container, but database
initialization variables often apply only to a new data directory.
Change the database credential using database administration procedures;
do not delete the volume as a shortcut.

### 16. Does Compose provide automatic multi-host failover?

Compose is not a general-purpose multi-host scheduler or
high-availability platform. Choose an appropriate orchestration and
recovery design for that requirement.

### 17. What is a Compose project name?

It groups resources created for a Compose application and often prefixes
resource names. It can be set explicitly with the `-p` option or
supported project-name configuration.

### 18. How would you debug a service that starts but cannot reach Redis?

Check `docker compose ps`, logs, health, shared network membership,
service name, Redis port, listening state, credentials if enabled, and
application retry behavior.

## 18. Scope boundaries

This README covers:

-   Compose YAML and service configuration.
-   Local multi-container application patterns.
-   Service discovery, networks, ports, environment variables, health
    checks, and volumes.
-   Build and lifecycle commands, debugging, and production-minded
    configuration.

Related topics intentionally reserved for other notes:

-   Docker image layers and multistage builds.
-   Detailed volume and bind-mount internals.
-   Container security hardening, SELinux/AppArmor, capabilities,
    seccomp, and runtime policy.
-   Stateful database backup consistency, recovery, replication, and
    disaster recovery.
-   Kubernetes Deployments, Services, Ingress, storage resources, and
    cluster networking.

## 19. Official references

-   [Docker Compose overview](https://docs.docker.com/compose/)
-   [Compose file
    reference](https://docs.docker.com/reference/compose-file/)
-   [Compose getting
    started](https://docs.docker.com/compose/gettingstarted/)
-   [Compose
    networking](https://docs.docker.com/compose/how-tos/networking/)
-   [Compose volumes](https://docs.docker.com/compose/how-tos/volumes/)
-   [Compose environment
    variables](https://docs.docker.com/compose/how-tos/environment-variables/)
-   [Compose startup
    order](https://docs.docker.com/compose/how-tos/startup-order/)
-   [Docker Engine security](https://docs.docker.com/engine/security/)

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
└── 07-docker-compose/
    └── README.md
```

From the root of your cloned repository:

``` bash
mkdir -p 07-docker-compose
# Copy this README.md into that directory, then:
git add 07-docker-compose/README.md
git commit -m "Add Docker Compose notes and labs"
git push origin main
```
