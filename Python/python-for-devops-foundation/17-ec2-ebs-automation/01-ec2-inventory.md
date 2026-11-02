# EC2 Inventory with Boto3

## Inventory instances
```python
import boto3

ec2 = boto3.client("ec2", region_name="ap-south-1")
paginator = ec2.get_paginator("describe_instances")

for page in paginator.paginate():
    for reservation in page.get("Reservations", []):
        for instance in reservation.get("Instances", []):
            tags = {t["Key"]: t["Value"] for t in instance.get("Tags", [])}
            print({
                "id": instance["InstanceId"],
                "type": instance["InstanceType"],
                "state": instance["State"]["Name"],
                "private_ip": instance.get("PrivateIpAddress"),
                "name": tags.get("Name", ""),
            })
```

## Useful filters
Filter by instance state, VPC, subnet, tag or instance ID. Use filters server-side to reduce returned data.

## Multi-region inventory
Regions are independent. Enumerate enabled regions only when required, then create a regional client for each. Do not accidentally run actions in every region.

## Exercises
1. Export instance ID, type, state, VPC, subnet and Name tag.
2. Count instances by state and region.
3. Identify instances missing owner or environment tags.
