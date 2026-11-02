# Secure Python Coding Principles

Security automation is still software. It needs clear trust boundaries, predictable failure behavior, least privilege and safe defaults.

## Core practices
- Validate data at boundaries; do not assume API, file or CLI input is trustworthy.
- Use `pathlib` and constrain paths to an approved root.
- Prefer parameterized database queries.
- Avoid `eval`, `exec`, unsafe deserialization and shell command construction.
- Do not log passwords, tokens, private keys or full authorization headers.
- Use maintained dependencies and pin/review versions.
- Make read-only behavior the default.

## Example: constrain a path

```python
from pathlib import Path

APPROVED_ROOT = Path("/var/tmp/security-lab").resolve()

def approved_path(user_value: str) -> Path:
    candidate = (APPROVED_ROOT / user_value).resolve()
    if candidate != APPROVED_ROOT and APPROVED_ROOT not in candidate.parents:
        raise ValueError("Path escapes approved directory")
    return candidate
```

The root should be configured by the operator, not supplied by an untrusted caller.

## Review questions
1. What data is trusted, and why?
2. Can input cause access outside the intended directory?
3. What happens if a dependency or API is unavailable?
4. Can logs expose secrets?
