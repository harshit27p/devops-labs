# 3. Functional Programming

Functional programming emphasizes transforming input data into output values, using functions as first-class objects and limiting unnecessary shared state.

## Pure functions
A pure function returns the same result for the same inputs and does not change external state.

```python
def normalize_service_name(name: str) -> str:
    return name.strip().lower()
```

Pure functions are easy to test because they do not depend on the machine, network, clock, or external services.

## Functions as values

```python
def is_healthy(status_code: int) -> bool:
    return status_code == 200

def evaluate(check, value):
    return check(value)

print(evaluate(is_healthy, 200))
```

This pattern is useful when a monitoring tool supports configurable checks.

## `lambda`
A lambda is a small anonymous function. Use it for short expressions, not complex business logic.

```python
instances = [
    {"name": "web-02", "cpu": 65},
    {"name": "web-01", "cpu": 91},
]

sorted_instances = sorted(instances, key=lambda item: item["cpu"])
```

## `map()` and `filter()`

```python
services = ["nginx", "sshd", "docker"]

upper_names = list(map(str.upper, services))
long_names = list(filter(lambda name: len(name) > 4, services))
```

Comprehensions are often clearer:

```python
upper_names = [name.upper() for name in services]
long_names = [name for name in services if len(name) > 4]
```

## `any()` and `all()`

```python
cpu_values = [45, 67, 91]
has_high_cpu = any(value > 85 for value in cpu_values)
all_valid = all(0 <= value <= 100 for value in cpu_values)
```

These are useful for threshold and validation checks.

## Avoid side effects in transformations
Keep data transformation separate from actions such as writing files, sending alerts, or deleting cloud resources. This separation makes it easier to test the decision logic before enabling operational actions.

## Exercises
1. Normalize a list of service names using a pure function.
2. Sort instance dictionaries by CPU usage.
3. Use `any()` to detect a threshold breach.
4. Rewrite a `map()` expression as a comprehension and compare readability.
