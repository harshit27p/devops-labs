# JSON Processing

## Parse and serialize
```python
import json

payload = '{"service": "nginx", "port": 443, "enabled": true}'
data = json.loads(payload)
print(data["service"])

encoded = json.dumps(data, indent=2, sort_keys=True)
```

For files, use `json.load()` and `json.dump()`:
```python
from pathlib import Path
import json

with Path("inventory.json").open(encoding="utf-8") as handle:
    inventory = json.load(handle)

with Path("inventory-copy.json").open("w", encoding="utf-8") as handle:
    json.dump(inventory, handle, indent=2)
    handle.write("\\n")
```

## Validate the structure
A successful parse proves syntax only, not that required fields or types are correct.
```python
def validate_server(item):
    if not isinstance(item, dict):
        raise ValueError("server must be an object")
    if not isinstance(item.get("name"), str) or not item["name"].strip():
        raise ValueError("name is required")
    port = item.get("port")
    if not isinstance(port, int) or not 1 <= port <= 65535:
        raise ValueError("invalid port")
    return item
```

## API response pattern
```python
import requests

response = requests.get(
    "https://api.github.com/repos/OWNER/REPO",
    timeout=(3, 10),
)
response.raise_for_status()
repository = response.json()
```

## Common mistakes
- Confusing `json.load()` (file object) with `json.loads()` (string).
- Treating JSON `null` as the string `"null"` instead of Python `None`.
- Assuming parsed data is valid for your application.
- Logging secrets or overwriting source data without validation.

## Exercises
1. Read a server inventory and print enabled servers.
2. Reject missing hostnames and invalid ports.
3. Save a public API response as formatted JSON.
