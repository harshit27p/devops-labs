# S3 Bucket Security and Encryption

## Security controls
- Block Public Access at account and bucket levels unless public access is intentionally required.
- Use bucket policies and IAM policies with least privilege.
- Enable default server-side encryption.
- Prefer SSE-KMS where key-level audit/control is required.
- Require TLS in bucket policies.
- Review access logging, CloudTrail data events and replication needs.

## Inspect public access block
```python
response = s3.get_public_access_block(Bucket="your-lab-bucket")
print(response["PublicAccessBlockConfiguration"])
```

## Inspect encryption
```python
response = s3.get_bucket_encryption(Bucket="your-lab-bucket")
print(response["ServerSideEncryptionConfiguration"])
```

## Policy review
Never copy a broad wildcard policy into production. Validate principals, actions, resources and conditions. Deny insecure transport where appropriate, and test policy effects in a sandbox.

## Exercises
1. Inspect public access block settings.
2. Inspect default encryption.
3. Write a review checklist for a bucket policy.
