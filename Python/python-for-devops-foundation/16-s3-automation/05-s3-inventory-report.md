# S3 Inventory Reporting Project

Create a read-only report of buckets and selected configuration:
- Bucket name and region.
- Public access block status.
- Default encryption status.
- Versioning status.
- Lifecycle rule count.

Use one API call per relevant bucket, catch expected service errors and record unknown/unavailable states rather than assuming a setting is disabled.

Suggested output fields:
```text
bucket,region,public_access_block,encryption,versioning,lifecycle_rules
```

Do not print object contents or credentials. Consider API throttling and permissions. A missing permission is not proof that a security control is absent.

Exercises: export CSV and JSON, flag buckets requiring review and test with mocked responses.
