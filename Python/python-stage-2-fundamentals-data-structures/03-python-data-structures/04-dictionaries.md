# 4. Dictionaries

## What is a dictionary?
A dictionary stores key-value pairs. Keys are unique and must be hashable. Modern Python dictionaries preserve insertion order.

```python
server = {
    "hostname": "web-01",
    "region": "ap-south-1",
    "port": 443,
    "active": True,
}
```

Dictionaries are a natural representation for structured resource data and decoded JSON.

## Reading values safely

```python
print(server["hostname"])
print(server.get("private_ip", "not-assigned"))
```

Square-bracket lookup raises `KeyError` for a missing key. `get()` returns a default.

## Add, update, and delete

```python
server["environment"] = "production"
server["port"] = 8443
server.update({"active": False, "owner": "platform"})
owner = server.pop("owner", None)
```

## Iteration

```python
for key, value in server.items():
    print(f"{key}: {value}")
```

## Nested structures

```python
inventory = {
    "web-01": {
        "region": "ap-south-1",
        "services": ["nginx", "sshd"],
    },
    "db-01": {
        "region": "ap-south-1",
        "services": ["postgresql"],
    },
}

for hostname, details in inventory.items():
    print(hostname, details["services"])
```

Validate external data before assuming nested keys exist.

## JSON conversion

```python
import json

payload = {"service": "nginx", "healthy": True, "port": 443}
json_text = json.dumps(payload, indent=2)
restored = json.loads(json_text)

print(json_text)
print(restored["service"])
```

`dumps()` converts a Python object to JSON text; `loads()` parses JSON text. Use `dump()` and `load()` for file objects.

## API response handling

```python
response_data = {
    "items": [
        {"username": "alice", "state": "open"},
        {"username": "bob", "state": "closed"},
    ]
}

for item in response_data.get("items", []):
    print(item.get("username", "unknown"))
```

For real APIs, check HTTP status, handle network errors, paginate where required, and respect rate limits.

## Exercises
Create an EC2-like resource dictionary, update its tags/state, safely read optional keys, iterate nested inventory, and serialize it to JSON.
