# Safe Subprocess Execution

Use `subprocess.run` with an argument list, a timeout, controlled environment and checked return status. Avoid `shell=True` for untrusted or variable input.

```python
import subprocess

def git_version() -> str:
    result = subprocess.run(
        ["git", "--version"],
        check=True,
        capture_output=True,
        text=True,
        timeout=5,
    )
    return result.stdout.strip()
```

## Operational safeguards
- Use absolute executable paths when practical.
- Validate each argument against an allowlist.
- Set a timeout and handle `TimeoutExpired`.
- Avoid passing secrets on command lines.
- Limit privileges of the process.
- Capture only the output needed; redact before logging.

Do not build commands by concatenating user input. A fixed executable and a list of validated arguments are easier to reason about.
