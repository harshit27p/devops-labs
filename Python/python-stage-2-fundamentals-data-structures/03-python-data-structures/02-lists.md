# 2. Lists

## What is a list?
A list is an ordered, mutable collection. It allows duplicates and mixed types.

```python
services = ["nginx", "sshd", "docker"]
mixed = ["web-01", 443, True]
```

Use lists when order matters or the collection will change.

## Accessing elements

```python
print(services[0])
print(services[-1])
print(services[0:2])
```

Indexes start at zero. A missing index raises `IndexError`.

## Updating lists

```python
services.append("node-exporter")
services.extend(["redis", "postgresql"])
services.insert(0, "systemd")
services.remove("redis")
last_service = services.pop()
```

Other useful methods include `sort`, `reverse`, `index`, and `count`.

## Iteration

```python
for service in services:
    print(f"Checking {service}")
```

Use `enumerate()` when both index and value are needed.

## Copying and aliasing
Assignment does not copy a list:

```python
original = ["web", "database"]
alias = original
alias.append("cache")
print(original)  # also contains cache
```

Create a shallow copy with `copy()` or slicing. Nested mutable objects remain shared in a shallow copy; use `copy.deepcopy()` only when necessary.

## Lists as stacks

```python
pending = ["build", "test"]
pending.append("deploy")
next_task = pending.pop()
```

For efficient queues, use `collections.deque` rather than repeatedly removing the first list element.

## DevOps example

```python
services = ["nginx", "sshd", "docker", "redis"]
required_services = {"nginx", "sshd"}

for service in services:
    if service in required_services:
        print(f"Required service: {service}")
```

## Common pitfalls
- `remove(value)` raises `ValueError` if absent.
- `pop(index)` raises `IndexError` if invalid.
- Mutating a list while iterating can skip elements.
- `list.sort()` changes the list and returns `None`; `sorted(list)` returns a new list.

## Exercises
Maintain a deployed-service list, filter stopped services safely, sort hostnames, and demonstrate aliasing versus copying.
