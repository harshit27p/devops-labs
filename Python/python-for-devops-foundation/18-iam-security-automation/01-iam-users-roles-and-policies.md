# IAM Users, Roles and Policies

## IAM concepts
- User: identity for a person or workload in IAM's user model.
- Group: collection of IAM users.
- Role: assumable identity that provides temporary credentials.
- Policy: JSON document defining allowed or denied actions on resources, optionally under conditions.

## Read-only inventory
```python
import boto3
iam = boto3.client("iam")

for page in iam.get_paginator("list_roles").paginate():
    for role in page.get("Roles", []):
        print(role["RoleName"], role["Arn"])
```

## Policy evaluation mindset
Explicit deny overrides allow. Permissions can be affected by identity policies, resource policies, permission boundaries, SCPs, session policies and conditions.

## Exercises
1. List roles and attached managed policies.
2. Export role metadata.
3. Explain the difference between an IAM role and an IAM user.
