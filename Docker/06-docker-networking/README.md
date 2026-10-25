# Docker Networking: Bridge, Host, Overlay, and Network Isolation

> **Video:** [Docker Networking --- DevOps Zero to
> Hero](https://www.youtube.com/watch?v=xrUGEoUpa3s&list=PLdpzxOOAlwvIc1TjTwopNSjRJkzES2ZXk&index=27)\
> **Course playlist:** [DevOps Zero to
> Hero](https://www.youtube.com/playlist?list=PLdpzxOOAlwvIc1TjTwopNSjRJkzES2ZXk)\
> **Suggested repository path:** `06-docker-networking/README.md`

These notes focus on Docker network drivers, container-to-container
communication, name resolution, port publishing, and logical isolation.
They complement the earlier Docker fundamentals and storage notes rather
than repeating them.

## Table of contents

-   [1. Learning objectives](#1-learning-objectives)
-   [2. Why Docker networking matters](#2-why-docker-networking-matters)
-   [3. Key networking terms](#3-key-networking-terms)
-   [4. Docker network drivers](#4-docker-network-drivers)
-   [5. Inspect existing networks](#5-inspect-existing-networks)
-   [6. Lab A --- Default bridge
    behavior](#6-lab-a--default-bridge-behavior)
-   [7. Lab B --- Custom bridge and DNS
    discovery](#7-lab-b--custom-bridge-and-dns-discovery)
-   [8. Lab C --- Isolating application
    tiers](#8-lab-c--isolating-application-tiers)
-   [9. Host networking](#9-host-networking)
-   [10. Overlay networking](#10-overlay-networking)
-   [11. Port publishing and firewall
    considerations](#11-port-publishing-and-firewall-considerations)
-   [12. Troubleshooting checklist](#12-troubleshooting-checklist)
-   [13. Security and production
    guidance](#13-security-and-production-guidance)
-   [14. Quick command reference](#14-quick-command-reference)
-   [15. Interview questions and
    answers](#15-interview-questions-and-answers)
-   [16. Scope of this note](#16-scope-of-this-note)
-   [17. Official references](#17-official-references)

## 1. Learning objectives

After completing the labs, you should be able to:

-   Explain how Docker networks connect containers and external clients.
-   Distinguish the default `bridge`, user-defined `bridge`, `host`, and
    `overlay` network drivers.
-   Create, inspect, attach, disconnect, and remove Docker networks.
-   Explain why service-name discovery works on a user-defined bridge.
-   Publish container ports safely and distinguish publishing from
    `EXPOSE`.
-   Isolate application tiers by placing containers on only the networks
    they need.
-   Troubleshoot DNS, routing, listening ports, and network attachment
    problems.

## 2. Why Docker networking matters

A container may need to communicate with:

-   Another container, such as a web frontend calling an API.
-   A database or cache container on a private application network.
-   The Docker host, for local development or host services.
-   A client outside the host, when a service port is intentionally
    published.
-   Containers on other Docker hosts, when using an appropriate
    multi-host networking solution.

Networking also helps define **reachability boundaries**. For example, a
reverse proxy might be reachable from the host-facing network, while a
database is attached only to a private backend network. This is useful
isolation, but it is not a substitute for application authentication,
database permissions, host firewall policy, or secret management.

### Typical two-tier design

``` text
Browser / API client
        |
    Host port 8080
        |
  [Web container]
        |
   private network
        |
  [API container]
        |
   private network
        |
 [Database container]
```

The diagram is conceptual: a real deployment may use separate networks
and attach the API to both frontend and database networks. Avoid
exposing the database port to the host unless there is a specific
operational need.

## 3. Key networking terms

  -----------------------------------------------------------------------
  Term                                Meaning
  ----------------------------------- -----------------------------------
  Network driver                      Implements a networking model, such
                                      as bridge, host, or overlay.

  Bridge                              A virtual Layer 2 network on a
                                      single Docker host.

  `docker0`                           The Linux bridge commonly used by
                                      Docker's default bridge network.

  Container IP                        An address assigned to a container
                                      on a particular network. It can
                                      change when containers are
                                      recreated.

  Port publishing                     Maps a host port to a container
                                      port, for example `-p 8080:80`.

  `EXPOSE`                            Image metadata documenting an
                                      intended container port; it does
                                      **not** publish the port by itself.

  User-defined bridge                 A bridge network created by the
                                      operator; supports automatic DNS
                                      resolution by container/service
                                      name.

  Overlay                             A network that can connect
                                      workloads across multiple Docker
                                      hosts in supported cluster setups.

  Network isolation                   Restricting which containers can
                                      directly reach one another by
                                      controlling their network
                                      attachments and firewall policy.
  -----------------------------------------------------------------------

### Important distinction: container port vs host port

In `-p 8080:80`, the usual interpretation is:

-   `8080`: port on the Docker host.
-   `80`: port inside the container.

For example:

``` bash
docker run -d --name web -p 127.0.0.1:8080:80 nginx
```

This publishes the container's port 80 on host loopback port 8080.
Binding to `127.0.0.1` makes it available locally on the host rather
than intentionally publishing it on all host interfaces. Exact behavior
can vary with platform and firewall configuration, so validate on the
target host.

## 4. Docker network drivers

### 4.1 Default bridge

Docker normally creates a default bridge network named `bridge`; on
Linux it is commonly backed by the `docker0` bridge interface.

-   Containers attached to the default bridge can generally reach one
    another by IP address, subject to firewall rules.
-   Automatic container-name DNS discovery is **not** provided on the
    default bridge in the same way it is on user-defined bridges.
-   Legacy links are not the recommended way to build new container
    networks.
-   Containers can often reach external networks through host routing
    and masquerading, depending on configuration.

### 4.2 User-defined bridge

This is generally the best choice for communication among containers on
one Docker host.

Advantages:

-   Containers on the same user-defined bridge can resolve each other by
    container name or network alias.
-   Networks can be created for distinct application groups.
-   Containers can be connected to or disconnected from the network as
    needed.
-   Network configuration is easier to inspect and manage than relying
    on the default bridge.

Example:

``` bash
docker network create app-net
docker run -d --name web --network app-net nginx
docker run --rm --network app-net busybox:1.36 nslookup web
```

The DNS test depends on the image being able to query DNS and the
container being on the same user-defined network.

### 4.3 Host network

Host networking removes the usual separate container network namespace
on supported Linux Docker setups: the container uses the host's network
namespace.

``` bash
docker run --rm --network host nginx
```

Consequences:

-   The container shares host networking rather than receiving a
    separate bridge-network IP.
-   Port publishing with `-p` is unnecessary and is ignored or not
    supported as a mapping in host mode.
-   Port conflicts are possible because services bind directly in the
    host network namespace.
-   Network isolation is reduced, so use it only when its trade-offs are
    understood.

Platform support and behavior differ. Docker Desktop has additional
virtualization constraints; verify current documentation for your
operating system.

### 4.4 Overlay network

Overlay networks provide multi-host connectivity in supported Docker
cluster environments, commonly Docker Swarm.

Typical uses:

-   Services scheduled across multiple Docker hosts.
-   Service-to-service traffic across nodes.
-   Separating traffic among groups of services in a swarm.

Overlay networking is **not simply "the Kubernetes network driver."**
Kubernetes has its own networking model and commonly relies on a
Container Network Interface (CNI) plugin. Docker overlay networks are a
Docker feature, especially associated with Swarm.

Example for a Swarm manager:

``` bash
docker swarm init
docker network create --driver overlay app-overlay
docker network ls
```

A standalone container on a single non-Swarm host cannot use a normal
Swarm overlay as if it were a local bridge. Swarm setup, node
membership, service deployment, and any required encryption/options must
be configured according to the Docker documentation.

### 4.5 Other drivers

Docker can also support drivers such as `none` (no container networking)
and `macvlan` (containers appear on a physical network with their own
MAC addresses, subject to network and host limitations). These are
specialized choices, not automatic replacements for bridge networking.

## 5. Inspect existing networks

Run these commands on a machine with Docker installed:

``` bash
# List networks
docker network ls

# Inspect the default bridge
docker network inspect bridge

# Inspect a network by name
docker network inspect app-net

# Show a container's network details
docker inspect web

# Print only network-related container data (Linux/macOS shell)
docker inspect --format '{{json .NetworkSettings.Networks}}' web
```

Look for:

-   Driver and scope.
-   Subnet and gateway.
-   Containers attached to the network.
-   Container IP addresses and network aliases.
-   Whether the network is local to one host or has a cluster-oriented
    scope.

Do not hard-code container IPs in application configuration when
service-name discovery is available. Container addresses can change when
containers are replaced.

## 6. Lab A --- Default bridge behavior

**Goal:** See the default bridge and understand why custom bridges are
usually easier to operate.

### Step 1: List networks

``` bash
docker network ls
```

You will normally see built-in networks such as `bridge`, `host`, and
`none`. The exact list depends on the Docker environment.

### Step 2: Start two containers on the default bridge

``` bash
docker run -dit --name default-a busybox:1.36 sh
docker run -dit --name default-b busybox:1.36 sh
```

### Step 3: Inspect addresses and attachment

``` bash
docker network inspect bridge
docker inspect default-a
docker inspect default-b
```

### Step 4: Test connectivity by IP

Find the IP address for `default-b` in the inspect output, then run:

``` bash
docker exec default-a ping -c 3 <DEFAULT_B_IP>
```

Replace `<DEFAULT_B_IP>` with the actual address. BusyBox builds differ,
and some images may not include every diagnostic utility. If `ping` is
unavailable, use another suitable diagnostic image or test the
application's actual TCP port.

### Step 5: Try name lookup

``` bash
docker exec default-a ping -c 1 default-b
```

Name-based discovery on the default bridge is not equivalent to the
built-in DNS discovery provided by user-defined bridges. Do not treat
this as a dependable service-discovery mechanism.

### Step 6: Clean up

``` bash
docker rm -f default-a default-b
```

**Expected lesson:** IP-level reachability and service-name discovery
are different concerns. User-defined bridge networks are the preferred
local networking pattern for most multi-container applications.

## 7. Lab B --- Custom bridge and DNS discovery

**Goal:** Create a network and verify that containers can communicate
using names.

### Step 1: Create a bridge

``` bash
docker network create --driver bridge lab-net
docker network ls
docker network inspect lab-net
```

### Step 2: Start containers on the network

``` bash
docker run -dit --name app-a --network lab-net busybox:1.36 sh
docker run -dit --name app-b --network lab-net busybox:1.36 sh
```

### Step 3: Test DNS discovery

``` bash
docker exec app-a nslookup app-b
docker exec app-a ping -c 3 app-b
```

The IP returned by DNS should correspond to `app-b`'s address on
`lab-net`. If a tool is missing from the image, use a diagnostic image
that includes it; do not assume all minimal images contain `ping`,
`curl`, or `nslookup`.

### Step 4: Inspect the network

``` bash
docker network inspect lab-net
```

You should see both containers in the network's container list.

### Step 5: Disconnect and reconnect a container

``` bash
docker network disconnect lab-net app-b
docker network inspect lab-net

docker network connect lab-net app-b
docker network inspect lab-net
```

After reconnecting, test name resolution and connectivity again.

### Step 6: Remove lab resources

``` bash
docker rm -f app-a app-b
docker network rm lab-net
```

**Expected lesson:** A user-defined bridge provides built-in DNS-based
discovery for containers on that network and lets you manage their
network membership explicitly.

## 8. Lab C --- Isolating application tiers

**Goal:** Demonstrate a simple reachability boundary between a frontend
and a database-like service.

> This lab demonstrates network attachment, not production database
> security. Use test data only.

### Design

-   `frontend-net`: frontend and API can communicate.
-   `data-net`: API and database can communicate.
-   The frontend is **not** attached to `data-net`.
-   The database has no published host port.

``` text
Client -> published frontend port -> frontend
                                     |
                                frontend-net
                                     |
                                    API
                                     |
                                  data-net
                                     |
                                  database
```

### Step 1: Create networks

``` bash
docker network create frontend-net
docker network create data-net
```

### Step 2: Start a frontend container

``` bash
docker run -d --name frontend \
  --network frontend-net \
  -p 127.0.0.1:8080:80 \
  nginx:alpine
```

Check locally on the Docker host:

``` bash
curl -I http://127.0.0.1:8080
```

If `curl` is not installed on the host, use a browser or another HTTP
client.

### Step 3: Start an API container on both networks

For a networking demonstration, BusyBox can be used as a placeholder; it
is not a running API service:

``` bash
docker run -dit --name api --network frontend-net busybox:1.36 sh
docker network connect data-net api
```

### Step 4: Start a database container only on the data network

For a real database lab, use the database image and provide credentials
through a secure mechanism. The following placeholder illustrates
network placement only:

``` bash
docker run -dit --name database --network data-net busybox:1.36 sh
```

This `database` container is **not** a database server. It is only a
test container used to illustrate network membership.

### Step 5: Inspect network membership

``` bash
docker network inspect frontend-net
docker network inspect data-net
```

Expected membership:

-   `frontend-net`: `frontend`, `api`
-   `data-net`: `api`, `database`

### Step 6: Verify reachability boundary

First, test name resolution from the API container:

``` bash
docker exec api nslookup database
```

Now test from the frontend:

``` bash
docker exec frontend sh
```

Inside the frontend shell, try `nslookup database` if the image contains
the utility, then exit:

``` sh
exit
```

The frontend should not be able to resolve the database by its
`data-net` name because it is not attached to that network. Actual
reachability also depends on network configuration and host firewall
rules. Avoid interpreting a failed DNS lookup alone as proof that every
possible route is blocked.

### Step 7: Cleanup

``` bash
docker rm -f frontend api database
docker network rm frontend-net data-net
```

### Production design notes

For an actual application:

-   Run a real API and database image with supported configuration.
-   Attach each service only to the networks it needs.
-   Publish only the intended entry point, commonly a reverse proxy or
    web frontend.
-   Do not publish database ports merely to enable communication between
    containers.
-   Use database users with least privilege, strong credentials, and TLS
    where appropriate.
-   Add health checks and application-level timeouts; network attachment
    alone does not guarantee service health.
-   Remember that containers attached to the same network are not
    automatically authenticated to one another.

## 9. Host networking

### Demonstration

On a supported Linux Docker Engine:

``` bash
docker run --rm --network host nginx
```

Nginx attempts to bind to the host's port 80. If another service already
uses that port, startup may fail.

Check listeners on Linux:

``` bash
sudo ss -lntp
```

Stop the test container with `Ctrl+C` if running interactively, or stop
the named container if you started it in detached mode.

### When might host networking be useful?

-   A workload needs to share host networking behavior for a specific
    reason.
-   The performance or packet-processing characteristics have been
    measured and justify the trade-off.
-   Port management and security implications are understood.

### Why not use it by default?

-   It reduces network namespace isolation.
-   Port collisions are more likely.
-   Port-publishing mappings do not work as they do in bridge mode.
-   Port exposure is tied more directly to host interfaces and host
    firewall configuration.

Prefer bridge networking unless you have a clear reason to choose host
mode.

## 10. Overlay networking

Overlay networks are for supported multi-host Docker setups, especially
Docker Swarm. They are useful when a service's tasks may run on
different swarm nodes but still need to communicate over a shared
logical network.

High-level Swarm workflow:

``` bash
# On a manager node, initialize a swarm
docker swarm init

# Create an overlay network
docker network create --driver overlay app-overlay

# Deploy a service connected to the overlay
docker service create \
  --name web-service \
  --network app-overlay \
  --replicas 2 \
  nginx:alpine

# Inspect the network and service
docker network ls
docker network inspect app-overlay
docker service ls
docker service ps web-service
```

For a real multi-node lab, join worker nodes using the join command
produced by `docker swarm init`, configure host/network firewall rules
required by Swarm, and validate node reachability. Do not expose swarm
management ports to untrusted networks.

To remove the demo service and network after confirming no service is
using it:

``` bash
docker service rm web-service
docker network rm app-overlay
```

If this was only a local practice environment and you no longer need the
swarm, consult Docker's instructions before leaving or removing the
swarm. Avoid running `docker swarm leave --force` on a production
manager.

**Kubernetes note:** Kubernetes networking is a separate model.
Kubernetes Pods generally communicate through the cluster network
implemented by the cluster's networking plugin; do not assume Docker's
`overlay` driver is the mechanism behind every Kubernetes cluster.

## 11. Port publishing and firewall considerations

### Publish a port on all host interfaces

``` bash
docker run -d --name web-public -p 8080:80 nginx:alpine
```

This commonly publishes host port 8080 on all host interfaces. Whether
it is reachable externally depends on routing, host firewall rules,
cloud security groups, and Docker's networking implementation.

### Publish only on loopback

``` bash
docker run -d --name web-local -p 127.0.0.1:8081:80 nginx:alpine
```

This is usually a safer default for local development when remote access
is not required.

### Confirm the mapping

``` bash
docker ps
docker port web-public
docker inspect web-public
```

### `EXPOSE` is not a firewall rule

A Dockerfile line such as:

``` dockerfile
EXPOSE 80
```

documents that the application is intended to listen on port 80 inside
the container. It does not publish that port on the host. Publishing is
normally requested with `-p` or `--publish` (or configured through a
service/orchestrator).

### Cloud VM reminder

If Docker runs on an AWS EC2 or another cloud VM, there may be multiple
layers to check:

1.  The process listens on the expected container interface and port.
2.  The container port is published as intended.
3.  The host firewall allows the traffic.
4.  The cloud security group/network firewall allows the traffic.
5.  Routing and DNS point to the correct host.

Do not open a database port to the public internet to fix a
container-to-container connectivity issue.

## 12. Troubleshooting checklist

### A. The container cannot reach another container

``` bash
docker ps
docker network ls
docker network inspect <NETWORK_NAME>
docker inspect <CONTAINER_NAME>
```

Check:

-   Are both containers attached to the same intended network?
-   Are you using a user-defined bridge for service-name discovery?
-   Is the destination application actually running and listening?
-   Are the service port and protocol correct?
-   Is the app listening on `127.0.0.1` inside its container rather than
    on an address reachable from other containers? For inter-container
    access, the service usually needs to listen on the container
    interface, often `0.0.0.0`.
-   Are custom firewall rules or network policies blocking traffic?

### B. Name lookup fails

``` bash
docker exec <SOURCE_CONTAINER> cat /etc/resolv.conf
docker network inspect <USER_DEFINED_NETWORK>
```

-   Confirm both containers share the user-defined network.
-   Use the correct container name or network alias.
-   Do not rely on dynamic container IPs.
-   Verify the diagnostic image has `nslookup` or another DNS tool
    installed.
-   If a container has multiple networks, check the name and alias on
    the network relevant to the source container.

### C. Host cannot access the published service

``` bash
docker ps
docker port <CONTAINER_NAME>
docker logs <CONTAINER_NAME>
```

On Linux:

``` bash
sudo ss -lntp
sudo firewall-cmd --list-all       # systems using firewalld
sudo ufw status                    # systems using UFW
```

Also check the cloud firewall/security group, if applicable. Use only
the firewall tool appropriate to the host distribution.

### D. Container exits immediately

``` bash
docker ps -a
docker logs <CONTAINER_NAME>
docker inspect <CONTAINER_NAME>
```

A network problem is not always the cause. The process may have exited
because of an invalid command, missing configuration, or application
error.

### E. Remove an unused network

``` bash
docker network ls
docker network inspect <NETWORK_NAME>
docker network rm <NETWORK_NAME>
```

A network cannot normally be removed while containers or services are
still using it. Disconnect or remove the relevant workloads first.
`docker network prune` removes unused networks, so inspect before
running it.

## 13. Security and production guidance

-   **Least connectivity:** attach a container only to networks it
    requires.
-   **Private data tier:** avoid publishing database and cache ports
    unless explicitly needed.
-   **Intentional publishing:** bind local-only development ports to
    `127.0.0.1`; publish to external interfaces only when required.
-   **Host networking:** treat it as a deliberate exception because it
    reduces network separation.
-   **Do not trust network membership alone:** authentication,
    authorization, TLS, and application-level controls still matter.
-   **Avoid hard-coded IPs:** use service discovery on user-defined
    networks or the orchestrator's supported service discovery.
-   **Use minimal diagnostic images carefully:** debug tools are useful,
    but do not leave unnecessary tools or privileged debug containers in
    production.
-   **Limit Docker daemon access:** users with Docker control can often
    gain host-level privileges; protect the socket and membership of the
    Docker group.
-   **Observe actual behavior:** test allowed and denied paths from the
    correct source container; inspect logs, listeners, routes, and
    firewall rules.
-   **Document the topology:** record network names, purpose, subnet
    choices, exposed ports, and which services attach to each network.

## 14. Quick command reference

  ----------------------------------------------------------------------------------------
  Task                                Command
  ----------------------------------- ----------------------------------------------------
  List networks                       `docker network ls`

  Inspect network                     `docker network inspect app-net`

  Create bridge                       `docker network create app-net`

  Run on a network                    `docker run --network app-net ...`

  Connect existing container          `docker network connect app-net container-name`

  Disconnect container                `docker network disconnect app-net container-name`

  Inspect container                   `docker inspect container-name`

  Publish host port                   `docker run -p 8080:80 ...`

  Publish on loopback                 `docker run -p 127.0.0.1:8080:80 ...`

  Show port mappings                  `docker port container-name`

  Remove network                      `docker network rm app-net`

  Remove unused networks              `docker network prune`
  ----------------------------------------------------------------------------------------

## 15. Interview questions and answers

### 1. What is Docker networking?

Docker networking connects containers to each other, the Docker host,
and external systems using network drivers and configuration. It also
helps define which workloads can directly communicate.

### 2. What is the default Docker bridge?

It is the default single-host bridge network, commonly backed by the
`docker0` Linux bridge. It allows containers to use bridge networking,
but user-defined bridges are generally preferable for new
multi-container applications because they support built-in name-based
discovery.

### 3. What is the difference between the default bridge and a user-defined bridge?

A user-defined bridge supports automatic DNS resolution for containers
by name or network alias and can be created for a specific application
group. The default bridge has more limited name-discovery behavior and
is less flexible for modern multi-container designs.

### 4. What does `-p 8080:80` mean?

It maps host port 8080 to port 80 inside the container. The exact
external reachability depends on the bind address, host firewall,
routing, and any cloud firewall rules.

### 5. Does `EXPOSE 80` make a container publicly accessible?

No. `EXPOSE` is image metadata. A host port must be published or
otherwise made reachable through an appropriate networking setup.

### 6. How do containers find one another without hard-coded IPs?

On a user-defined bridge, Docker provides name-based DNS discovery for
containers attached to that network. In orchestrated environments, use
the orchestrator's supported service-discovery mechanism.

### 7. What is host networking?

The container uses the host's network namespace on supported
environments, rather than an isolated bridge-network namespace. It can
simplify certain networking cases but reduces isolation and can cause
port conflicts.

### 8. What is an overlay network?

A logical network that can connect workloads across multiple Docker
hosts in supported cluster configurations, especially Docker Swarm.

### 9. Is Docker overlay networking the same as Kubernetes networking?

No. Kubernetes defines its own Pod networking model and normally uses a
cluster networking implementation/plugin. Docker overlay is a Docker
networking feature.

### 10. How would you isolate a database from a frontend?

Place the database on a private data network shared with the API, but do
not attach the frontend to that network. Do not publish the database
port unnecessarily, and enforce database authentication and
authorization as well.

### 11. A container can ping another container but the application request fails. Why?

ICMP reachability does not prove the application is listening or that
its TCP/UDP port is reachable. Check the process, listening address,
target port, protocol, logs, and firewall rules.

### 12. Why should you avoid hard-coding container IP addresses?

Container IP addresses may change when containers are recreated or
networks are changed. Use network DNS names or the service discovery
mechanism of the relevant orchestrator.

### 13. How do you inspect which containers belong to a network?

Run `docker network inspect <NETWORK_NAME>` and review its container
list and IP details.

### 14. Does putting containers on separate networks provide complete security?

No. It is one layer of isolation. Host-level access, published ports,
routing, daemon permissions, application vulnerabilities, and
credentials still matter.

### 15. What is the difference between `bridge`, `host`, and `overlay`?

-   `bridge`: generally for containers on one Docker host.
-   `host`: shares the host network namespace on supported environments.
-   `overlay`: enables networking across multiple Docker hosts in
    supported cluster setups.

## 16. Scope of this note

This README covers Docker's main networking concepts, local bridge labs,
network-based tier separation, host mode, and an introductory Swarm
overlay workflow.

Related topics intentionally left for their own notes:

-   Docker image building, Dockerfile layers, and multistage builds.
-   Container writable layers, volumes, and bind mounts.
-   Kubernetes Services, Ingress, NetworkPolicy, and CNI implementation
    details.
-   Advanced Linux routing, nftables/iptables internals, and production
    network design.

## 17. Official references

Prefer official documentation when behavior varies by Docker Engine
version or operating system.

-   [Docker networking
    overview](https://docs.docker.com/engine/network/)
-   [Bridge network
    driver](https://docs.docker.com/engine/network/drivers/bridge/)
-   [Host network
    driver](https://docs.docker.com/engine/network/drivers/host/)
-   [Overlay network
    driver](https://docs.docker.com/engine/network/drivers/overlay/)
-   [Port publishing and
    mapping](https://docs.docker.com/engine/network/port-publishing-and-mapping/)
-   [Docker CLI:
    `docker network`](https://docs.docker.com/reference/cli/docker/network/)
-   [Docker Swarm mode](https://docs.docker.com/engine/swarm/)

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
└── 06-docker-networking/
    └── README.md
```

From the root of your cloned repository:

``` bash
mkdir -p 06-docker-networking
# Copy this README.md into that directory, then:
git add 06-docker-networking/README.md
git commit -m "Add Docker networking notes and labs"
git push origin main
```
