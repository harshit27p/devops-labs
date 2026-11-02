# S3 Buckets and Objects with Boto3

## List buckets
```python
import boto3
s3 = boto3.client("s3")
for item in s3.list_buckets().get("Buckets", []):
    print(item["Name"])
```

## Create a bucket
Bucket creation parameters vary by region. For regions other than `us-east-1`, include a `CreateBucketConfiguration` with the target location constraint:
```python
s3.create_bucket(
    Bucket="globally-unique-lab-bucket-name",
    CreateBucketConfiguration={"LocationConstraint": "ap-south-1"},
)
```
Bucket names are globally unique within the S3 partition. Check whether the name is available and use a lab-specific prefix.

## List objects
```python
paginator = s3.get_paginator("list_objects_v2")
for page in paginator.paginate(Bucket="your-lab-bucket"):
    for obj in page.get("Contents", []):
        print(obj["Key"], obj["Size"])
```

## Delete object
Deletion is destructive and may interact with versioning:
```python
# Only run against a disposable lab key after verifying the target.
s3.delete_object(Bucket="your-lab-bucket", Key="temporary/test.txt")
```

## Exercises
1. List buckets and their regions.
2. List every object in a lab bucket using pagination.
3. Create and remove a disposable test bucket after emptying it safely.
