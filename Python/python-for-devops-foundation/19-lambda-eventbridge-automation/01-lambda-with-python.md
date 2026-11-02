# AWS Lambda with Python

## Handler model
A Lambda handler receives an event and context:
```python
def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": "Inventory job accepted",
    }
```

## Boto3 inside Lambda
Use the function's execution role; do not package AWS access keys:
```python
import boto3

def lambda_handler(event, context):
    sts = boto3.client("sts")
    identity = sts.get_caller_identity()
    return {"account": identity["Account"]}
```

## Design
- Keep work within the configured timeout.
- Make event processing idempotent.
- Reuse clients outside the handler when safe.
- Avoid storing state only in memory.
- Keep package size and dependency versions controlled.
- Use environment variables for non-secret settings and a secret manager for secrets.

## Exercises
1. Create a Lambda that returns caller account ID.
2. Add structured logging.
3. Test handler logic locally with a sample event.
