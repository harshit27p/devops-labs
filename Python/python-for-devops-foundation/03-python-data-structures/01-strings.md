# 1. Strings

## What is a string?
A string (`str`) is an immutable sequence of Unicode characters.

```python
service = "nginx"
message = 'Service is active'
multiline = """First line
Second line"""
```

## Indexing and slicing

```python
hostname = "web-01"
print(hostname[0])     # w
print(hostname[-1])    # 1
print(hostname[0:3])   # web
print(hostname[4:])    # 01
```

The slice end index is excluded. An invalid direct index raises `IndexError`; slicing beyond the boundary is allowed.

## Common methods

```python
raw = "  ERROR: disk space low  "
print(raw.strip())
print(raw.lower())
print(raw.upper())
print(raw.replace("disk", "filesystem"))
print(raw.split(":"))
```

Useful methods include `strip`, `split`, `join`, `replace`, `find`, `count`, `startswith`, `endswith`, `lower`, and `upper`.

## Split and join

```python
record = "nginx,active,443"
service, state, port_text = record.split(",")
port = int(port_text)

services = ["nginx", "sshd", "docker"]
print(",".join(services))
```

Validate field counts before unpacking untrusted or inconsistent records.

## F-strings

```python
service = "nginx"
latency_ms = 125.7
print(f"{service} response time: {latency_ms:.1f} ms")
```

## Parsing an ARN-like identifier

```python
arn = "arn:aws:iam::123456789012:user/automation-user"
parts = arn.split(":")

if len(parts) >= 6:
    resource = parts[5]
    username = resource.split("/")[-1]
    print(username)
else:
    raise ValueError("Unexpected ARN format")
```

For production, validate the expected structure or use the cloud SDK rather than relying on fragile assumptions.

## Security
Treat external strings as untrusted. Do not build shell commands or SQL by concatenating untrusted strings. Use safe APIs, argument arrays, and parameterized queries.

## Exercises
1. Normalize service names.
2. Parse and validate a comma-separated service record.
3. Extract a filename with `pathlib`.
4. Format response times to two decimal places.
