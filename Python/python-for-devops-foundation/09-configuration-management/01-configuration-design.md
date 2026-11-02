# Configuration Design for Automation

Keep environment-specific values out of source code. Typical settings include API base URLs, regions, retry limits, inventory paths and log levels.

A useful precedence is:
1. Safe built-in defaults.
2. YAML configuration for non-secret settings.
3. Environment variables for deployment-specific overrides.
4. Secret manager or workload identity for credentials.

```python
import os

raw_timeout = os.getenv("API_TIMEOUT", "10")
try:
    timeout = int(raw_timeout)
except ValueError as exc:
    raise SystemExit("API_TIMEOUT must be an integer") from exc

if timeout <= 0:
    raise SystemExit("API_TIMEOUT must be positive")
```

Environment values are strings; convert and validate them explicitly. Fail fast before network calls or infrastructure changes. Avoid dangerous defaults in production.

Exercises: create defaults for an inventory tool, override region and timeout, reject invalid values and add a safe-by-default dry-run setting.
