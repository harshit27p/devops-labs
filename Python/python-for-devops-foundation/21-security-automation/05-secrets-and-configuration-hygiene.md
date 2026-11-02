# Secrets and Configuration Hygiene

Environment variables are convenient configuration inputs, but they are not a secure secret vault. They may be exposed through process inspection, crash dumps, diagnostics or accidental logging.

## Preferred patterns
- Use cloud workload identity / IAM roles instead of long-lived access keys.
- Use a managed secret store for application secrets.
- Grant the smallest possible secret access scope.
- Rotate credentials and audit access.
- Keep `.env` files out of version control; use `.gitignore`.
- Redact secrets from exceptions, logs and support bundles.

```python
import os

def required_setting(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Required setting {name} is missing")
    return value
```

This checks presence only; it does not make the value secret or validate its authorization.
