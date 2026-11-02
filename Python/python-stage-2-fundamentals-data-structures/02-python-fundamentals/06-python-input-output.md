# 6. Python Input and Output

## Printing output

```python
service = "nginx"
state = "active"

print("Service:", service, "State:", state)
print(f"{service} is {state}")
```

F-strings provide readable interpolation and formatting.

## Interactive input
`input()` always returns a string. Convert and validate before using numeric input.

```python
raw_port = input("Enter port: ")

try:
    port = int(raw_port)
except ValueError:
    print("Port must be an integer")
else:
    if 1 <= port <= 65535:
        print(f"Valid port: {port}")
    else:
        print("Port outside valid range")
```

## Standard streams
- `sys.stdin`: standard input.
- `sys.stdout`: normal output.
- `sys.stderr`: diagnostic output.

```python
import sys

print("Normal status")
print("Warning: sample diagnostic", file=sys.stderr)
```

## Multiple lines of input
For paths containing spaces, ask for one path per line instead of splitting a line on spaces.

```python
paths = []
print("Enter paths, one per line. Blank line finishes.")

while True:
    path = input("> ").strip()
    if not path:
        break
    paths.append(path)

print(paths)
```

## Command-line arguments
`sys.argv` is suitable for simple argument access. Use `argparse` for user-friendly command-line tools.

```python
import argparse

parser = argparse.ArgumentParser(description="Check a service")
parser.add_argument("--service", required=True)
parser.add_argument(
    "--environment",
    choices=["dev", "test", "prod"],
    default="dev",
)
args = parser.parse_args()

print(f"Checking {args.service} in {args.environment}")
```

Run:

```bash
python service_check.py --service nginx --environment test
```

## Environment variables
Use environment variables for runtime configuration:

```python
import os

environment = os.getenv("APP_ENV", "development")
api_url = os.getenv("API_URL")

if not api_url:
    raise RuntimeError("API_URL is not configured")
```

Environment variables are not a complete secrets-management system. Do not print secrets, commit `.env` files, or pass sensitive tokens as command-line arguments. Prefer managed identities/IAM roles and a secrets manager for production workloads.

## Exercise
Build a CLI script accepting `--directory` and `--max-files`, validate both, and read a default environment from `APP_ENV`.
