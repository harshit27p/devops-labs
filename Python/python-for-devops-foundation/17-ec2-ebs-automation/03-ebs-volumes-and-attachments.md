# EBS Volumes and Attachments

## Inventory
```python
paginator = ec2.get_paginator("describe_volumes")
for page in paginator.paginate():
    for volume in page.get("Volumes", []):
        print(
            volume["VolumeId"],
            volume["State"],
            volume["Size"],
            volume.get("Attachments", []),
        )
```

## Important distinctions
- `available` generally means not attached to an instance.
- `in-use` means attached.
- Unattached does not automatically mean unused or safe to delete.
- A volume may be intentionally retained for recovery, migration, forensic analysis or later attachment.

## Candidate review
Before proposing deletion, inspect tags, creation time, owner, application dependencies, backups, encryption, snapshot coverage, retention policy and change approvals.

## Exercises
1. Report available volumes.
2. Flag missing owner and purpose tags.
3. Produce a candidate review report without deleting anything.
