# Docker Persistent Storage: Volumes and Bind Mounts

> **Video:** [Day-27 --- Docker Volumes and Bind Mounts \| Abhishek
> Veeramalla](https://www.youtube.com/watch?v=r_LgmqejAkA)\
> **Playlist:** [DevOps Zero to
> Hero](https://www.youtube.com/playlist?list=PLdpzxOOAlwvIc1TjTwopNSjRJkzES2ZXk)\
> **Suggested path:** `05-docker-storage/README.md`\
> **Prerequisites:** Basic Docker commands and the earlier [Docker
> fundamentals](../02-docker-fundamentals/README.md) notes.

This guide explains how to keep data beyond a container's lifecycle
using Docker volumes and bind mounts. It includes practical commands,
Nginx and file-persistence labs, inspection and cleanup,
troubleshooting, backup guidance, and production considerations. It
focuses on storage; container architecture and basic lifecycle commands
are covered in the earlier notes.

------------------------------------------------------------------------

## Table of contents

-   [1. Learning objectives](#1-learning-objectives)
-   [2. Why container storage needs
    planning](#2-why-container-storage-needs-planning)
-   [3. The container writable layer](#3-the-container-writable-layer)
-   [4. Storage options: writable layer, bind mount, and
    volume](#4-storage-options-writable-layer-bind-mount-and-volume)
-   [5. Bind mounts](#5-bind-mounts)
-   [6. Docker volumes](#6-docker-volumes)
-   [7. `--mount` versus `-v`](#7---mount-versus--v)
-   [8. Lab A: prove container data is
    ephemeral](#8-lab-a-prove-container-data-is-ephemeral)
-   [9. Lab B: use a bind mount](#9-lab-b-use-a-bind-mount)
-   [10. Lab C: use a named volume](#10-lab-c-use-a-named-volume)
-   [11. Lab D: persist Nginx website
    content](#11-lab-d-persist-nginx-website-content)
-   [12. Inspect, back up, and restore
    volumes](#12-inspect-back-up-and-restore-volumes)
-   [13. Volume lifecycle and cleanup](#13-volume-lifecycle-and-cleanup)
-   [14. Permissions and
    troubleshooting](#14-permissions-and-troubleshooting)
-   [15. Production considerations](#15-production-considerations)
-   [16. Practical exercises](#16-practical-exercises)
-   [17. Interview questions and
    answers](#17-interview-questions-and-answers)
-   [18. What belongs in later notes](#18-what-belongs-in-later-notes)
-   [19. References](#19-references)

------------------------------------------------------------------------

## 1. Learning objectives

After completing this guide, you should be able to:

1.  Explain why a container's writable layer is not a suitable place for
    important long-lived data.
2.  Compare bind mounts and named volumes.
3.  Create, list, inspect, and remove Docker volumes.
4.  Attach storage with `--mount` and understand the common `-v` syntax.
5.  Demonstrate that data can survive removal and recreation of a
    container.
6.  Troubleshoot mount paths, permissions, and file ownership.
7.  Back up and restore a volume using a temporary helper container.
8.  Recognize why persistence alone is not the same as backup,
    replication, or high availability.

## 2. Why container storage needs planning

Containers are designed to be replaceable. A deployment may stop and
remove a container during an update, recreate it after a failure, or
start another instance from the same image.

Application data may include:

-   User-uploaded documents and images
-   Database files
-   Application-generated reports
-   Configuration that is intentionally managed outside the image
-   Logs, when a workload explicitly writes logs to files
-   Cache data, depending on whether it is safe to regenerate

If important data is written only to a container's writable layer,
removing the container removes that layer. A new container created from
the same image starts with a fresh writable layer.

### Core principle

> Treat containers as replaceable; store important persistent data in a
> storage location with a deliberate lifecycle.

Docker offers several storage mechanisms. This note focuses on bind
mounts and volumes, the two common options for keeping files outside the
container's writable layer.

## 3. The container writable layer

When Docker creates a container from an image, it adds a writable layer
above the image's read-only layers.

``` text
Container
├── Writable container layer
│   └── Changes made by the running container
└── Image layers (read-only)
    ├── Application files
    ├── Runtime
    └── Base image content
```

The writable layer is useful for temporary runtime changes. It is not a
durable storage contract: its data is tied to that particular container
instance.

A replacement container gets a new writable layer even when it uses the
same image tag. Image layers and persistent mounts have separate
lifecycles.

### Important distinction: stop vs remove

-   `docker stop` stops the container but retains the container and its
    writable layer.
-   `docker start` can restart that same container, retaining its
    writable-layer changes.
-   `docker rm` removes the container and its writable layer.
-   A named volume is a separate Docker-managed object and normally
    remains after its container is removed.
-   A bind mount points to a host path; its data is managed on the host.

`docker rm -v` does not remove every named volume. It removes anonymous
volumes associated with the container under the documented conditions.
Check which storage objects you are using before cleanup.

## 4. Storage options: writable layer, bind mount, and volume

  --------------------------------------------------------------------------
  Feature           Container writable   Bind mount        Named volume
                    layer                                  
  ----------------- -------------------- ----------------- -----------------
  Storage location  Container-specific   Explicit host     Docker-managed
                    writable layer       path              storage location

  Survives          No                   Yes, host files   Yes, volume
  container removal                      remain            normally remains

  Host path control Managed by Docker's  User selects the  Docker
                    container storage    path              selects/manages
                                                           the mountpoint

  Portability       Low for persistent   Depends on host   Usually easier to
                    data                 path and files    attach to
                                                           replacement
                                                           containers on the
                                                           same Docker host

  Host file access  Not directly         Directly visible  Possible, but not
                    intended as          at the chosen     typically managed
                    persistent host      path              by editing
                    storage                                Docker's internal
                                                           path directly

  Common use        Temporary runtime    Source code,      Application data
                    changes              host-managed      that needs
                                         configuration,    Docker-managed
                                         specific host     persistence
                                         directories       

  Backup            Usually not          Back up the host  Back up the
                    appropriate for      path              volume data with
                    durable data                           a deliberate
                                                           method
  --------------------------------------------------------------------------

Docker also supports `tmpfs` mounts for temporary in-memory data on
supported Linux setups. They are useful for sensitive or ephemeral files
but are not persistent across container or host restarts.

## 5. Bind mounts

A bind mount maps a specific path on the Docker host into a path inside
the container.

Example:

``` bash
mkdir -p "$HOME/docker-labs/site"

echo "Hello from the host" > "$HOME/docker-labs/site/index.html"

docker run --name bind-nginx \
  --mount type=bind,source="$HOME/docker-labs/site",target=/usr/share/nginx/html,readonly \
  -p 8080:80 \
  -d nginx:alpine
```

Open `http://localhost:8080/` on the Docker host. The Nginx container
serves the file from the host directory.

### How bind mounts behave

-   The host path must exist or be handled according to the selected
    mount syntax and Docker environment.
-   Changes to files in the mounted host directory are visible to the
    container, subject to filesystem and caching behavior.
-   Writes by the container may change host files if the mount is
    read-write.
-   The mounted directory obscures the image's existing files at the
    target path while the mount is active.
-   The path is host-specific; a deployment on another machine must have
    an appropriate path and content.

### Read-only bind mounts

Use `readonly` or `ro` for data the container should not modify:

``` bash
docker run --rm \
  --mount type=bind,source="$HOME/docker-labs/site",target=/site,readonly \
  alpine:3.21 \
  sh -c 'cat /site/index.html'
```

The container can read the file but cannot write to that mount. This
does not make the rest of the container filesystem read-only.

### When bind mounts are useful

-   Local development where source changes should appear immediately.
-   Mounting host-managed configuration.
-   Sharing specific host files or directories with a container.
-   Workflows that deliberately require direct host-path access.

### Bind mount risks

-   Accidentally mounting a sensitive host directory.
-   Allowing a container to overwrite host files.
-   Differences between host operating systems and paths.
-   Permission and ownership mismatches.
-   A mount hiding application files that were present in the image.

Mount only the minimum required path and use read-only mode where
practical.

## 6. Docker volumes

A Docker volume is a storage object managed by Docker. Docker maintains
its lifecycle independently of an individual container, making named
volumes a common choice for persistent application data.

### Create and list a volume

``` bash
docker volume create app-data
docker volume ls
docker volume inspect app-data
```

A named volume such as `app-data` can be attached to different
containers on the same Docker host.

### Mount the volume in a container

``` bash
docker run --name volume-writer \
  --mount type=volume,source=app-data,target=/data \
  alpine:3.21 \
  sh -c 'echo "Persistent Docker volume data" > /data/message.txt'
```

The container writes a file under `/data`, which is the volume
mountpoint from the container's perspective. The one-shot process exits,
but the named volume remains.

Read the file from a new container:

``` bash
docker run --rm \
  --mount type=volume,source=app-data,target=/data,readonly \
  alpine:3.21 \
  cat /data/message.txt
```

The output should be:

``` text
Persistent Docker volume data
```

Remove the original container:

``` bash
docker rm volume-writer
```

Then read the file again with the previous `docker run` command. The
volume persists independently of the removed container.

### Why named volumes are often recommended

-   Docker manages the volume object.
-   The same volume can be attached to a replacement container.
-   The volume lifecycle is separate from the container lifecycle.
-   Volume drivers can support different storage backends.
-   They can be backed up and restored with appropriate procedures.

**A volume is not automatically a backup.** It can still be deleted,
corrupted, filled, or lost with the underlying host/storage system.
Production data requires a recovery and backup plan.

## 7. `--mount` versus `-v`

Both forms can attach storage, but `--mount` is often clearer because it
explicitly names each field.

### Volume syntax with `--mount`

``` bash
docker run --rm \
  --mount type=volume,source=app-data,target=/data \
  alpine:3.21 ls -la /data
```

### Volume syntax with `-v`

``` bash
docker run --rm \
  -v app-data:/data \
  alpine:3.21 ls -la /data
```

The short form is:

``` text
-v SOURCE:TARGET[:OPTIONS]
```

For a named volume, `SOURCE` is the volume name. For a bind mount,
`SOURCE` is a host path.

### Bind mount with `--mount`

``` bash
docker run --rm \
  --mount type=bind,source="$HOME/docker-labs/site",target=/site,readonly \
  alpine:3.21 ls -la /site
```

### Bind mount with `-v`

``` bash
docker run --rm \
  -v "$HOME/docker-labs/site:/site:ro" \
  alpine:3.21 ls -la /site
```

### A useful behavior difference

With `--mount type=bind`, Docker normally reports an error if the source
path does not exist. The short `-v` bind-mount form can create a missing
source path as a directory, which may hide a typo. Prefer the explicit
`--mount` form when clarity and validation matter.

Options and behavior can vary by Docker environment, so check the
official documentation for your version.

## 8. Lab A: prove container data is ephemeral

This lab demonstrates the writable-layer lifecycle.

### Step 1 --- Create a container that writes data

``` bash
docker run --name ephemeral-demo alpine:3.21 \
  sh -c 'echo "Only in this container layer" > /tmp/demo.txt'
```

### Step 2 --- Read the file from the same container

The process has exited, but the container still exists:

``` bash
docker start -ai ephemeral-demo
```

For a one-shot command, `docker start -ai` reruns the container's
configured command, which in this example overwrites the same file. To
inspect without rerunning the original command, use a running container
or a separate debug pattern. A simpler direct inspection of the stopped
container's filesystem is not available via ordinary `docker exec`,
because `exec` requires a running container.

Use this alternative for an easy repeatable demonstration:

``` bash
docker run -d --name ephemeral-shell alpine:3.21 \
  sh -c 'echo "Only in this container layer" > /tmp/demo.txt; sleep 600'
docker exec ephemeral-shell cat /tmp/demo.txt
```

### Step 3 --- Remove the container

``` bash
docker rm -f ephemeral-shell
```

### Step 4 --- Create a new container from the same image

``` bash
docker run --rm alpine:3.21 cat /tmp/demo.txt
```

The file is not present because it existed only in the removed
container's writable layer. The command exits with an error; this is the
expected result for the demonstration.

## 9. Lab B: use a bind mount

### Step 1 --- Create host data

``` bash
mkdir -p "$HOME/docker-labs/bind-data"
echo "Created on the Docker host" > "$HOME/docker-labs/bind-data/message.txt"
```

### Step 2 --- Read the host file from a container

``` bash
docker run --rm \
  --mount type=bind,source="$HOME/docker-labs/bind-data",target=/data,readonly \
  alpine:3.21 cat /data/message.txt
```

### Step 3 --- Change the host file

``` bash
echo "Updated on the host" >> "$HOME/docker-labs/bind-data/message.txt"
```

Run the read command again and confirm the change is visible.

### Step 4 --- Verify the data survives container removal

Run a temporary container with the bind mount, remove it, then read the
file from a new container. The host file remains because it is not
stored in the container's writable layer.

### Lab observation

A bind mount persists because the underlying data is in the host
directory. Removing a container does not remove that directory.

## 10. Lab C: use a named volume

### Step 1 --- Create a volume

``` bash
docker volume create training-data
docker volume ls
docker volume inspect training-data
```

### Step 2 --- Write data into it

``` bash
docker run --name volume-writer \
  --mount type=volume,source=training-data,target=/data \
  alpine:3.21 \
  sh -c 'date -u > /data/created-at.txt; echo "volume data" > /data/hello.txt'
```

### Step 3 --- Read it from a different container

``` bash
docker run --rm \
  --mount type=volume,source=training-data,target=/data,readonly \
  alpine:3.21 cat /data/hello.txt
```

### Step 4 --- Remove the original container

``` bash
docker rm volume-writer
```

### Step 5 --- Confirm persistence

``` bash
docker run --rm \
  --mount type=volume,source=training-data,target=/data,readonly \
  alpine:3.21 ls -l /data
```

The volume remains because its lifecycle is separate from the original
container.

## 11. Lab D: persist Nginx website content

This example shows how a volume can hold files served by Nginx.

### Step 1 --- Create a named volume

``` bash
docker volume create nginx-site
```

### Step 2 --- Populate it

The official Nginx image serves content from `/usr/share/nginx/html`. A
temporary helper container can create a file in the volume:

``` bash
docker run --rm \
  --mount type=volume,source=nginx-site,target=/site \
  alpine:3.21 \
  sh -c 'echo "<h1>Persistent Nginx content</h1>" > /site/index.html'
```

### Step 3 --- Run Nginx with the volume

``` bash
docker run -d --name nginx-persistent \
  --mount type=volume,source=nginx-site,target=/usr/share/nginx/html,readonly \
  -p 8080:80 \
  nginx:alpine
```

Open `http://localhost:8080/`, or test from the Docker host:

``` bash
curl http://localhost:8080/
```

### Step 4 --- Replace the container

``` bash
docker rm -f nginx-persistent

docker run -d --name nginx-persistent-2 \
  --mount type=volume,source=nginx-site,target=/usr/share/nginx/html,readonly \
  -p 8080:80 \
  nginx:alpine
```

The same website content is served by the replacement container because
the named volume remains.

### Important note about volume initialization

When an empty volume is mounted over a non-empty image directory, Docker
may initialize the volume with the directory's existing contents unless
copy behavior is disabled. This is useful in some cases but can surprise
users. The lab explicitly populates the volume first, so the source of
the website content is clear.

## 12. Inspect, back up, and restore volumes

### Inspect volume metadata

``` bash
docker volume inspect training-data
```

The result includes metadata such as the volume name, driver, and
mountpoint. The mountpoint is host-side implementation detail; avoid
editing Docker-managed storage directly unless you understand the
implications.

### Backup a named volume

For a simple local volume using Docker's default local driver, a
temporary helper container can archive the volume contents. The backup
destination below is a host bind mount.

``` bash
mkdir -p "$HOME/docker-backups"

docker run --rm \
  --mount type=volume,source=training-data,target=/source,readonly \
  --mount type=bind,source="$HOME/docker-backups",target=/backup \
  alpine:3.21 \
  tar -czf /backup/training-data.tar.gz -C /source .
```

Verify the archive exists:

``` bash
ls -lh "$HOME/docker-backups/training-data.tar.gz"
```

This example assumes the helper image contains `tar` and the host backup
directory is writable. For databases, a filesystem archive alone may not
produce an application-consistent backup while the database is changing.
Use the database's native backup procedure or stop/quiesce writes as
appropriate.

### Restore into a new volume

Create a new volume:

``` bash
docker volume create training-data-restored
```

Extract the archive into it:

``` bash
docker run --rm \
  --mount type=volume,source=training-data-restored,target=/target \
  --mount type=bind,source="$HOME/docker-backups",target=/backup,readonly \
  alpine:3.21 \
  tar -xzf /backup/training-data.tar.gz -C /target
```

Verify the restored content:

``` bash
docker run --rm \
  --mount type=volume,source=training-data-restored,target=/data,readonly \
  alpine:3.21 ls -la /data
```

### Backup best practices

-   Store backups outside the only host/storage failure domain.
-   Encrypt sensitive backups and restrict access.
-   Use a consistent backup method for databases and stateful
    applications.
-   Test restoration regularly.
-   Document retention and recovery-time/recovery-point expectations.
-   Do not assume that creating a volume creates a backup automatically.

## 13. Volume lifecycle and cleanup

### List and inspect

``` bash
docker volume ls
docker volume inspect app-data
```

### Remove a volume

A volume generally cannot be removed while a container references it.

``` bash
docker ps -a
docker rm -f volume-writer
docker volume rm app-data
```

Only remove `app-data` if you are certain its contents are no longer
needed. Volume removal is destructive.

### Remove unused volumes

``` bash
docker volume prune
```

This removes unused local volumes according to Docker's command
behavior. Review what is unused before running cleanup, especially on
shared or production hosts. Do not assume an unused volume contains no
valuable data.

### Cleanup checklist

-   [ ] Identify containers using the volume.
-   [ ] Confirm the volume's purpose and contents.
-   [ ] Create and verify a backup if the data matters.
-   [ ] Stop or remove referencing containers as appropriate.
-   [ ] Remove only the intended volume.
-   [ ] Verify the result with `docker volume ls`.

## 14. Permissions and troubleshooting

  -------------------------------------------------------------------------
  Symptom                 Likely cause            First checks
  ----------------------- ----------------------- -------------------------
  Container cannot write  Host directory          Check host ownership,
  to a bind mount         permissions, UID/GID    mount options, container
                          mismatch, read-only     user and logs.
                          mount                   

  Empty directory appears Wrong host source path  Inspect the exact path
  in container            or mount target         and use `--mount` for
                                                  clearer errors.

  Image content           Mount obscures existing Verify target path and
  disappears under mount  files at the target     whether a mount should
                                                  cover it.

  Volume removal fails    A container still       Check `docker ps -a` and
                          references it           inspect container mounts.

  Data disappears after   Data was stored in      Inspect `docker inspect`
  replacing container     writable layer, not a   and confirm the
                          mount                   volume/bind source and
                                                  target.

  Permission denied       Filesystem ownership or Inspect file permissions;
  writing volume          application UID         use least-privilege
                          mismatch                ownership and avoid broad
                                                  permissions.

  Nginx serves default    Wrong mount target or   Check
  page rather than custom volume contents         `/usr/share/nginx/html`
  page                                            mount and the volume's
                                                  `index.html`.

  Backup archive is empty Wrong source volume or  Inspect the volume
                          incorrect archive path  contents and verify the
                                                  archive before deleting
                                                  data.

  SELinux blocks a bind   Host security           Review SELinux labels and
  mount                   labeling/access policy  Docker documentation for
                                                  the host distribution; do
                                                  not disable SELinux as a
                                                  first step.

  Database data is        Files copied while      Use database-native
  inconsistent after      database was writing    backup or a consistent
  backup                                          snapshot procedure.
  -------------------------------------------------------------------------

### Useful diagnostic commands

``` bash
docker inspect CONTAINER_NAME
docker volume inspect VOLUME_NAME
docker ps -a
docker logs CONTAINER_NAME
docker exec -it CONTAINER_NAME sh
```

The `docker exec ... sh` example works only if the image contains a
shell and the container is running. Minimal images may not include one.

### Permissions guidance

Avoid solving mount permission issues with `chmod -R 777`. Instead,
identify which user the application runs as and grant the minimum
required read/write access. On SELinux-enabled hosts, filesystem labels
may also affect bind-mount access.

## 15. Production considerations

### Choose storage based on data ownership

-   Use a **named volume** when Docker-managed persistence is
    appropriate.
-   Use a **bind mount** when a specific host path must be shared or
    managed directly.
-   Use **external object storage or a database service** when the
    application architecture requires shared access, independent
    scaling, replication, or managed durability.
-   Use **tmpfs** for suitable temporary data that should not persist to
    disk.

### Stateful services

A named volume helps data survive container replacement, but it does not
automatically provide:

-   Replication across hosts
-   Database consistency
-   Backups
-   Disaster recovery
-   Encryption at rest
-   High availability
-   Safe concurrent access by multiple writers

The correct storage architecture depends on the application's
consistency requirements, workload, and failure model.

### Operational checklist

-   [ ] Identify which directories contain durable state.
-   [ ] Mount durable state explicitly.
-   [ ] Use read-only mounts when writes are unnecessary.
-   [ ] Plan ownership and permissions.
-   [ ] Monitor free disk space and volume growth.
-   [ ] Back up important data and test restoration.
-   [ ] Protect backups with access controls and encryption where
    needed.
-   [ ] Understand the volume driver's behavior and failure domain.
-   [ ] Avoid manually modifying Docker's internal volume directories.
-   [ ] Document cleanup procedures to avoid accidental data loss.

## 16. Practical exercises

### Exercise A --- Ephemeral versus persistent data

-   [ ] Write a file inside a container's writable layer.
-   [ ] Remove the container.
-   [ ] Create a new container and confirm the file is missing.
-   [ ] Repeat using a named volume and confirm the file remains.

### Exercise B --- Bind mount

-   [ ] Create a host directory and a text file.
-   [ ] Mount it read-only into Alpine.
-   [ ] Read the file inside the container.
-   [ ] Change the file on the host and confirm the update.
-   [ ] Explain the security advantage of a read-only mount.

### Exercise C --- Nginx persistence

-   [ ] Create a named volume.
-   [ ] Populate it with an `index.html` file.
-   [ ] Mount it into Nginx.
-   [ ] Verify it through `curl`.
-   [ ] Remove and recreate the Nginx container using the same volume.
-   [ ] Confirm the page still exists.

### Exercise D --- Backup and restore

-   [ ] Archive a named volume to the host.
-   [ ] Verify the archive file.
-   [ ] Restore it into a new volume.
-   [ ] Compare the original and restored contents.
-   [ ] Explain why a live database may require an
    application-consistent backup.

### Exercise E --- Cleanup and reflection

-   [ ] Inspect a volume.
-   [ ] Identify containers referencing it.
-   [ ] Back up any important data.
-   [ ] Remove the intended lab container and volume.
-   [ ] Explain why `docker volume prune` must be used carefully.

## 17. Interview questions and answers

**1. Why is a container's writable layer not suitable for important
persistent data?**\
It belongs to the container instance and is removed when the container
is removed. A replacement container gets a new writable layer.

**2. What is a Docker bind mount?**\
A mapping from a specific host path into a container path.

**3. What is a Docker volume?**\
A storage object managed by Docker and maintained independently of a
particular container.

**4. What is the difference between a bind mount and a named volume?**\
A bind mount uses a host-selected path; a named volume uses a
Docker-managed volume object and lifecycle.

**5. Which is generally preferred for Docker-managed persistent
application data?**\
A named volume is often the natural choice, unless the application
requires a specific host path or external storage architecture.

**6. What does `docker volume create app-data` do?**\
It creates a named volume called `app-data`.

**7. What does `docker volume inspect` show?**\
Volume metadata, including the driver and mountpoint information.

**8. What is the difference between `--mount` and `-v`?**\
Both configure mounts. `--mount` uses explicit key-value fields and is
often easier to read; `-v` is a compact syntax.

**9. Does `docker stop` delete container data?**\
No. It stops the same container while retaining its writable layer.
Removing the container is different.

**10. Does a named volume automatically disappear when its container is
removed?**\
Normally no. Named volumes persist independently and can be attached to
another container.

**11. Does a volume automatically provide a backup?**\
No. Backups and restoration must be designed and tested separately.

**12. Why might a bind mount be empty inside the container?**\
The wrong host source path may have been selected, or the mount may be
obscuring the image's original files.

**13. Why use a read-only mount?**\
It prevents the container from modifying that mounted data, reducing
accidental or malicious changes.

**14. What does `docker volume prune` do?**\
It removes unused local volumes according to Docker's pruning behavior.
Review impact before running it.

**15. Why can Docker fail to remove a volume?**\
A container may still reference the volume. Inspect containers and their
mounts first.

**16. Why should `chmod -R 777` be avoided?**\
It grants broad permissions and can expose data or permit unwanted
modifications instead of fixing the actual ownership issue.

**17. Are bind mounts portable between hosts?**\
Not automatically. The host path and its contents must exist and be
appropriate on the target host.

**18. Is a named volume shared across all Docker hosts automatically?**\
No. The default local volume is local to the Docker host. Multi-host
storage requires an appropriate driver or external storage system.

**19. Is a Docker volume enough for database high availability?**\
No. It provides storage, not replication, failover, consistent backups,
or a complete high-availability design.

**20. When might `tmpfs` be appropriate?**\
For temporary data on supported Linux systems that should not be
persisted to the host's ordinary storage.

## 18. What belongs in later notes

Keep the next subjects separate:

  ------------------------------------------------------------------------
  Future note                          Focus
  ------------------------------------ -----------------------------------
  `06-docker-networking/README.md`     Bridge networks, port publishing,
                                       DNS, container-to-container
                                       communication

  `07-docker-compose/README.md`        Multi-container applications and
                                       service configuration

  `08-container-security/README.md`    Mount security, non-root users,
                                       secrets, SELinux/AppArmor and
                                       runtime controls

  `09-stateful-containers/README.md`   Database containers, consistency,
                                       backup/restore, external storage
                                       and recovery
  ------------------------------------------------------------------------

Refer back to this storage note when later tutorials need persistent
database or application files instead of repeating the full explanation
of volumes and bind mounts.

## 19. References

### Video and playlist

-   [Abhishek Veeramalla --- Docker Volumes and Bind
    Mounts](https://www.youtube.com/watch?v=r_LgmqejAkA)
-   [DevOps Zero to Hero
    playlist](https://www.youtube.com/playlist?list=PLdpzxOOAlwvIc1TjTwopNSjRJkzES2ZXk)
-   [Previous note: Docker
    fundamentals](../02-docker-fundamentals/README.md)

### Official documentation

-   [Docker storage overview](https://docs.docker.com/engine/storage/)
-   [Docker volumes](https://docs.docker.com/engine/storage/volumes/)
-   [Docker bind
    mounts](https://docs.docker.com/engine/storage/bind-mounts/)
-   [Docker tmpfs mounts](https://docs.docker.com/engine/storage/tmpfs/)
-   [Docker volume CLI
    reference](https://docs.docker.com/reference/cli/docker/volume/)
-   [Docker run
    reference](https://docs.docker.com/reference/cli/docker/container/run/)
-   [Docker backup, restore, or migrate data
    volumes](https://docs.docker.com/engine/storage/volumes/#back-up-restore-or-migrate-data-volumes)

------------------------------------------------------------------------

## Attribution and update note

These are original study notes based on the video's subject and
supplementary official documentation, not a verbatim transcript. Storage
behavior and CLI options can vary by Docker version, host operating
system, and volume driver. Verify the official documentation and test
backup/restore procedures before relying on them for production data.

**Suggested commit message:**
`docs: add Docker volumes and bind mounts lab`
