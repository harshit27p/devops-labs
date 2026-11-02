# 3. Configuration and Secrets

## Configuration versus code
Configuration describes environment-specific settings such as API endpoints, region names, log levels, and feature flags. Keep these separate from application logic.

```python
import os

environment = os.getenv("APP_ENV", "development")
region = os.getenv("AWS_REGION", "ap-south-1")
log_level = os.getenv("LOG_LEVEL", "INFO")
```

## Environment variables
Set a variable for the current shell:

```bash
# Linux/macOS
export APP_ENV=testing

# PowerShell
$env:APP_ENV = "testing"
```

Environment variables are useful for runtime configuration but are not inherently secret or encrypted. They may be exposed through process inspection, diagnostics, crash reports, or misconfigured logs.

## Secrets management
For production:
- Prefer workload identity, instance profiles, or IAM roles over long-lived access keys.
- Retrieve application secrets from an approved secrets manager.
- Apply least-privilege access.
- Rotate credentials and audit access.
- Never print tokens, passwords, or private keys.
- Do not commit `.env` files or credentials to Git.

## Validate required configuration

```python
import os

def required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Required setting {name} is missing")
    return value

api_endpoint = required_env("API_ENDPOINT")
```

## Configuration files
Use a parser suited to the format:
- INI: `configparser`
- JSON: `json`
- TOML: `tomllib` (Python 3.11+ for reading)
- YAML: a maintained YAML library, with safe loading for untrusted input

Do not parse structured formats with ad-hoc string splitting if a proper parser exists.

## Exercises
Build a configuration loader that reads environment name, region, and API endpoint; validates required settings; and never prints secret values.
