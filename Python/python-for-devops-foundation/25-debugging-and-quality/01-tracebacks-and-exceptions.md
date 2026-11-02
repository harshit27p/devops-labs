# Tracebacks and Exception Diagnosis

A traceback shows the call path that led to an exception. Start at the final exception type/message, then trace the relevant application frames.

## Good exception handling
- Catch specific exceptions.
- Add context without hiding the original cause.
- Re-raise when the caller must decide recovery.
- Avoid empty `except` blocks.
- Do not expose secrets in exception messages.

```python
from pathlib import Path

def read_config(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise RuntimeError(f"Configuration file is missing: {path}") from exc
```
