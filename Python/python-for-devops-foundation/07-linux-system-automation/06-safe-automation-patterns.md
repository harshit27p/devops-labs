# 6. Safe Automation Patterns

## Start read-only
Build an inspection mode before implementing changes. Report what would happen and require an explicit option to perform a destructive action.

## Dry-run design

```python
def remove_old_artifact(path, dry_run=True):
    if dry_run:
        print(f"DRY RUN: would remove {path}")
        return

    # Implement deletion only after validating the path,
    # ownership, retention policy, and approval requirements.
    raise NotImplementedError("Deletion intentionally not implemented")
```

A dry-run must not perform the destructive operation indirectly.

## Validate scope
Before modifying files or infrastructure:
- Resolve and validate target paths.
- Check that targets remain within an approved root directory.
- Consider symlinks and path traversal.
- Exclude system-critical locations.
- Verify ownership and permissions.
- Back up data and define rollback steps.

## Timeouts and retries
- Set timeouts for network and subprocess operations.
- Retry only transient failures.
- Use bounded retries and backoff.
- Avoid retrying non-idempotent operations without an idempotency strategy.

## Idempotency
An operation is idempotent when repeating it produces the same intended state. Prefer “ensure directory exists” over “create directory and fail if it exists.” For cloud APIs, use resource state checks and idempotency tokens where supported.

## Auditability
Log the action, target, result, and correlation identifier. Do not log secrets. For production changes, integrate approvals and audit records with the organization's deployment workflow.

## When to use established tools
Use Ansible for fleet configuration, Terraform for declarative infrastructure provisioning, systemd for service lifecycle, and native monitoring systems for continuous observability. Python is especially useful for glue logic, API integrations, custom checks, and data processing.

## Capstone exercise
Create a read-only Linux host inventory tool that reports hostname, OS, disk usage, selected service status, and file permissions for a user-provided test directory. Add structured logs, timeouts, clear error handling, and a dry-run flag for any future changes.
