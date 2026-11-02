# S3 Versioning, Lifecycle and Retention

## Versioning
Versioning preserves multiple object versions and can help recover overwritten or deleted objects. It also increases storage use.

```python
s3.put_bucket_versioning(
    Bucket="your-lab-bucket",
    VersioningConfiguration={"Status": "Enabled"},
)
```

## Lifecycle
Lifecycle rules can transition or expire objects based on age, prefix or tags. Design rules around business retention, legal holds, recovery requirements and cost.

## Delete markers
In versioned buckets, a normal delete may create a delete marker rather than permanently remove prior versions. Permanent deletion of versions requires explicit version IDs and should be tightly controlled.

## Exercises
1. Enable versioning on a disposable bucket.
2. Inspect object versions and delete markers.
3. Design a lifecycle policy on paper before applying it to a lab bucket.
