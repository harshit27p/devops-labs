# Boto3 Sessions, Clients and Resources

## Session
A `boto3.Session` groups configuration such as credentials, profile and region:
```python
import boto3
session = boto3.Session(region_name="ap-south-1")
```

## Client interface
Clients map closely to AWS service API operations and expose low-level request/response structures:
```python
ec2 = session.client("ec2")
response = ec2.describe_instances()
```

## Resource interface
Resources provide a higher-level, object-oriented interface for selected services:
```python
s3 = session.resource("s3")
for bucket in s3.buckets.all():
    print(bucket.name)
```
Not every AWS service has a resource interface. Newer features and complete API coverage are generally available through clients.

## Design guidance
- Pass a session or client into functions to make code testable.
- Create clients once and reuse them where appropriate.
- Set the region deliberately.
- Use clients when you need full API coverage, precise request parameters or paginators.
- Use resources for concise object-oriented operations when supported.

## Exercises
1. List S3 buckets using a client.
2. List them using the S3 resource interface.
3. Refactor a function to accept an injected EC2 client.
