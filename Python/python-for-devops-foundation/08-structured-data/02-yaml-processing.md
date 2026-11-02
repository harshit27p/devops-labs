# YAML Processing

YAML is widely used for application configuration, CI pipelines, Kubernetes manifests and automation inventories.

Install PyYAML:
```bash
python -m pip install PyYAML
```

Load untrusted or external YAML with the safe loader:
```python
from pathlib import Path
import yaml

with Path("app.yaml").open(encoding="utf-8") as handle:
    config = yaml.safe_load(handle)
```

Example:
```yaml
application:
  name: inventory-api
  port: 8080
logging:
  level: INFO
features:
  metrics: true
```

Validate after parsing:
```python
def validate_config(config):
    if not isinstance(config, dict):
        raise ValueError("top-level value must be a mapping")
    app = config.get("application")
    if not isinstance(app, dict):
        raise ValueError("application must be a mapping")
    port = app.get("port")
    if not isinstance(port, int) or not 1 <= port <= 65535:
        raise ValueError("invalid application port")
    return config
```

Use YAML for non-secret settings. Prefer secret managers or workload identity for credentials. Environment variables are not automatically secure and should not be treated as a secret vault.

Exercises: load the example, validate its port, add an environment override and write a sanitized configuration summary.
