# Retries, Backoff and Timeouts

Retries can improve resilience for transient failures, but careless retries amplify outages.

## Guidelines
- Set a timeout for every network or subprocess operation.
- Retry only failures likely to be transient.
- Use exponential backoff with jitter.
- Respect `Retry-After` and service rate limits.
- Bound attempts and total elapsed time.
- Do not retry non-idempotent actions unless they use an idempotency key.

```python
import random
import time

def wait_before_retry(attempt: int, base: float = 0.5, cap: float = 20.0):
    delay = min(cap, base * (2 ** attempt))
    time.sleep(random.uniform(0, delay))
```

This helper only computes/waits for a delay; callers must still classify errors and cap the number of attempts.
