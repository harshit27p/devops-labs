# 17 — EC2 and EBS Automation

- `01-ec2-inventory.md`
- `02-instance-lifecycle-and-waiters.md`
- `03-ebs-volumes-and-attachments.md`
- `04-snapshot-inventory-and-retention.md`
- `05-safe-stale-snapshot-cleanup.md`

Read-only inventory comes first. Stop, terminate, detach and snapshot deletion operations must be guarded by dry-run, allowlists, retention rules and explicit approvals.
