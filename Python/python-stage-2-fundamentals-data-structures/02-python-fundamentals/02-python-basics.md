# 2. Python Basics

## Statements, expressions, and indentation
A statement performs an action; an expression produces a value.

```python
cpu_percent = 72
is_busy = cpu_percent > 80
print(is_busy)
```

Python uses indentation to define blocks. Four spaces are conventional.

```python
service_running = True

if service_running:
    print("Service is running")
    print("Health check passed")
```

## Comments and docstrings
Use `#` for short comments. Use docstrings to describe modules, classes, and functions.

```python
def check_disk_usage(path):
    """Return disk usage information for a filesystem path."""
    return path
```

## Naming conventions

| Element | Convention | Example |
|---|---|---|
| Variable/function | `snake_case` | `instance_count` |
| Class | `PascalCase` | `CloudResource` |
| Constant | Uppercase | `DEFAULT_TIMEOUT` |
| Module | Lowercase | `log_parser.py` |

Names are case-sensitive.

## Imports

```python
import os
import platform
import sys

print(platform.system())
print(platform.python_version())
print(os.getcwd())
print(sys.executable)
```

Prefer explicit imports. Avoid wildcard imports because they obscure where names come from.

## Main guard

```python
def main():
    print("Starting infrastructure checks")

if __name__ == "__main__":
    main()
```

The main function runs when the file is executed directly, but not simply because another module imports it.

## Common errors
- `SyntaxError`: source code cannot be parsed.
- `IndentationError`: invalid block indentation.
- `NameError`: a name is not defined.
- `TypeError`: an operation receives an incompatible type.
- `ValueError`: a value is invalid for the requested operation.

## Exercise
Create `environment_report.py` that prints the working directory, OS name, Python version, and interpreter path using `os`, `platform`, and `sys`.
