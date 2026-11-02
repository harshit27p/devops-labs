# 6. Comprehensions

Comprehensions provide concise syntax for creating lists, sets, and dictionaries from iterables.

## List comprehension

```python
services = ["nginx", "sshd", "docker"]
uppercase = [service.upper() for service in services]
```

Equivalent loop:

```python
uppercase = []
for service in services:
    uppercase.append(service.upper())
```

## Filtering

```python
ports = [22, 80, 443, 8080, 3306]
web_ports = [port for port in ports if port in {80, 443, 8080}]
```

## Set and dictionary comprehensions

```python
hostnames = ["web-01", "web-02", "web-01"]
prefixes = {name.split("-")[0] for name in hostnames}

services = ["nginx", "sshd", "docker"]
status = {name: "unknown" for name in services}
```

## Practical inventory example

```python
instances = [
    {"name": "web-01", "state": "running"},
    {"name": "db-01", "state": "stopped"},
    {"name": "web-02", "state": "running"},
]

running_names = [
    item["name"]
    for item in instances
    if item.get("state") == "running"
]
print(running_names)
```

Nested comprehensions can become hard to read. Prefer a normal loop or helper function when logic has multiple conditions or side effects.

## Exercises
Create a list of even port numbers, map service names to their lengths, deduplicate hostnames with a set comprehension, and rewrite a complex comprehension as a readable loop.
