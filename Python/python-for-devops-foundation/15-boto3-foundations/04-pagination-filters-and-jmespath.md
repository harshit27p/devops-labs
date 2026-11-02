# Pagination, Filters and Response Queries

## Why pagination matters
Many AWS list/describe operations return only part of the result set. Use paginators when available:
```python
paginator = ec2.get_paginator("describe_instances")
for page in paginator.paginate(
    Filters=[{"Name": "instance-state-name", "Values": ["running"]}]
):
    for reservation in page["Reservations"]:
        for instance in reservation["Instances"]:
            print(instance["InstanceId"], instance["State"]["Name"])
```

## Filters
Server-side filters reduce returned data and API traffic. Confirm filter names and values in the service API documentation.

## JMESPath
AWS CLI and Botocore use JMESPath-style query expressions for structured response selection. Python code can also use the `jmespath` package:
```bash
python -m pip install jmespath
```
```python
import jmespath
ids = jmespath.search(
    "Reservations[].Instances[].InstanceId",
    response,
)
```

## Safety
- Do not assume the first page is the complete inventory.
- Use stable resource identifiers.
- Handle empty responses.
- Avoid broad scans across all regions unless explicitly required.

## Exercises
1. List all running instances using a paginator.
2. Filter instances by a tag.
3. Export a complete multi-page inventory.
