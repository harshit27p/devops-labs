# Bandit JSON Reports

Bandit analyzes Python source for common security issues and can emit JSON for automation.

Example command in a project you own:

```bash
bandit -r src -f json -o bandit-report.json
```

## Parse a report

```python
import json
from pathlib import Path

def load_bandit(path: Path) -> list[dict]:
    report = json.loads(path.read_text(encoding="utf-8"))
    return report.get("results", [])
```

## Report fields
Typical findings include test ID, issue text, severity, confidence, filename and line number. Preserve tool version and report metadata.

A Bandit finding is not automatically a confirmed vulnerability. Review the code context and document disposition.
