# 4. Processes and Subprocess

## Process information
Python's `os` module exposes the current process ID and parent process ID.

```python
import os

print("PID:", os.getpid())
print("Parent PID:", os.getppid())
```

For detailed process monitoring, a third-party library such as `psutil` is commonly used. Install it in a virtual environment and review its platform support.

## Run external commands safely
Use `subprocess.run()` with an argument list. Avoid `shell=True` when arguments may contain user-controlled data.

```python
import subprocess

result = subprocess.run(
    ["uname", "-a"],
    capture_output=True,
    text=True,
    check=True,
    timeout=5,
)
print(result.stdout)
```

`check=True` raises `CalledProcessError` for a non-zero exit code. `timeout` prevents an unbounded wait.

## Handle failures

```python
import subprocess

try:
    result = subprocess.run(
        ["systemctl", "is-active", "sshd"],
        capture_output=True,
        text=True,
        timeout=5,
    )
except FileNotFoundError:
    print("systemctl is not available")
except subprocess.TimeoutExpired:
    print("Command timed out")
else:
    print("Exit code:", result.returncode)
    print("Output:", result.stdout.strip())
```

Some systems use a different SSH service unit name. Confirm the unit on the target distribution.

## Avoid unsafe shell construction
Bad pattern:

```python
# Do not interpolate untrusted input into a shell command.
# subprocess.run(f"some-command {user_input}", shell=True)
```

Prefer:

```python
subprocess.run(["some-command", validated_argument], check=True)
```

Validate arguments against an allowlist when the command has a constrained set of valid values.

## Exercises
Run a harmless system-information command, add a timeout, handle missing executables, and explain why an argument list is safer than a shell command string.
