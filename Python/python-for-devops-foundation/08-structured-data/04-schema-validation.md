# Schema Validation and Data Contracts

Parsing checks syntax. Validation checks whether values meet the contract expected by the application.

Example contract:
- `name`: non-empty string.
- `address`: non-empty hostname or IP string.
- `port`: integer from 1 to 65535.
- `enabled`: boolean.

```python
def validate_target(value):
    if not isinstance(value, dict):
        raise ValueError("target must be an object")
    name = value.get("name")
    address = value.get("address")
    port = value.get("port", 22)
    if not isinstance(name, str) or not name.strip():
        raise ValueError("name is required")
    if not isinstance(address, str) or not address.strip():
        raise ValueError("address is required")
    if not isinstance(port, int) or not 1 <= port <= 65535:
        raise ValueError("invalid port")
    return {"name": name.strip(), "address": address.strip(), "port": port}
```

Validate at trust boundaries: files, CLI input, API responses and webhooks. For larger projects, consider Pydantic or JSON Schema tooling and consult the selected library's current documentation.

Exercises: validate a server inventory, test missing fields and boundary values, and ensure invalid records cannot reach action-performing functions.
