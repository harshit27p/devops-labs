# Role-Based Access for Automation

## Prefer roles over long-lived access keys
Use:
- EC2 instance profiles for code running on EC2.
- ECS task roles for containers.
- Lambda execution roles for functions.
- IAM Identity Center or role assumption for human-operated automation.
- OIDC federation for supported CI/CD platforms.

## Least privilege
Grant only the actions and resources required. Scope resource ARNs and use conditions where supported. Separate read-only inventory roles from change-execution roles.

## Verify identity
```python
import boto3
identity = boto3.client("sts").get_caller_identity()
print(identity["Account"], identity["Arn"])
```

## Exercises
1. Define separate read-only and cleanup roles.
2. Document required actions for an S3 inventory script.
3. Explain why access keys should not be embedded in Docker images or Git repositories.
