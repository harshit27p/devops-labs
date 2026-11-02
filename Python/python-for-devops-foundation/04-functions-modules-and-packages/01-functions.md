# 1. Functions

## Why functions matter in DevOps
A function packages a focused operation behind a reusable interface. Functions reduce duplicated code and make automation easier to test, review, and troubleshoot.

Typical operations include checking a service, validating configuration, querying an API, rotating a log, or reporting disk usage.

## Define and call a function

```python
def greet_operator():
    print("Starting infrastructure checks")

greet_operator()
```

Use parameters to supply changing values:

```python
def check_service(service_name):
    print(f"Checking {service_name}")

check_service("nginx")
check_service("sshd")
```

## Return values
Prefer returning data from a function rather than printing everything inside it. This allows callers to decide whether to log, display, store, or test the result.

```python
def is_valid_port(port):
    return isinstance(port, int) and 1 <= port <= 65535

if is_valid_port(443):
    print("Port is valid")
```

A function without an explicit `return` returns `None`.

## Single responsibility
A function should have one clear purpose. Avoid combining input parsing, cloud API calls, deletion, and reporting in one large function.

```python
def calculate_used_percent(used_bytes, total_bytes):
    if total_bytes <= 0:
        raise ValueError("total_bytes must be positive")
    return (used_bytes / total_bytes) * 100
```

## Type hints and docstrings

```python
def disk_warning(used_percent: float, threshold: float = 85.0) -> bool:
    """Return True when disk usage reaches the warning threshold."""
    return used_percent >= threshold
```

Type hints document expected values and help static analysis tools. Python does not enforce them automatically at runtime.

## Avoid hidden side effects
A function that silently changes global variables, deletes files, or modifies cloud resources is harder to reason about. Make important effects explicit in its name, arguments, and documentation.

## Exercises
1. Write a function that validates a TCP port.
2. Write a function that calculates disk usage percentage.
3. Separate a service-check script into input, check, and report functions.
4. Add type hints and docstrings to each function.
