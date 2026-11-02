# Input Validation and Output Encoding

Validation checks whether data meets the application's expected shape and meaning. Encoding makes data safe for a particular output context.

## Validate explicitly
- Type and length
- Allowed characters or enumerated values
- Numeric ranges
- File size and file type where relevant
- Identifiers against a known format

```python
import re

HOST_LABEL = re.compile(r"^[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$")

def validate_host_label(value: str) -> str:
    if not isinstance(value, str) or not HOST_LABEL.fullmatch(value):
        raise ValueError("Invalid DNS host label")
    return value
```

Validation is context-specific: a DNS label validator is not a URL validator or a shell-escaping function.

## Output contexts
- HTML: use a template engine's auto-escaping.
- SQL: use parameterized queries.
- Shell: avoid shell interpretation; pass argument arrays.
- JSON: use `json.dump` / `json.dumps`, not string concatenation.

Never treat escaping as a substitute for validating business rules.
