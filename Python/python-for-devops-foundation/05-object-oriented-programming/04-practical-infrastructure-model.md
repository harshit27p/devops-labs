# 4. Practical Infrastructure Model

This example models cloud-like resources without connecting to a real cloud account.

```python
from dataclasses import dataclass, field

@dataclass
class ComputeInstance:
    instance_id: str
    region: str
    state: str = "stopped"
    tags: dict[str, str] = field(default_factory=dict)

    def start(self) -> None:
        self.state = "running"

    def stop(self) -> None:
        self.state = "stopped"

    def add_tag(self, key: str, value: str) -> None:
        if not key.strip():
            raise ValueError("Tag key cannot be empty")
        self.tags[key] = value

instance = ComputeInstance(
    instance_id="i-example001",
    region="ap-south-1",
)
instance.add_tag("Environment", "test")
instance.start()

print(instance)
```

## Design observations
- `dataclass` generates common methods such as initialization and representation.
- `field(default_factory=dict)` creates a separate dictionary for each instance. Never use `{}` as a mutable dataclass default.
- Methods change the in-memory model only. They do not start or stop a real EC2 instance.
- A production adapter would call Boto3 and handle authentication, permissions, pagination, retries, and API errors.

## Suggested extension
Create a `ResourceInventory` class that stores instances, finds them by ID, filters by state, and produces a summary. Keep cloud API access outside the inventory model.

## Exercises
1. Add validation for instance IDs and region names.
2. Add a method that returns all running instances.
3. Write unit tests for state transitions.
4. Explain why the example does not perform a real AWS operation.
