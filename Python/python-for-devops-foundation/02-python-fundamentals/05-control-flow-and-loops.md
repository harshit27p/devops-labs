# 5. Control Flow and Loops

## Conditional statements

```python
status_code = 503

if status_code == 200:
    print("Request succeeded")
elif 400 <= status_code < 500:
    print("Client error")
elif 500 <= status_code < 600:
    print("Server error")
else:
    print("Unexpected status")
```

Branches are evaluated from top to bottom; the first matching branch runs.

## Nested conditions

```python
service_active = True
health_check_passed = False

if service_active:
    if health_check_passed:
        print("Service healthy")
    else:
        print("Investigate service")
else:
    print("Service stopped")
```

Avoid deeply nested logic when guard clauses or helper functions improve readability.

## `for` loops
A `for` loop iterates over an iterable.

```python
services = ["nginx", "sshd", "docker"]

for service in services:
    print(f"Checking {service}")
```

Use `enumerate()` when an index is needed and `range()` for integer sequences.

```python
for number, service in enumerate(services, start=1):
    print(number, service)

for attempt in range(1, 4):
    print(f"Attempt {attempt}")
```

## `while` loops
A `while` loop continues while its condition is true. Ensure the condition can eventually become false.

```python
attempt = 1
while attempt <= 3:
    print(f"Health check attempt {attempt}")
    attempt += 1
```

For real polling, include a delay and an overall timeout; avoid busy loops.

## `break`, `continue`, and `pass`
- `break` exits the nearest loop.
- `continue` skips to the next iteration.
- `pass` is a no-operation placeholder.

## Loop `else`
The `else` block runs if the loop completes normally, not if it exits with `break`.

```python
for port in [22, 80, 443]:
    if port == 443:
        print("HTTPS port found")
        break
else:
    print("HTTPS port not found")
```

## Bounded retry example

```python
import time

for attempt in range(1, 4):
    print(f"Health check attempt {attempt}")
    healthy = attempt == 3  # replace with a real check

    if healthy:
        print("Endpoint healthy")
        break

    if attempt < 3:
        time.sleep(2)
else:
    print("Health check failed")
```

Production checks also need request timeouts, exception handling, and structured logging.

## Exercises
1. Iterate through a list of Linux services.
2. Print only service names beginning with `s`.
3. Simulate a bounded health check.
4. Stop iterating when a target host is found.
5. Explain `break` versus `continue`.
