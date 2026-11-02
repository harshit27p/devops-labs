# 4. Modules and Packages

## Module
A module is a Python file that can define functions, classes, and variables.

Example layout:

```text
service_tool/
├── main.py
└── healthcheck.py
```

`healthcheck.py`:

```python
def is_healthy(status_code: int) -> bool:
    return status_code == 200
```

`main.py`:

```python
from healthcheck import is_healthy

print(is_healthy(200))
```

Run from the project directory:

```bash
python main.py
```

## Packages
A package groups related modules into a directory. A regular package commonly contains `__init__.py`.

```text
ops_tool/
├── __init__.py
├── cli.py
├── checks/
│   ├── __init__.py
│   ├── disk.py
│   └── service.py
└── reports/
    ├── __init__.py
    └── text.py
```

Imports should be consistent and avoid circular dependencies.

## Standard library, third-party, and local modules
- Standard library: included with Python, such as `pathlib`, `json`, `logging`, `subprocess`.
- Third-party: installed separately, such as `requests` or `boto3`.
- Local: code maintained in your project.

## `__name__` and the main guard

```python
def main():
    print("Run the automation")

if __name__ == "__main__":
    main()
```

This prevents the entry-point code from running merely because another module imports the file.

## Module search path
Python searches locations listed in `sys.path`. The current execution context and environment affect imports. Avoid naming project files after standard-library modules (for example, `json.py` or `logging.py`) because this can shadow the real module.

## Install third-party packages
Use the selected interpreter:

```bash
python -m pip install requests
python -m pip show requests
```

Pin project dependencies in a requirements file when appropriate. For reusable libraries, consider `pyproject.toml` and modern packaging standards.

## Exercises
Split a service health-check script into a CLI module, a checks package, and a reporting module. Verify that importing the package does not unexpectedly execute the CLI.
