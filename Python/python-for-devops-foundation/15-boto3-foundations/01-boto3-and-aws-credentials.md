# Boto3 and AWS Credentials

## What is Boto3?
Boto3 is the AWS SDK for Python. It lets Python applications call AWS service APIs to inspect and manage resources.

Install:
```bash
python -m pip install boto3
```

Verify the active identity before doing anything:
```python
import boto3

sts = boto3.client("sts")
identity = sts.get_caller_identity()
print({
    "account": identity["Account"],
    "arn": identity["Arn"],
})
```

## Credential provider chain
Boto3 can obtain credentials from supported sources such as:
- Environment variables.
- Shared AWS config and credentials files.
- IAM Identity Center profiles.
- Container/task credentials.
- EC2 instance profiles.
- Other supported credential providers.

Prefer temporary role credentials. On EC2, ECS or Lambda, attach an IAM role rather than copying access keys onto the machine.

## Local profile
```python
import boto3

session = boto3.Session(profile_name="dev-lab", region_name="ap-south-1")
sts = session.client("sts")
print(sts.get_caller_identity()["Arn"])
```

## Safety checks
- Verify account ID and region at startup.
- Separate development and production profiles.
- Use a dedicated automation role.
- Never print secret access keys or session tokens.
- Do not commit `~/.aws/credentials` or local secret files.

## Exercises
1. Print the active account and ARN.
2. Create a session with a named profile.
3. Fail closed if the account is not the expected lab account.
