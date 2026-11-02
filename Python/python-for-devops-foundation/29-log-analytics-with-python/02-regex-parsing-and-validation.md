# Regex Parsing and Validation

Regex is useful for stable, documented text formats. Prefer a structured JSON log format when you control the application.

```python
import re

ACCESS = re.compile(
    r'(?P<method>GET|POST|PUT|DELETE) '
    r'(?P<path>\S+) (?P<status>\d{3}) '
    r'(?P<duration_ms>\d+)'
)

def parse_line(line: str) -> dict | None:
    match = ACCESS.fullmatch(line.strip())
    if not match:
        return None
    data = match.groupdict()
    data["status"] = int(data["status"])
    data["duration_ms"] = int(data["duration_ms"])
    return data
```

This parser expects a deliberately simplified format, not every real Nginx/Apache log format. Test against representative fixtures.
