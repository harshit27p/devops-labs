# EBS Snapshot Inventory and Retention

## List snapshots owned by the account
```python
paginator = ec2.get_paginator("describe_snapshots")
for page in paginator.paginate(OwnerIds=["self"]):
    for snapshot in page.get("Snapshots", []):
        print(
            snapshot["SnapshotId"],
            snapshot["VolumeId"],
            snapshot["StartTime"],
            snapshot["State"],
        )
```

## Retention considerations
Define:
- Required recovery point and retention duration.
- Backup schedule and copy/replication requirements.
- Legal or compliance holds.
- Excluded workloads and tagged exceptions.
- Whether snapshots are managed by AWS Backup or another backup system.

## Stale is not the same as old
A snapshot may be old but still required. A snapshot whose source volume no longer exists may be a candidate for review, but still needs ownership, tag, retention and backup-policy checks.

## Exercises
1. Export snapshot inventory.
2. Group snapshots by source volume.
3. Identify snapshots older than a configured age for review only.
