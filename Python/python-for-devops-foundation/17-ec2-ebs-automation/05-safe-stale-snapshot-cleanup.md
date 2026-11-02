# Safe Stale EBS Snapshot Cleanup

## Core rule
Do not delete a snapshot merely because it is old or because its source volume is unattached. An unattached volume is not a deleted volume. A snapshot of a deleted source volume may still be required for recovery or compliance.

## Candidate policy
A snapshot can only become a review candidate when all configured checks pass:
- Snapshot is owned by the expected account.
- Region is explicitly allowed.
- Snapshot is completed.
- Source volume no longer exists, or a separately approved policy identifies it.
- Snapshot is older than the retention threshold.
- No protected tag, legal hold or exclusion applies.
- Backup owner has approved deletion.
- A current recovery copy exists if policy requires one.

## Dry-run-first pattern
```python
def plan_snapshot_deletion(snapshot, policy):
    reasons = []
    if snapshot.get("State") != "completed":
        reasons.append("snapshot is not completed")
    if snapshot.get("SnapshotId") in policy["protected_ids"]:
        reasons.append("snapshot is protected")
    if snapshot.get("AgeDays", 0) < policy["minimum_age_days"]:
        reasons.append("below retention age")
    if not snapshot.get("SourceVolumeConfirmedDeleted", False):
        reasons.append("source volume deletion not confirmed")
    return {
        "snapshot_id": snapshot["SnapshotId"],
        "eligible": not reasons,
        "reasons": reasons,
        "action": "would-delete" if not reasons else "skip",
    }
```
This is a policy-planning example, not a complete AWS cleanup implementation. Build and validate the full inventory and approval workflow before adding `delete_snapshot`.

## Execution safeguards
- Dry-run is the default.
- Require explicit `--execute` and a second approval for destructive actions.
- Re-fetch the snapshot immediately before deletion.
- Verify account, region, snapshot ID and policy again.
- Persist an audit record.
- Never bulk-delete based only on age.
- Use AWS Backup lifecycle policies where they meet the requirement.

## Exercises
1. Build a report of candidate snapshots and skip reasons.
2. Add protected tag and explicit ID exclusions.
3. Unit-test that dry-run never calls `delete_snapshot`.
