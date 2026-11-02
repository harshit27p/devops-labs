# Scheduling and Job Execution

Choose the scheduler that matches the runtime and operational environment.

## Common options
- Linux `cron` for simple time-based jobs.
- `systemd` timers for service-managed Linux jobs.
- Kubernetes CronJobs for containerized cluster workloads.
- Cloud schedulers such as Amazon EventBridge Scheduler for managed cloud workloads.
- Workflow engines for multi-step jobs with dependencies and state.

## Operational checklist
- Use absolute paths and a known working directory.
- Set a controlled environment and timezone.
- Prevent overlapping runs when required.
- Capture stdout/stderr and exit status.
- Set runtime limits and alert on repeated failure.
- Document owner, schedule and recovery procedure.

Scheduling does not make a script reliable; the job itself still needs idempotency and observability.
