# EC2 Instance Lifecycle Automation

## Start and stop
```python
# Read and verify the target first.
instance_id = "i-0123456789abcdef0"
ec2.start_instances(InstanceIds=[instance_id])
ec2.get_waiter("instance_running").wait(
    InstanceIds=[instance_id],
    WaiterConfig={"Delay": 10, "MaxAttempts": 30},
)
```
Stopping an instance can interrupt workloads and may affect public IPs, storage, monitoring and dependent systems. Termination is destructive and may delete EBS volumes configured for deletion on termination.

## Safe lifecycle design
- Require explicit instance IDs or a narrow tag selector.
- Exclude production and critical workloads.
- Confirm account, region, owner and maintenance window.
- Display intended action before executing.
- Require an explicit `--execute` or approval token.
- Record the API response and final state.

## Exercises
1. Implement a read-only state report.
2. Add a dry-run stop plan.
3. Test that the script refuses to stop instances without an explicit approval flag.
