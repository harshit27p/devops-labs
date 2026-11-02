# S3 Upload, Download and Object Metadata

## Upload
```python
from pathlib import Path
import boto3

s3 = boto3.client("s3")
path = Path("report.json")
s3.upload_file(
    str(path),
    "your-lab-bucket",
    "reports/report.json",
    ExtraArgs={"ContentType": "application/json"},
)
```

## Download
```python
s3.download_file(
    "your-lab-bucket",
    "reports/report.json",
    "downloaded-report.json",
)
```

## Metadata
Use `head_object` to inspect metadata without downloading the object:
```python
metadata = s3.head_object(
    Bucket="your-lab-bucket",
    Key="reports/report.json",
)
print(metadata["ContentLength"], metadata.get("ContentType"))
```

## Integrity
Do not assume an ETag is always an MD5 hash. Multipart uploads and encryption can change its meaning. Use supported checksum features when integrity verification is required.

## Exercises
1. Upload a JSON report.
2. Download it to a separate output path.
3. Inspect size, content type and metadata.
