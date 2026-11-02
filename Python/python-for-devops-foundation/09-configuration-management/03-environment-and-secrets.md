# Environment Variables and Secret Handling

Environment variables are useful for runtime configuration but are not inherently secure. They may appear in process inspection, diagnostics, crash dumps or logs.

```python
import os

def required_env(name):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"required environment variable {name} is missing")
    return value

api_token = required_env("SERVICE_API_TOKEN")
```

Never print tokens, include them in exception messages or pass them as command-line arguments if process listings may expose them.

Prefer cloud secret managers, CI/CD secret stores, workload identity, short-lived credentials and least-privilege permissions. Add `.env` and local secret files to `.gitignore`; this does not remove secrets already committed. Revoke and rotate exposed credentials immediately.

Exercises: require a token at startup, ensure logs never include it and use a mock secret provider in tests.
