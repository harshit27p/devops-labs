# 7. Regular Expressions

## What are regular expressions?
Regular expressions (regex) describe text patterns. Python's `re` module can search, match, extract, split, and replace text.

Use a proper parser when a standard structured format is available; regex is useful for semi-structured text such as selected log lines.

## Common symbols

| Pattern | Meaning |
|---|---|
| `.` | Any character except newline by default |
| `\\d` | Digit |
| `\\w` | Word character |
| `\\s` | Whitespace |
| `+` | One or more |
| `*` | Zero or more |
| `?` | Zero or one |
| `{n}` | Exactly n repetitions |
| `^` | Start of string/line depending on flags |
| `$` | End of string/line depending on flags |
| `[abc]` | One character from the set |
| `(...)` | Capturing group |

Use raw strings such as `r"\\d+"` to avoid confusion with Python string escapes.

## Search and match

```python
import re

message = "ERROR: database connection timed out"
if re.search(r"ERROR", message):
    print("Error entry found")
```

`re.match()` checks from the start of the string; `re.search()` scans for a match anywhere.

## Named extraction groups

```python
import re

line = "client=192.0.2.15 status=503 latency=1.42"
pattern = (
    r"client=(?P<ip>\\d{1,3}(?:\\.\\d{1,3}){3}) "
    r"status=(?P<status>\\d{3}) "
    r"latency=(?P<latency>\\d+\\.\\d+)"
)

match = re.search(pattern, line)
if match:
    print(match.groupdict())
```

This extracts an IPv4-shaped string but does not validate octet ranges. Use `ipaddress.ip_address()` for actual IP validation.

## Find and replace

```python
ports = re.findall(r"\\b\\d{2,5}\\b", "Ports: 22, 80, 443, 8080")
print(ports)

safe_text = re.sub(
    r"token=[^\\s]+",
    "token=[REDACTED]",
    "request token=abc123 accepted",
)
print(safe_text)
```

Prevent secrets from entering logs in the first place; redaction patterns alone are not a complete security control.

## Compile repeated patterns

```python
pattern = re.compile(r"\\bERROR\\b", re.IGNORECASE)

for line in ["INFO started", "error connection failed"]:
    if pattern.search(line):
        print("Error:", line)
```

## Exercises
Extract HTTP status codes, find ERROR/CRITICAL lines, extract timestamps, redact a sample token, and validate extracted IP addresses with `ipaddress`.
