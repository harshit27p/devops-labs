# Day 03 — Docker Compose, Networking, Volumes, Docker Hub & Docker Swarm

Hands-on notes and lab guide for **PGCP-ITISS — DevOps**.

This README consolidates the three supplied Day 03 PDFs:
- **Lab Guide:** Docker Compose labs, YAML troubleshooting, networking, persistence, image builds, Docker Hub, capstone, cleanup, and self-assessment.
- **Session 1:** YAML fundamentals, Compose service lifecycle, multi-service applications, network isolation, named volumes, and Docker Hub.
- **Session 2:** Container orchestration fundamentals and Docker Swarm.

> **Environment:** Docker Desktop on Windows 10/11 with Git Bash, or Docker Engine on Linux/macOS. Commands assume a working Docker Engine and modern `docker compose` (Compose V2).

---

## Table of Contents

1. [Learning Objectives](#learning-objectives)
2. [Prerequisites and Workspace](#prerequisites-and-workspace)
3. [Docker Compose and YAML Fundamentals](#docker-compose-and-yaml-fundamentals)
4. [Essential Compose Commands](#essential-compose-commands)
5. [Lab 1 — YAML Syntax Troubleshooting](#lab-1--yaml-syntax-troubleshooting)
6. [Lab 2 — Single-Service Nginx Stack](#lab-2--single-service-nginx-stack)
7. [Lab 3 — Two-Tier Backend and PostgreSQL](#lab-3--two-tier-backend-and-postgresql)
8. [Lab 4 — Network Segmentation and Isolation](#lab-4--network-segmentation-and-isolation)
9. [Lab 5 — Bind Mounts and Persistent Database Storage](#lab-5--bind-mounts-and-persistent-database-storage)
10. [Lab 6 — Build a Custom Python API Image](#lab-6--build-a-custom-python-api-image)
11. [Lab 7 — Publish Images to Docker Hub](#lab-7--publish-images-to-docker-hub)
12. [Capstone — Three-Tier Enterprise-Style Stack](#capstone--three-tier-enterprise-style-stack)
13. [Docker Swarm Orchestration](#docker-swarm-orchestration)
14. [Troubleshooting](#troubleshooting)
15. [Cleanup](#cleanup)
16. [Self-Assessment and Review Questions](#self-assessment-and-review-questions)

---

## Learning Objectives

By completing the labs, you should be able to:

- Write valid YAML and troubleshoot common indentation and syntax errors.
- Define and manage services declaratively with Docker Compose.
- Start, inspect, log, execute commands in, and remove multi-container applications.
- Use Compose DNS service discovery instead of hard-coded container IP addresses.
- Keep a database on a private network without publishing its port to the host.
- Segment a stack using frontend and backend bridge networks.
- Explain the difference between bind mounts and named volumes.
- Prove that named-volume database data survives container recreation.
- Build a custom image from a Dockerfile using `build.context`.
- Tag and push versioned images to Docker Hub.
- Explain Docker Swarm managers, workers, services, tasks, overlay networks, routing mesh, scaling, rolling updates, and rollbacks.

## Prerequisites and Workspace

### Verify Docker

```bash
docker --version
docker compose version
docker info
```

`docker info` must be able to reach the Docker Engine. On Windows, start Docker Desktop and wait for its engine to become ready before running Compose commands.

### Create the lab workspace

```bash
mkdir -p ~/docker-compose-lab
cd ~/docker-compose-lab
```

Each lab should have its own directory and its own `docker-compose.yml`. Run `docker compose` commands from the directory containing the relevant Compose file.

Suggested layout:

```text
docker-compose-lab/
├── lab1-yaml/
│   └── docker-compose.yml
├── lab2-single-service/
│   └── docker-compose.yml
├── lab3-two-tier/
│   └── docker-compose.yml
├── lab4-networks/
│   └── docker-compose.yml
├── lab5-storage/
│   ├── docker-compose.yml
│   ├── nginx.conf
│   └── html/
│       └── index.html
└── lab6-build/
    ├── docker-compose.yml
    └── api/
        ├── app.py
        └── Dockerfile
```

---

## Docker Compose and YAML Fundamentals

Docker Compose is a declarative tool for defining and running multi-container applications. Instead of repeatedly entering a long `docker run` command, describe the desired services, networks, ports, environment variables, and volumes in `docker-compose.yml`.

### YAML rules

1. **Use spaces, never tabs.** Two spaces per indentation level is a common convention.
2. **YAML is case-sensitive.** `services:` and `Services:` are different keys.
3. **Put a space after a key's colon.** Use `image: nginx:alpine`, not `image:nginx:alpine`.
4. **Use hyphens for list items.** For example, `- '8080:80'`.
5. **Quote port mappings.** Use `'8080:80'` or `"80:80"` to keep them unambiguously as strings.
6. **Use `|` or `>` for multi-line values.** `|` preserves line breaks; `>` folds line breaks into spaces.
7. **Keep sibling keys aligned.** `image`, `ports`, and `restart` must be at the same indentation level inside a service.

Modern Docker Compose V2 does not require the old top-level `version: '3.8'` field. Omitting it avoids the “version is obsolete” warning.

### Common YAML errors

| Problem | Incorrect | Correct |
|---|---|---|
| Tabs used for indentation | A tab before `web:` | Two spaces before `web:` |
| Missing space after colon | `image:nginx:alpine` | `image: nginx:alpine` |
| Unquoted port mapping | `- 80:80` | `- '80:80'` |
| Misaligned service | `web:` at the same level as `image:` | `web:` under `services:`, `image:` under `web:` |

Always validate a file before starting containers:

```bash
docker compose config
```

---

## Essential Compose Commands

Run these from the directory containing `docker-compose.yml`.

```bash
# Validate and render the Compose configuration
docker compose config

# Start services in the background
docker compose up -d

# Build images and start/recreate services
docker compose up -d --build

# Show service status
docker compose ps

# Follow logs for all services
docker compose logs -f

# Show the last 50 log lines for a service
docker compose logs --tail=50 web

# Run a command inside a running service
docker compose exec web nginx -v

# Stop and remove project containers and networks
docker compose down

# Also remove named volumes declared by the Compose project (DESTRUCTIVE)
docker compose down -v
```

**Important:** `docker compose down` normally keeps named volumes. `docker compose down -v` removes Compose-managed named volumes and can permanently delete database data. Use it only when you intentionally want to reset the database.

---

## Lab 1 — YAML Syntax Troubleshooting

### Objective

Intentionally identify common YAML mistakes and learn to validate a Compose file.

### Create the workspace

```bash
mkdir -p ~/docker-compose-lab/lab1-yaml
cd ~/docker-compose-lab/lab1-yaml
```

### Valid minimal Compose file

```bash
cat << 'EOF' > docker-compose.yml
services:
  web:
    image: nginx:alpine
EOF
```

Validate:

```bash
docker compose config
```

The output should show a parsed configuration. If validation fails, inspect indentation, colons, and quotes before starting anything.

### Practice errors

Try these one at a time, validating after each change:

- Insert a tab before `web:` and observe the YAML parsing error; replace the tab with spaces.
- Change `image: nginx:alpine` to `image:nginx:alpine`; restore the space after the colon.
- Use an unquoted port mapping; then quote it as `'8080:80'`.

### Checkpoint

You should understand why YAML indentation is structural, why tabs cause errors, and why quoted port mappings are recommended.

---

## Lab 2 — Single-Service Nginx Stack

### Objective

Replace a standalone `docker run` command with a repeatable Compose definition.

### Create the workspace and file

```bash
mkdir -p ~/docker-compose-lab/lab2-single-service
cd ~/docker-compose-lab/lab2-single-service

cat << 'EOF' > docker-compose.yml
services:
  web:
    image: nginx:alpine
    container_name: lab-web-server
    ports:
      - '8080:80'
    restart: always
EOF
```

### Run and verify

```bash
docker compose config
docker compose up -d
docker compose ps
curl -I http://localhost:8080
docker compose logs --tail=10 web
docker compose exec web nginx -v
```

Open `http://localhost:8080` in a browser. The expected HTTP response includes `200 OK` if the service is running and port 8080 is available.

### What the settings mean

- `image`: image to run; Docker pulls it if needed.
- `container_name`: explicit container name.
- `ports`: publishes host port 8080 to container port 80.
- `restart: always`: asks Docker to restart the container when it stops, subject to Docker's restart-policy behavior.

### Clean up

```bash
docker compose down
```

---

## Lab 3 — Two-Tier Backend and PostgreSQL

### Objective

Run an application container and a PostgreSQL database on the same Compose network. Compose provides service-name DNS, so the backend can use `db` rather than a hard-coded IP address.

### Create the workspace

```bash
mkdir -p ~/docker-compose-lab/lab3-two-tier
cd ~/docker-compose-lab/lab3-two-tier
```

### Compose file

```bash
cat << 'EOF' > docker-compose.yml
services:
  # Tier 1: Application backend
  backend:
    image: python:3.11-slim
    container_name: lab-api-server
    command: >
      sh -c "echo 'API Server starting...' &&
      python -m http.server 5000"
    ports:
      - '5000:5000'
    environment:
      - DB_HOST=db
      - DB_PORT=5432
      - DB_NAME=company_db
      - DB_USER=db_admin
      - DB_PASSWORD=${DB_PASSWORD:-change-me-for-local-lab}
    depends_on:
      - db
    restart: unless-stopped

  # Tier 2: PostgreSQL database
  db:
    image: postgres:15-alpine
    container_name: lab-postgres-db
    environment:
      POSTGRES_DB: company_db
      POSTGRES_USER: db_admin
      POSTGRES_PASSWORD: ${DB_PASSWORD:-change-me-for-local-lab}
    # No host port is published for PostgreSQL.
    restart: unless-stopped
EOF
```

For this lab, `DB_PASSWORD` is supplied from the shell or a local `.env` file. Do not commit real credentials. The Python built-in HTTP server in this example is a simple file server; it does **not** implement database queries or a real API despite the example's backend label.

### Start and inspect

```bash
docker compose config
docker compose up -d
docker compose ps
docker compose logs --tail=50 db
docker compose logs --tail=50 backend
```

The database should not have a host mapping such as `0.0.0.0:5432->5432/tcp`. It remains reachable from containers on the Compose network.

### Test service-name DNS

```bash
docker compose exec backend python -c "import socket; print('db resolves to:', socket.gethostbyname('db'))"
```

### Test TCP connectivity to PostgreSQL

The `python:3.11-slim` image may not include `ping`. Use Python's socket library to test the actual database port:

```bash
docker compose exec backend python -c "import socket; s=socket.create_connection(('db',5432),timeout=5); print('SUCCESS: PostgreSQL port 5432 is reachable'); s.close()"
```

To inspect container DNS configuration on Git Bash, avoid MSYS path rewriting:

```bash
MSYS_NO_PATHCONV=1 docker compose exec backend cat /etc/resolv.conf
```

Docker commonly uses its embedded DNS resolver at `127.0.0.11` on user-defined networks.

### Optional: insert and query sample orders

```bash
docker compose exec db psql -U db_admin -d company_db -c "CREATE TABLE orders (order_id SERIAL PRIMARY KEY, product VARCHAR(50), amount INT); INSERT INTO orders (product, amount) VALUES ('DevOps Bootcamp', 499), ('Cloud Voucher', 150);"
```

Query:

```bash
docker compose exec db psql -U db_admin -d company_db -c "SELECT * FROM orders;"
```

If the table already exists, run only the `INSERT` statement or use a fresh disposable lab database.

### Clean up

```bash
docker compose down
```

---

## Lab 4 — Network Segmentation and Isolation

### Objective

Use two custom bridge networks to separate public-facing services from the database tier.

- `frontend-net`: Nginx proxy and backend.
- `backend-net`: backend and database.
- Backend is **dual-homed**, meaning it joins both networks.
- Web and database share no network, so the web service should not be able to resolve the database service name.

### Create the workspace and file

```bash
mkdir -p ~/docker-compose-lab/lab4-networks
cd ~/docker-compose-lab/lab4-networks

cat << 'EOF' > docker-compose.yml
services:
  # Public-facing web proxy
  web:
    image: nginx:alpine
    container_name: net-web-proxy
    ports:
      - '8080:80'
    networks:
      - frontend-net
    depends_on:
      - backend
    restart: always

  # Backend joins both networks
  backend:
    image: python:3.11-slim
    container_name: net-api-server
    command: >
      sh -c "echo 'API ready...' &&
      python -m http.server 5000"
    ports:
      - '5000:5000'
    environment:
      - DB_HOST=db
      - DB_PORT=5432
    networks:
      - frontend-net
      - backend-net
    depends_on:
      - db
    restart: unless-stopped

  # Private database tier
  db:
    image: postgres:15-alpine
    container_name: net-postgres-db
    environment:
      POSTGRES_DB: secure_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD:-change-me-for-local-lab}
    networks:
      - backend-net
    restart: unless-stopped

networks:
  frontend-net:
    driver: bridge
  backend-net:
    driver: bridge
EOF
```

> Nginx is attached to `frontend-net`, but this basic configuration does not yet proxy requests to the backend. The backend is published on host port 5000 for lab testing. Remove that `ports` mapping if it should only be reachable by other containers.

### Launch and inspect the networks

```bash
docker compose config
docker compose up -d
docker compose ps
docker network ls
```

Inspect the network membership. Actual network names usually include the Compose project name:

```bash
docker network inspect lab4-networks_frontend-net
docker network inspect lab4-networks_backend-net
```

If your names differ, copy them from `docker network ls`.

### Verify expected communication

Backend to database should resolve and connect:

```bash
docker compose exec backend python -c "import socket; print(socket.gethostbyname('db'))"
docker compose exec backend python -c "import socket; s=socket.create_connection(('db',5432),timeout=5); print('backend -> db:5432 works'); s.close()"
```

Web to backend should resolve:

```bash
docker compose exec web sh -c 'getent hosts backend || true'
```

Web to database should **not** resolve `db`, because `web` and `db` do not share a network:

```bash
docker compose exec web sh -c 'getent hosts db'
```

The last command is expected to return no database address or a lookup failure. Minimal images may not include `ping` or `getent`; in that case, use a temporary diagnostic container attached to the relevant network or inspect network membership instead.

### Clean up

```bash
docker compose down
```

---

## Lab 5 — Bind Mounts and Persistent Database Storage

### Objective

Use bind mounts for host-managed configuration and web content, and a named volume for PostgreSQL data.

- **Bind mount:** Maps a specific host path into a container. Useful for local configuration and live-edited static content.
- **Named volume:** Docker-managed persistent storage. Suitable for stateful database files.
- `:ro` means read-only inside the container.
- `docker compose down` keeps named volumes by default; `docker compose down -v` deletes them.

### Create the workspace

```bash
mkdir -p ~/docker-compose-lab/lab5-storage/html
cd ~/docker-compose-lab/lab5-storage
```

### Create Nginx configuration

```bash
cat << 'EOF' > nginx.conf
events {
    worker_connections 1024;
}

http {
    server {
        listen 80;

        location / {
            root /usr/share/nginx/html;
            index index.html;
        }
    }
}
EOF
```

### Create the HTML page

```bash
cat << 'EOF' > html/index.html
<!DOCTYPE html>
<html>
<head>
    <title>DevOps Docker Compose Lab</title>
</head>
<body style="font-family: Arial; text-align: center; margin-top: 50px;">
    <h1>Welcome to Docker Compose Persistent Storage!</h1>
    <p>Version: 1.0 (Live Bind Mount)</p>
</body>
</html>
EOF
```

### Compose configuration

```bash
cat << 'EOF' > docker-compose.yml
services:
  web:
    image: nginx:alpine
    container_name: store-web-server
    ports:
      - '8080:80'
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./html:/usr/share/nginx/html:ro
    restart: always

  db:
    image: postgres:15-alpine
    container_name: store-postgres-db
    environment:
      POSTGRES_DB: customer_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD:-change-me-for-local-lab}
    volumes:
      - db-persistent-data:/var/lib/postgresql/data
    restart: always

volumes:
  db-persistent-data:
    driver: local
EOF
```

### Test live bind-mount updates

```bash
docker compose config
docker compose up -d
curl -s http://localhost:8080
```

Edit `html/index.html` on the host and change the version text from `1.0` to `2.0`. Refresh the browser or run:

```bash
curl -s http://localhost:8080
```

The updated host file should be visible without rebuilding the image or restarting the container.

### Test database persistence

Create a table and sample rows:

```bash
docker compose exec db psql -U postgres -d customer_db -c "CREATE TABLE orders (order_id SERIAL PRIMARY KEY, product VARCHAR(50), amount INT); INSERT INTO orders (product, amount) VALUES ('DevOps Bootcamp', 499), ('Cloud Voucher', 150);"
```

Query the table:

```bash
docker compose exec db psql -U postgres -d customer_db -c "SELECT * FROM orders;"
```

Now remove containers and networks **without deleting the volume**:

```bash
docker compose down
docker volume ls
docker compose up -d
```

Query the table again:

```bash
docker compose exec db psql -U postgres -d customer_db -c "SELECT * FROM orders;"
```

The records should still exist because PostgreSQL data is stored in `db-persistent-data`.

### Destructive reset — use only when intended

```bash
docker compose down -v
```

This deletes the Compose-managed named volume and its database data. Verify with `docker volume ls`. Do not run this if you need to keep the lab data.

---

## Lab 6 — Build a Custom Python API Image

### Objective

Build a custom image from local source using Compose `build.context` and a Dockerfile.

### Create the workspace

```bash
mkdir -p ~/docker-compose-lab/lab6-build/api
cd ~/docker-compose-lab/lab6-build
```

### Create `api/app.py`

```bash
cat << 'EOF' > api/app.py
import os
from http.server import HTTPServer, BaseHTTPRequestHandler


class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        app_env = os.getenv('APP_ENV', 'development')
        response = (
            f'{{"status": "UP", "environment": "{app_env}", "version": "1.0"}}'
        )
        self.wfile.write(response.encode('utf-8'))


if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8000), SimpleHandler)
    print("API Server listening on port 8000...")
    server.serve_forever()
EOF
```

This is a small standard-library HTTP handler returning a JSON health-like response. It is suitable for the lab, not a production API framework.

### Create `api/Dockerfile`

```bash
cat << 'EOF' > api/Dockerfile
FROM python:3.11-alpine

WORKDIR /app

COPY app.py .

EXPOSE 8000

CMD ["python", "app.py"]
EOF
```

### Create the Compose file

```bash
cat << 'EOF' > docker-compose.yml
services:
  custom-api:
    build:
      context: ./api
      dockerfile: Dockerfile
    image: my-company/custom-api:1.0
    container_name: build-api-server
    ports:
      - '8000:8000'
    environment:
      - APP_ENV=production
    restart: unless-stopped
EOF
```

### Build, run, and test

```bash
docker compose config
docker compose up -d --build
docker compose ps
docker compose logs --tail=50 custom-api
curl -s http://localhost:8000
```

Expected response:

```json
{"status": "UP", "environment": "production", "version": "1.0"}
```

### Change the version and rebuild

Edit `api/app.py`, changing `"version": "1.0"` to `"version": "2.0"`, then run:

```bash
docker compose up -d --build
curl -s http://localhost:8000
```

Expected response now contains `"version": "2.0"`.

### Clean up

```bash
docker compose down
```

---

## Lab 7 — Publish Images to Docker Hub

### Objective

Authenticate to Docker Hub, tag local images using a personal namespace and version tags, push them, and verify they can be pulled.

### Log in

```bash
docker login
```

Use your Docker Hub username and the supported authentication method, such as a personal access token when required. Never put tokens into source code or commit them to Git.

### Tag the custom API image

Replace `YOUR_DOCKERHUB_USERNAME` with your Docker Hub username:

```bash
docker tag my-company/custom-api:1.0 YOUR_DOCKERHUB_USERNAME/custom-api:v1.0
docker tag my-company/custom-api:1.0 YOUR_DOCKERHUB_USERNAME/custom-api:latest
```

### Push both tags

```bash
docker push YOUR_DOCKERHUB_USERNAME/custom-api:v1.0
docker push YOUR_DOCKERHUB_USERNAME/custom-api:latest
```

### Verify by pulling

```bash
docker pull YOUR_DOCKERHUB_USERNAME/custom-api:v1.0
docker image ls
```

You can also repeat the workflow for a custom web image, using the same pattern:

```bash
docker tag custom-web:v1.0 YOUR_DOCKERHUB_USERNAME/custom-web:v1.0
docker tag custom-web:v1.0 YOUR_DOCKERHUB_USERNAME/custom-web:latest
docker push YOUR_DOCKERHUB_USERNAME/custom-web:v1.0
docker push YOUR_DOCKERHUB_USERNAME/custom-web:latest
docker pull YOUR_DOCKERHUB_USERNAME/custom-web:v1.0
```

The `custom-web:v1.0` image must exist locally before tagging. A versioned tag such as `v1.0` makes deployments more reproducible than relying only on the mutable `latest` tag.

---

## Capstone — Three-Tier Enterprise-Style Stack

### Target architecture

The capstone combines the concepts from the previous labs:

1. **Web tier:** Nginx reverse proxy, host port 80, bind-mounted `nginx.conf` and static HTML, attached to `public-net`.
2. **Backend tier:** Custom application image, host port 5000 in the lab specification, attached to both `public-net` and `private-net`, with `DB_HOST=database`.
3. **Database tier:** PostgreSQL 15 Alpine, attached only to `private-net`, no published host port, and a named volume mounted at `/var/lib/postgresql/data`.

Expected verification goals from the lab guide:

- `curl http://localhost:80` reaches the web proxy.
- `curl http://localhost:5000` reaches the backend.
- The web container cannot resolve or connect to `database` because the web and database tiers share no network.
- Database records survive `docker compose down` followed by `docker compose up -d`, because the named volume is retained.

### Important implementation note

A complete working reverse-proxy stack requires an Nginx configuration with an `upstream` or `proxy_pass` that points to the backend service name and port. Merely attaching Nginx and the backend to the same network does not automatically configure HTTP proxying. The basic `python -m http.server` examples are file servers rather than database-backed APIs. Treat the capstone as complete only after the proxy route and application endpoints are configured and tested.

### Verification checklist

```bash
docker compose config
docker compose up -d --build
docker compose ps
docker compose logs --tail=100
curl -I http://localhost:80
curl -s http://localhost:5000
docker network ls
docker volume ls
```

For network isolation, inspect network membership and verify the web service cannot resolve the database service name.

---

## Docker Swarm Orchestration

The Session 2 PDF introduces Docker Swarm as Docker's native clustering and orchestration engine. It addresses production concerns that a single Docker host cannot fully handle by itself:

- High availability if a host fails.
- Scaling replicas during traffic spikes.
- Self-healing and rescheduling tasks.
- Rolling updates and rollbacks.
- Distributing incoming traffic across service replicas.

### Swarm architecture

- **Manager nodes:** Maintain cluster state, schedule services, and dispatch tasks. Managers use Raft consensus to maintain a consistent state.
- **Worker nodes:** Execute assigned tasks and report task state.
- **Service:** Declarative desired state, such as “run three Nginx replicas.”
- **Task:** A scheduled unit of work corresponding to one container instance.
- **Container:** The running instance created for a task.

For manager high availability, the supplied session recommends an odd number of managers (3, 5, or 7). A majority quorum is required: `floor(N / 2) + 1`.

### Initialize a Swarm

On the first manager node, use an IP address that is reachable by other nodes. Replace the example address with the manager's real interface IP:

```bash
docker swarm init --advertise-addr 192.168.1.10
```

Get a worker join command/token:

```bash
docker swarm join-token worker
```

Get a manager join command/token:

```bash
docker swarm join-token manager
```

List nodes from a manager:

```bash
docker node ls
```

Do not publish join tokens; they allow nodes to join the cluster.

### Create and inspect a service

```bash
docker service create --name web-service --replicas 1 -p 80:80 nginx:latest
docker service ls
docker service ps web-service
docker service inspect --pretty web-service
docker service logs -f web-service
```

### Scale a service

```bash
docker service scale web-service=10
docker service ps web-service

docker service scale web-service=2
docker service ps web-service
```

Swarm attempts to reconcile the number of running tasks with the desired replica count.

### Rolling update and rollback

```bash
docker service update \
  --image nginx:1.25-alpine \
  --update-parallelism 2 \
  --update-delay 10s \
  --update-failure-action rollback \
  web-service
```

Check progress:

```bash
docker service ps web-service
```

Manually roll back if required:

```bash
docker service rollback web-service
```

### Swarm networking concepts

- **Overlay networks:** Allow containers on different Swarm hosts to communicate. The session describes VXLAN encapsulation over UDP port 4789.
- **Ingress routing mesh:** Any Swarm node can accept connections on a published service port and route traffic to an active task on another node.
- **Raft consensus:** Managers use it to agree on cluster state and support manager high availability.

### Remove the lab service and leave Swarm

```bash
docker service rm web-service
```

To leave a Swarm from a worker:

```bash
docker swarm leave
```

On a manager, leaving a cluster requires care. For a disposable single-node lab only, use `docker swarm leave --force` after removing services and understanding that this leaves the Swarm.

---

## Troubleshooting

### Docker Engine unavailable

Example: `failed to connect to the Docker API` or missing `dockerDesktopLinuxEngine` pipe.

1. Start Docker Desktop and wait for it to become ready.
2. Check:

   ```bash
   docker version
   docker info
   docker context ls
   ```

3. If `desktop-linux` is listed, select it:

   ```bash
   docker context use desktop-linux
   ```

### Compose reports obsolete `version`

Remove the top-level line `version: '3.8'`. Modern Compose uses the Compose Specification and ignores this field.

### `ping: executable file not found`

Minimal images may not include `ping`. This does not prove that networking is broken. Test DNS and TCP directly:

```bash
docker compose exec backend python -c "import socket; print(socket.gethostbyname('db'))"
docker compose exec backend python -c "import socket; s=socket.create_connection(('db',5432),timeout=5); print('TCP connection succeeded'); s.close()"
```

### Git Bash changes Linux paths

For commands that pass paths such as `/etc/resolv.conf` as arguments, Git Bash may rewrite the path to a Windows path. Try:

```bash
MSYS_NO_PATHCONV=1 docker compose exec backend cat /etc/resolv.conf
```

### Port is already in use

Change the host side of a port mapping. For example, change `'80:80'` to `'8080:80'`, then recreate the service:

```bash
docker compose up -d
```

Access Nginx at `http://localhost:8080`.

### Container exits or reports unhealthy behavior

```bash
docker compose ps
docker compose logs --tail=100 SERVICE_NAME
docker compose config
```

Replace `SERVICE_NAME` with the Compose service key, such as `web`, `backend`, `db`, or `custom-api`.

### Database data appears missing

- Confirm the named volume is declared at the top level and mounted to the correct PostgreSQL data directory.
- Check `docker volume ls`.
- Remember that `docker compose down -v` deletes the Compose project's named volumes.
- A change to `POSTGRES_DB`, `POSTGRES_USER`, or `POSTGRES_PASSWORD` does not automatically reinitialize an already populated data directory.

---

## Cleanup

### Remove individual Compose stacks

Run from each lab directory:

```bash
cd ~/docker-compose-lab/lab2-single-service && docker compose down
cd ~/docker-compose-lab/lab3-two-tier && docker compose down
cd ~/docker-compose-lab/lab4-networks && docker compose down
cd ~/docker-compose-lab/lab5-storage && docker compose down
cd ~/docker-compose-lab/lab6-build && docker compose down
```

For the storage lab, use `docker compose down -v` only if you deliberately want to delete its database volume.

### Optional Docker cleanup

The lab guide includes these commands:

```bash
docker network prune -f
docker volume prune -f
```

**Caution:** These prune unused Docker networks and volumes across the Docker host, not just this lab. Inspect resources first and do not run them if other projects depend on unused-looking volumes.

Verify current state:

```bash
docker ps -a
docker network ls
docker volume ls
```

---

## Self-Assessment and Review Questions

Use this checklist after completing the labs:

- [ ] I can explain why YAML forbids tabs for indentation and why consistent spaces matter.
- [ ] I can author and launch a single-service Compose file with `docker compose up -d`.
- [ ] I understand why port mappings should be quoted.
- [ ] I can configure inter-service communication using environment variables and Compose DNS.
- [ ] I understand why a database port should not be published to the host unless needed.
- [ ] I can create custom bridge networks to isolate the database from the web tier.
- [ ] I can explain the difference between a named volume and a bind mount.
- [ ] I proved named-volume data survives `docker compose down`.
- [ ] I understand that `docker compose down -v` deletes named volumes.
- [ ] I can build an image from local source using `build.context`.
- [ ] I can log in, tag images with version tags, and push/pull them from Docker Hub.
- [ ] I can explain Swarm manager/worker roles, services, tasks, scaling, routing mesh, rolling updates, and rollbacks.

### Review questions

1. Why does YAML throw a parsing error when tabs are used for indentation?
2. Why should Compose port mappings such as `'8080:80'` be quoted?
3. Which Docker component resolves a Compose service name such as `db` to a container IP?
4. Should a database that is only needed by peer containers normally have a host `ports:` mapping?
5. What is the difference between `docker compose down` and `docker compose down -v`?
6. Why is using only the mutable `latest` tag risky for production deployments?
7. How does network segmentation prevent the web tier from directly reaching the database?
8. What is the difference between a Swarm service, task, and container?
9. Why do Swarm managers use Raft consensus and majority quorum?
10. How does the Swarm ingress routing mesh route traffic to a task on another node?
11. How do rolling updates and rollback settings help control deployment risk?

---

## Security and Lab Hygiene

- The supplied lab examples use demonstration passwords. Replace them with local-only lab values; never commit real credentials.
- Prefer environment variables, secret-management tools, or Docker secrets for sensitive values. A committed `.env` file can expose credentials.
- Do not publish PostgreSQL's port unless there is a specific, controlled requirement.
- Avoid publishing diagnostic tools or unnecessary ports in production images.
- Version images explicitly for reproducible deployment; treat `latest` as mutable.
- Before running prune or `down -v` commands, confirm that no other project depends on the affected resources.

---

## Reference Material

This README is based on the supplied files:
- `Lab-Guide(1).pdf` — Day 03 lab guide (23 pages).
- `Session-1(1).pdf` — Day 3 Session 1: Docker Compose and Docker Hub (19 pages).
- `Session-2(1).pdf` — Day 3 Session 2: Container Orchestration Fundamentals and Docker Swarm (5 pages).

The Compose labs follow the supplied material's progression: YAML → single service → backend/database → network segmentation → persistent storage → custom image builds → Docker Hub → three-tier capstone. The final section adds the Swarm concepts and commands covered in Session 2.
