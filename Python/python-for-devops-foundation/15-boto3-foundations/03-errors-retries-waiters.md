# Boto3 Errors, Retries and Waiters

## Catch service errors
Boto3 service errors are commonly surfaced as `botocore.exceptions.ClientError`:
```python
from botocore.exceptions import ClientError

try:
    response = ec2.describe_instances()
except ClientError as exc:
    code = exc.response.get("Error", {}).get("Code", "Unknown")
    message = exc.response.get("Error", {}).get("Message", "")
    print(f"AWS API error {code}: {message}")
    raise
```
Do not swallow errors and continue as if an operation succeeded.

## Retry behavior
Botocore has configurable retry behavior. Configure retries through a `botocore.config.Config` object:
```python
from botocore.config import Config
import boto3

config = Config(
    retries={"mode": "standard", "max_attempts": 5},
    connect_timeout=3,
    read_timeout=10,
)
ec2 = boto3.client("ec2", config=config)
```
Check the SDK's current retry semantics for the installed version. Avoid stacking aggressive custom retries on top of SDK retries.

## Waiters
Waiters poll for a resource state:
```python
ec2.get_waiter("instance_running").wait(
    InstanceIds=["i-0123456789abcdef0"],
    WaiterConfig={"Delay": 15, "MaxAttempts": 20},
)
```
Use waiters instead of fixed sleeps when the service provides an appropriate waiter.

## Exercises
1. Handle `AccessDenied` without exposing credentials.
2. Configure standard retries.
3. Wait for a lab instance to reach `running`, with a bounded timeout.
