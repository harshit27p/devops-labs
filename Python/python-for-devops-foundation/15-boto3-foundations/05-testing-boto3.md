# Testing Boto3 Automation

## Testing layers
- Unit tests: mock clients and assert API calls and decisions.
- AWS service mocks: Moto can emulate selected AWS services for many test cases.
- Integration tests: use a dedicated sandbox account and isolated resource names.
- Production validation: use read-only checks and staged rollout.

Install development dependencies:
```bash
python -m pip install pytest moto
```

Example with an injected client:
```python
def list_bucket_names(s3_client):
    response = s3_client.list_buckets()
    return [item["Name"] for item in response.get("Buckets", [])]
```

A unit test can pass a mock client with a controlled response. For Moto, check current service coverage and version-specific setup in its documentation.

## Test safety
- Never point destructive tests at production.
- Use unique resource names and tags.
- Clean up test resources in `finally` blocks or fixtures.
- Keep tests deterministic and avoid real credentials for unit tests.

## Exercises
1. Mock an EC2 describe response.
2. Test empty and multi-page results.
3. Test that dry-run mode never calls a delete method.
