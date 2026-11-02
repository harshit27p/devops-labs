# 5. System Monitoring and Logging

## Host information
The standard library can gather basic platform and filesystem information.

```python
import platform
import shutil

print("Host:", platform.node())
print("OS:", platform.platform())

usage = shutil.disk_usage("/")
used_percent = (usage.used / usage.total) * 100
print(f"Root filesystem usage: {used_percent:.1f}%")
```

This example checks the filesystem containing `/`. Production monitoring should inspect each relevant mount point and handle container or namespace boundaries.

## Structured application logging
Use the `logging` module rather than relying on scattered `print()` calls.

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

logger = logging.getLogger("host-monitor")
logger.info("Monitoring started")
logger.warning("Disk usage is above the warning threshold")
```

Levels include DEBUG, INFO, WARNING, ERROR, and CRITICAL.

## Exception logging

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    logger.exception("Calculation failed")
```

`logger.exception()` includes exception traceback information and should be called inside an exception handler.

## Monitoring is not alerting
A script that prints a metric is not a complete monitoring system. Production monitoring needs collection intervals, timestamps, labels, retention, alert routing, deduplication, and operational ownership.

## Avoid sensitive data
Do not log passwords, tokens, private keys, session cookies, or complete secret-bearing environment dumps. Sanitize untrusted log fields to reduce log injection risks.

## Exercises
Write a read-only disk usage report, log threshold warnings, and add an exception handler for a missing mount path.
