# Stateful Containers: Databases, Persistence, Backup, and Recovery

> **Topic:** Database containers, persistent storage, backup
> consistency, restore validation, external storage, and recovery
> planning\
> **Suggested repository path:** `09-stateful-containers/README.md`

A stateful container runs an application that keeps important data
beyond the lifetime of an individual container instance. Databases are
the most common example. Containers can be replaced or recreated during
upgrades, so durable data must live in storage whose lifecycle is
managed separately from the container.

This note focuses on the operational side of stateful workloads:
choosing storage, preserving database data, taking consistent backups,
restoring safely, and planning for failures. It builds on the Docker
storage, networking, Compose, and container security notes in this
repository.

## Table of contents

-   [1. Learning objectives](#1-learning-objectives)
-   [2. Stateless vs. stateful
    workloads](#2-stateless-vs-stateful-workloads)
-   [3. Where container data lives](#3-where-container-data-lives)
-   [4. Run PostgreSQL with a named
    volume](#4-run-postgresql-with-a-named-volume)
-   [5. Initialization and lifecycle
    behavior](#5-initialization-and-lifecycle-behavior)
-   [6. Backup strategies and
    consistency](#6-backup-strategies-and-consistency)
-   [7. Practical lab: logical backup and
    restore](#7-practical-lab-logical-backup-and-restore)
-   [8. Physical backups and storage
    snapshots](#8-physical-backups-and-storage-snapshots)
-   [9. External storage and database
    services](#9-external-storage-and-database-services)
-   [10. Database upgrades and
    migrations](#10-database-upgrades-and-migrations)
-   [11. Recovery planning and disaster
    recovery](#11-recovery-planning-and-disaster-recovery)
-   [12. Monitoring storage and database
    health](#12-monitoring-storage-and-database-health)
-   [13. Troubleshooting](#13-troubleshooting)
-   [14. Production checklist](#14-production-checklist)
-   [15. Interview questions and
    answers](#15-interview-questions-and-answers)
-   [16. Scope boundaries](#16-scope-boundaries)
-   [17. Official references](#17-official-references)

## 1. Learning objectives

After completing this note, you should be able to:

-   Explain why a container's writable layer is not suitable for
    important long-term data.
-   Choose between named volumes, bind mounts, external storage, and
    managed database services.
-   Run a database container with persistent storage and safe network
    exposure.
-   Understand database initialization behavior when a volume already
    contains data.
-   Take and validate a logical backup.
-   Restore a backup into a separate database and verify its contents.
-   Distinguish logical backups, physical backups, and storage
    snapshots.
-   Plan upgrades, recovery targets, monitoring, and disaster recovery.

## 2. Stateless vs. stateful workloads

### Stateless workload

A stateless service does not rely on local container state to preserve
important business data. If its container is replaced, it can start
again from the image and external configuration.

Examples include:

-   A frontend web server serving packaged static assets.
-   An API container whose important data is stored in a database.
-   A worker that can safely retry jobs stored in an external queue.

### Stateful workload

A stateful service stores information that must survive restarts,
container replacement, host maintenance, or deployment changes.

Examples include:

-   PostgreSQL or MySQL database files.
-   A persistent message broker queue.
-   Application uploads or other durable files.
-   Search indexes, depending on the application's recovery strategy.

### Core rule

**Container lifecycle and data lifecycle must be managed separately.**
Recreating a database container should not mean accidentally recreating
or deleting its data.

``` text
                 container lifecycle
          create -> run -> stop -> replace
                               |
                               v
                      database container
                               |
                         mounted storage
                               |
                               v
                    persistent database data
                               |
                    backup / replication / restore
```

A persistent volume protects data from ordinary container removal, but
it does not protect against volume deletion, disk failure, corruption,
ransomware, operator mistakes, or loss of the entire host. Backups and
recovery procedures remain necessary.

## 3. Where container data lives

  -----------------------------------------------------------------------
  Storage option          Typical use             Important
                                                  considerations
  ----------------------- ----------------------- -----------------------
  Container writable      Temporary runtime       Tied to the container
  layer                   changes                 lifecycle; not a
                                                  durable-data strategy.

  Named Docker volume     Database files and      Managed by Docker; must
                          persistent application  be backed up and
                          data                    monitored.

  Bind mount              Host-managed files,     Host path, permissions,
                          configuration, or data  SELinux labels, and
                          paths                   portability need
                                                  attention.

  External block storage  Durable disks attached  Requires
                          to a host or cluster    provider-specific
                                                  attachment, filesystem,
                                                  availability, and
                                                  recovery planning.

  Network file storage    Shared files or         Performance, locking,
                          supported workloads     consistency, and
                                                  database support must
                                                  be verified.

  Managed database        Production database     Reduces operational
  service                 with provider-operated  burden but still
                          infrastructure          requires access
                                                  control, backup
                                                  validation, and
                                                  recovery planning.
  -----------------------------------------------------------------------

### Named volume example

``` yaml
services:
  db:
    image: postgres:16
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

The named volume is managed separately from the database container.
Compose commonly prefixes its name with the project name. Do not assume
the actual volume name without checking it.

### Inspect volumes

``` bash
docker volume ls
docker volume inspect <VOLUME_NAME>
docker inspect <CONTAINER_NAME>
```

Avoid editing database files directly inside a live data directory.
Database engines manage their own file formats, write-ahead logs, locks,
and consistency rules.

## 4. Run PostgreSQL with a named volume

This lab creates a local PostgreSQL instance whose data persists when
the container is recreated.

> **Use a lab password only.** Do not reuse a production credential.

### Step 1: Create a project

``` bash
mkdir stateful-postgres-lab
cd stateful-postgres-lab
```

Create `.env`:

``` dotenv
POSTGRES_PASSWORD=replace-with-a-strong-lab-password
```

Add `.env` to `.gitignore`:

``` gitignore
.env
```

Do not commit real credentials. A `.env` file is plain text
configuration, not an encrypted secret store.

### Step 2: Create `compose.yaml`

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
    # No host port is published; access is from this Compose project.
    networks:
      - backend

networks:
  backend:

volumes:
  postgres_data:
```

For production, choose a currently supported database image version and
follow a tested patch/upgrade policy. This example intentionally does
not publish PostgreSQL's port to the host.

### Step 3: Start and inspect

``` bash
docker compose config
docker compose up -d
docker compose ps
docker compose logs db
docker compose exec db pg_isready -U appuser -d appdb
```

### Step 4: Create test data

``` bash
docker compose exec db psql -U appuser -d appdb
```

At the `psql` prompt:

``` sql
CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

INSERT INTO customers (name) VALUES ('Asha'), ('Ravi');

SELECT * FROM customers;
\q
```

If you run the `INSERT` statement repeatedly, it will insert duplicate
rows. That is acceptable for a simple lab, but production scripts should
use controlled migrations or idempotent data-loading logic.

### Step 5: Recreate the container

``` bash
docker compose down
docker compose up -d
docker compose exec db psql -U appuser -d appdb -c 'SELECT * FROM customers;'
```

The records should remain because the named volume persists.

### Step 6: Inspect the volume

``` bash
docker volume ls
docker compose config
```

Find the actual volume name and inspect it:

``` bash
docker volume inspect <ACTUAL_VOLUME_NAME>
```

### Important warning

This command removes project-declared named volumes and can permanently
delete the database data:

``` bash
docker compose down --volumes
```

Use it only when intentionally resetting a disposable lab. Never use
volume deletion as a routine troubleshooting step.

## 5. Initialization and lifecycle behavior

Official database images commonly use environment variables and
initialization scripts only when the database data directory is empty
and the database is initialized for the first time.

For example, changing `POSTGRES_PASSWORD` in `.env` after PostgreSQL has
already initialized its persistent volume does **not** automatically
change the password stored inside that database.

Similarly, changing initialization SQL scripts does not necessarily
rerun them against an existing database.

### Safe operational principles

-   Treat persistent database data as authoritative.
-   Change database users and passwords through database administration
    commands or approved migration procedures.
-   Back up before risky changes.
-   Test initialization changes using a new disposable volume or a
    separate test environment.
-   Do not remove a production volume to force initialization variables
    to run again.
-   Keep the database version and data-directory compatibility
    requirements in mind when changing image tags.

## 6. Backup strategies and consistency

A backup is useful only if it can be restored to a valid state within
the required time.

### Logical backup

A logical backup exports database objects and data as SQL or a
database-specific logical archive.

Examples:

-   PostgreSQL: `pg_dump`, `pg_dumpall`.
-   MySQL: `mysqldump`, MySQL Shell utilities.

Advantages:

-   Portable across many environments.
-   Useful for selective restore and migration.
-   Can be inspected or processed using database tools.

Trade-offs:

-   Large databases can take longer to dump and restore.
-   Roles, global objects, extensions, permissions, and database-level
    settings may need separate handling.
-   Backup and restore tool versions should be compatible with the
    database version and format.

### Physical backup

A physical backup captures database storage files in a
database-supported manner. For PostgreSQL, this can include base backups
and WAL archiving; MySQL has its own physical backup approaches.

Advantages:

-   Can be more efficient for large databases.
-   May support point-in-time recovery when combined with logs and
    correct procedures.

Trade-offs:

-   Often more dependent on database version, filesystem layout, and
    recovery procedure.
-   Copying a live data directory with ordinary file-copy commands is
    generally not a safe substitute for a database-supported backup.

### Storage snapshot

A storage snapshot captures a block-storage or filesystem state at a
point in time, depending on the platform. A snapshot is not
automatically application-consistent. For database recovery, use a
documented process that coordinates the database, filesystem, and
storage platform as required.

### Consistency matters

A database may be actively changing during a backup. Use
database-supported backup tools or a properly coordinated snapshot
method. For multi-volume databases or applications that update related
data in different systems, define how consistency is achieved.

### The 3-2-1 principle

A common backup guideline is:

-   Keep at least **3** copies of important data.
-   Use **2** different storage types or failure domains.
-   Keep **1** copy offsite or otherwise isolated from the primary
    environment.

Adapt this to organizational requirements. Immutability, access
isolation, encryption, and restore testing are important additional
controls.

## 7. Practical lab: logical backup and restore

This lab uses PostgreSQL's logical custom-format backup. It restores
into a **separate database** so that the original database remains
intact.

### Step 1: Ensure the database and test data exist

From the project directory:

``` bash
docker compose up -d
docker compose exec db psql -U appuser -d appdb -c 'SELECT * FROM customers;'
```

If you have not completed the earlier lab, create a sample table and
insert test records first.

### Step 2: Create a backup directory

``` bash
mkdir -p backups
```

Create a custom-format backup using `pg_dump` inside the database
container and redirect the output to the host:

``` bash
docker compose exec -T db pg_dump -U appuser -d appdb -Fc > backups/appdb.dump
```

Why `-T`? It disables pseudo-TTY allocation, which is appropriate when
redirecting binary backup output. The `-Fc` option creates a PostgreSQL
custom-format archive.

Check that the file exists and is non-empty:

``` bash
ls -lh backups/appdb.dump
```

A non-empty file alone does not prove the backup is valid. Inspect its
contents using PostgreSQL tools.

### Step 3: List archive contents

``` bash
docker compose exec -T db pg_restore --list < backups/appdb.dump
```

This reads the archive's table of contents. Keep a copy of the backup
outside the primary host or storage failure domain.

### Step 4: Create a separate restore target

``` bash
docker compose exec db createdb -U appuser restore_test
```

### Step 5: Restore the backup

``` bash
docker compose exec -T db pg_restore \
  -U appuser \
  -d restore_test \
  --no-owner \
  < backups/appdb.dump
```

This lab uses the same PostgreSQL instance for simplicity. A real
recovery drill should also test restoration to a separate instance or
environment so that it covers host or storage loss.

If the target database already contains conflicting objects, restore may
report errors. Restore into a fresh target when testing a full logical
backup, or deliberately plan object ownership and conflict handling.

### Step 6: Verify restored data

``` bash
docker compose exec db psql -U appuser -d restore_test -c '\dt'
docker compose exec db psql -U appuser -d restore_test -c 'SELECT * FROM customers;'
```

Compare table counts, key records, schema, ownership, extensions, and
application-level behavior as appropriate. For real data, use validation
suited to the application's requirements rather than checking only that
one table exists.

### Step 7: Record the recovery result

Document:

-   Backup timestamp and source database.
-   Tool and database versions.
-   Backup file location and checksum.
-   Restore destination and elapsed time.
-   Validation checks performed and results.
-   Missing dependencies or manual steps.

Optional checksum on Linux:

``` bash
sha256sum backups/appdb.dump
```

On macOS, `shasum -a 256` is commonly available. A checksum can help
detect file changes; it does not prove that a backup contains all
required data.

### Step 8: Clean up carefully

The restore target is a database inside the same persistent PostgreSQL
volume. Remove it only after validation if you want to reset the lab:

``` bash
docker compose exec db dropdb -U appuser restore_test
```

Keep or remove the backup file according to your practice needs. Do not
delete the persistent volume unless you intend to erase all databases
stored there.

## 8. Physical backups and storage snapshots

### PostgreSQL physical backup concepts

PostgreSQL supports physical backup workflows such as base backups and
WAL archiving. These are used in more advanced recovery plans, including
point-in-time recovery (PITR). A valid PITR plan requires the
appropriate base backup, WAL files covering the target time, correct
configuration, and a tested recovery process.

Do not copy a live PostgreSQL data directory using a plain `cp` command
and assume the result is consistent. Use PostgreSQL-supported tooling or
a documented filesystem/storage snapshot process that coordinates with
the database.

### Snapshot considerations

Before relying on a storage snapshot, answer:

-   Is the snapshot atomic across all required volumes?
-   Does the database need to be quiesced or put into a supported backup
    mode?
-   Are write-ahead logs or transaction logs captured appropriately?
-   Can the snapshot be restored to another host or region?
-   Are encryption keys and access permissions available during
    recovery?
-   How long does a restore take at realistic data sizes?
-   Does the process preserve the required consistency guarantees?

### Logical vs. physical vs. snapshot

  -------------------------------------------------------------------------
  Method                  Best fit                Main caution
  ----------------------- ----------------------- -------------------------
  Logical dump            Portability, selective  May be slow for large
                          recovery, small/medium  datasets; check roles,
                          database migrations     extensions, and metadata.

  Physical backup         Large databases and     Version/layout
                          database-specific       compatibility and log
                          recovery workflows      management matter.

  Storage snapshot        Fast volume-level       May be crash-consistent
                          recovery where          rather than
                          supported               application-consistent;
                                                  validate coordination.

  Replication             Availability and        Replication can copy
                          reducing recovery time  accidental
                          after some failures     deletes/corruption; it is
                                                  not a substitute for
                                                  backups.
  -------------------------------------------------------------------------

## 9. External storage and database services

A database does not have to store its durable data in a local Docker
named volume.

### External block storage

Examples include cloud block volumes attached to a host running Docker.
The filesystem and database files may be on that volume, with Docker
mounting the path into the container.

Operational requirements include:

-   Correct attachment and mount lifecycle.
-   Filesystem and ownership configuration.
-   Backup and snapshot policy.
-   Encryption and access control.
-   Monitoring of capacity and latency.
-   A documented process for reattaching storage after host failure.
-   Avoiding unsafe simultaneous writable attachment unless the storage
    and database design explicitly support it.

### Network file storage

Network file systems can be appropriate for some shared files and
workloads, but database support depends on the specific database,
filesystem, protocol, locking, latency, and vendor guidance. Do not
assume every network share is safe for database data files.

### Managed database services

For production systems, a managed PostgreSQL/MySQL service may provide
automated backups, patching options, monitoring, replication, and
recovery features. These reduce some operational tasks but do not remove
responsibility for:

-   Credentials and network access.
-   Retention and backup policies.
-   Restore drills and application validation.
-   Data residency and compliance requirements.
-   Cost and capacity management.
-   Regional outage and disaster-recovery planning.

### Choosing an approach

Use a local named volume for a simple single-host lab. For production,
select storage based on availability, performance, consistency, recovery
objectives, supportability, and cost---not only convenience.

## 10. Database upgrades and migrations

Changing a container image tag is not the same as upgrading a database
safely. Database engines can change data-directory formats and require
explicit upgrade steps.

### Safer upgrade workflow

1.  Read the database vendor's upgrade notes for the exact source and
    target versions.
2.  Identify supported in-place upgrade or dump/restore paths.
3.  Inventory extensions, users, permissions, collations, and
    application compatibility.
4.  Take a verified backup and ensure a recovery path exists.
5.  Test the procedure using a copy of representative data.
6.  Measure migration duration and application downtime.
7.  Plan connection cutover and rollback constraints.
8.  Perform the production change during an approved window.
9.  Verify database health and application behavior.
10. Keep the previous backup and recovery materials according to
    retention policy.

### Why "just change the image" can fail

A new database major version may reject the old data directory or
require a formal upgrade process. A backup may also require compatible
restore tools. Never experiment with a production volume by switching
image versions without a tested plan.

## 11. Recovery planning and disaster recovery

### RPO and RTO

-   **Recovery Point Objective (RPO):** the maximum acceptable amount of
    data loss, expressed as a time interval.
-   **Recovery Time Objective (RTO):** the target maximum time to
    restore service after an incident.

Example: if the business requires an RPO of 15 minutes, a daily backup
alone is usually insufficient. A five-minute RTO may require more than a
slow full dump restore. Actual design depends on database size, write
rate, replication, backup tooling, and budget.

### Example recovery plan

``` text
Incident detected
      |
Assess scope and select recovery point
      |
Protect evidence and prevent further damage
      |
Provision clean/isolated recovery environment
      |
Restore backup + logs as required
      |
Validate database integrity and application behavior
      |
Switch traffic according to approved cutover plan
      |
Monitor service and document incident
```

### Recovery scenarios to test

-   Container removed accidentally.
-   Named volume deleted or corrupted.
-   Host disk failure.
-   Credentials leaked or malicious data changed.
-   Database upgrade failure.
-   Regional or provider outage.
-   Backup file corrupt or unavailable.
-   Encryption key or account access unavailable during recovery.

### Backups vs. replication

Replication can reduce downtime and data loss for some failures, but it
may replicate unwanted changes, accidental deletions, or corruption.
Independent backups and isolated copies are still required for many
recovery scenarios.

## 12. Monitoring storage and database health

Monitor both container health and the underlying storage.

### Docker-level checks

``` bash
docker ps
docker stats
docker system df
docker volume ls
docker volume inspect <VOLUME_NAME>
docker logs <CONTAINER_NAME>
```

`docker system df` summarizes Docker disk usage; it does not replace
monitoring the free space of the filesystem or external storage where
volumes reside.

On a Linux host, useful checks include:

``` bash
df -h
df -i
lsblk
```

-   `df -h`: filesystem space usage.
-   `df -i`: inode usage.
-   `lsblk`: block devices and mount relationships.

### Database-level checks

For PostgreSQL:

``` bash
docker compose exec db pg_isready -U appuser -d appdb
docker compose exec db psql -U appuser -d appdb -c 'SELECT now();'
```

Monitor relevant production metrics, including:

-   Database availability and connection errors.
-   Storage capacity and growth rate.
-   Read/write latency and I/O saturation.
-   Transaction volume, locks, and long-running queries.
-   Replication lag where applicable.
-   Backup success, age, duration, and restore-test results.
-   Container restarts, memory pressure, and out-of-memory events.

A container health check is useful, but it does not guarantee the
database is meeting performance, consistency, or business-level
requirements.

## 13. Troubleshooting

### A. Data disappears after recreating a container

Check whether the database directory was mounted to a named volume or
another durable storage location:

``` bash
docker inspect <CONTAINER_NAME>
docker volume ls
docker volume inspect <VOLUME_NAME>
```

Confirm that the new container uses the expected volume and that the
Compose project name has not changed the resource name. Data stored only
in the writable layer may be lost when the container is removed.

### B. Database image reports an incompatible data directory

Do not delete the volume. Review the database version, supported upgrade
path, logs, and backups. Restore or upgrade using the database vendor's
documented procedure.

### C. Database initialization variables seem ignored

The database may already have an initialized data directory. Use
database administration commands to change credentials and
configuration. Initialization variables commonly apply only to a fresh
data directory.

### D. Backup command creates an empty or invalid file

Check command exit status, logs, permissions, disk space, and the use of
`-T` when redirecting binary output through `docker compose exec`.
Inspect the archive with `pg_restore --list` or use the corresponding
database tool to validate it.

Do not treat file existence or a checksum as proof of a successful,
complete backup.

### E. Restore fails with ownership or object errors

Review database roles, extensions, target database state, tool versions,
and ownership requirements. Restore into a fresh test database when
appropriate and use the database vendor's options for ownership and
privileges.

### F. Host disk is full

``` bash
df -h
df -i
docker system df
docker volume ls
```

Identify the actual consuming filesystem and data before cleanup. Do not
run broad prune commands or delete volume directories blindly; that can
destroy databases or backups.

### G. Container cannot write to a mounted data directory

Check the container's UID/GID, directory ownership, mount mode,
filesystem status, and SELinux/AppArmor denials. Correct the narrow
permission or labeling issue rather than applying world-writable
permissions.

### H. A backup exists but recovery is too slow

Measure the complete restore path using representative data. Consider
database-supported physical backup, WAL/binlog retention, snapshots,
replication, storage performance, or managed database recovery features
according to the RPO/RTO requirements.

## 14. Production checklist

-   [ ] Database data is stored outside the container's disposable
    writable layer.
-   [ ] Volume lifecycle and project/resource names are documented.
-   [ ] Database ports are not exposed unnecessarily.
-   [ ] Credentials are not hard-coded in images or committed to source
    control.
-   [ ] Database image versions and upgrade procedures are controlled.
-   [ ] Backups use database-supported or properly coordinated methods.
-   [ ] Backup files are encrypted and access-controlled where required.
-   [ ] At least one backup copy is isolated from the primary failure
    domain.
-   [ ] Backup success and age are monitored.
-   [ ] Restore drills are performed and documented.
-   [ ] Recovery objectives (RPO/RTO) are defined with stakeholders.
-   [ ] Disk space, inodes, latency, and growth are monitored.
-   [ ] Replication is not treated as the only backup.
-   [ ] Credential rotation and incident recovery are documented.
-   [ ] Database consistency and application-level checks are part of
    recovery validation.
-   [ ] Production changes are tested before modifying live data or
    database versions.

## 15. Interview questions and answers

### 1. What is a stateful container?

A containerized workload that relies on data that must survive container
restarts, replacements, or deployment changes. Databases are a common
example.

### 2. Why should a database not rely on the container writable layer?

The writable layer belongs to a specific container instance and is not a
durable-data lifecycle strategy. Replacing the container can lose data
stored only there.

### 3. What is a Docker named volume?

A storage resource managed by Docker and mounted into one or more
containers. Its lifecycle is separate from an individual container, but
it still needs backup and recovery protection.

### 4. Does a named volume count as a backup?

No. It protects data from ordinary container replacement but may still
be lost through volume deletion, disk failure, corruption, or host loss.

### 5. What is the difference between a logical and physical backup?

A logical backup exports database objects and data in a logical
representation. A physical backup captures database storage using a
database-supported process and is often suited to larger or
database-specific recovery workflows.

### 6. Why is copying a live database directory with `cp` risky?

The database may be changing files and logs while the copy runs. The
resulting copy may not represent a consistent recoverable state. Use
database-supported backup tools or a documented coordinated snapshot
method.

### 7. What is point-in-time recovery?

Restoring a suitable base backup and applying the required transaction
logs to recover the database to a specific point in time, when the
database and backup configuration support it.

### 8. What is RPO?

Recovery Point Objective: the maximum acceptable data-loss interval,
usually measured in time.

### 9. What is RTO?

Recovery Time Objective: the target maximum time to restore service
after an incident.

### 10. Is replication a substitute for backups?

No. Replication can copy accidental deletions or corruption to replicas.
Independent backups are needed for many recovery scenarios.

### 11. Why might changing `POSTGRES_PASSWORD` not change an existing database password?

The image's initialization variable commonly applies only when the data
directory is first initialized. Change the database credential using
database administration procedures.

### 12. What should you verify after restoring a database?

Check schema, tables, row counts or key records, users and permissions,
extensions, application connectivity, and relevant integrity checks.
Test the application's actual behavior.

### 13. Why can changing a database image tag break the service?

Major database versions may have incompatible data-directory formats or
require an explicit upgrade process. Follow the vendor's supported
upgrade path and test it with a backup or clone.

### 14. What is the difference between a snapshot and a database backup?

A snapshot captures storage state according to the storage platform's
semantics. It may not be application-consistent. A database backup
process is designed around the database's consistency and recovery
requirements.

### 15. What should a database container monitoring plan include?

Availability, logs, container restarts, CPU/memory, disk capacity and
latency, database errors, backup status, replication lag where relevant,
and restore-test outcomes.

### 16. What is the safest way to test a restore?

Restore into an isolated, separate database or environment, validate its
contents and application behavior, measure the recovery time, and
document any missing steps.

### 17. Why should database ports generally not be published to the internet?

It expands the attack surface. Applications on a private container
network can usually connect to the database using its service name and
internal port without exposing it publicly.

### 18. When should you consider a managed database service?

When operational requirements for backups, patching, availability,
monitoring, scaling, and recovery exceed what the team can reliably
operate itself. Managed services still require correct security,
retention, and restore testing.

## 16. Scope boundaries

This README focuses on persistent data and recovery operations for
containerized stateful services.

Related topics intentionally reserved for other notes:

-   Basic Docker volume and bind-mount syntax and internals.
-   Compose service orchestration and general configuration.
-   Container hardening, capabilities, SELinux/AppArmor, and runtime
    restrictions.
-   Advanced PostgreSQL replication architecture, database clustering,
    and vendor-specific disaster-recovery design.
-   Kubernetes StatefulSets, PersistentVolumes, PersistentVolumeClaims,
    and storage classes.

## 17. Official references

-   [Docker storage overview](https://docs.docker.com/engine/storage/)
-   [Docker volumes](https://docs.docker.com/engine/storage/volumes/)
-   [Docker Compose
    volumes](https://docs.docker.com/compose/how-tos/volumes/)
-   [Docker Compose down
    command](https://docs.docker.com/reference/cli/docker/compose/down/)
-   [PostgreSQL documentation](https://www.postgresql.org/docs/)
-   [PostgreSQL
    `pg_dump`](https://www.postgresql.org/docs/current/app-pgdump.html)
-   [PostgreSQL
    `pg_restore`](https://www.postgresql.org/docs/current/app-pgrestore.html)
-   [PostgreSQL continuous archiving and point-in-time
    recovery](https://www.postgresql.org/docs/current/continuous-archiving.html)
-   [MySQL documentation](https://dev.mysql.com/doc/)
-   [Docker security](https://docs.docker.com/engine/security/)

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
├── 08-container-security/
└── 09-stateful-containers/
    └── README.md
```

From the root of your cloned repository:

``` bash
mkdir -p 09-stateful-containers
# Copy this README.md into that directory, then:
git add 09-stateful-containers/README.md
git commit -m "Add stateful container backup and recovery notes"
git push origin main
```
