# 5. Decorators and Generators

## Decorators
A decorator wraps a function to add behavior without rewriting the function's core logic. Common uses include logging, timing, authorization checks, retries, and instrumentation.

```python
from functools import wraps
import time

def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        started = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - started
            print(f"{func.__name__} took {elapsed:.4f}s")
    return wrapper

@measure_time
def process_inventory():
    return sum(range(100_000))

process_inventory()
```

`@wraps` preserves useful metadata such as the original function name and docstring.

Decorators should not hide important operational behavior. Document retries, permissions, and side effects clearly.

## Decorators with arguments
A configurable decorator requires an outer function that accepts configuration, returns a decorator, and then wraps the target function. Keep the implementation simple and test its behavior.

## Generators
A generator yields values lazily instead of constructing an entire result in memory.

```python
def read_error_lines(path):
    with open(path, encoding="utf-8") as file:
        for line in file:
            if "ERROR" in line:
                yield line.rstrip("\n")

for error in read_error_lines("application.log"):
    print(error)
```

This is useful for processing large log files one line at a time.

## Generator expressions

```python
values = (number * number for number in range(1_000_000))
first_five = [next(values) for _ in range(5)]
```

A generator is usually consumed as it is iterated. It is not a reusable list.

## Iterators
An iterable can produce an iterator. An iterator provides values one at a time and remembers its current position. `for` loops manage iterator creation and exhaustion for you.

## When to use
- Use decorators for consistent cross-cutting behavior.
- Use generators for streaming or large datasets.
- Avoid decorators that make debugging or control flow surprising.
- Do not read an entire large log file into memory if line-by-line processing is sufficient.

## Exercises
Add a timing decorator to a harmless function. Build a generator that yields warning and error lines from a sample log file. Compare memory and readability with loading all lines into a list.
