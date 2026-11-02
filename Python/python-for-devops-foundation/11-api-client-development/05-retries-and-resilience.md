# Retries and Resilience

Retry only transient failures: temporary network issues, 429 and selected 5xx responses. Do not retry invalid requests or permission failures unchanged.

Exponential backoff with jitter:
`min(max_delay, base_delay * 2 ** attempt) + random_jitter`

A bounded GET example:
```python
import random
import time
import requests

def get_with_retries(url, attempts=4):
    retryable = {429, 500, 502, 503, 504}
    for attempt in range(attempts):
        try:
            response = requests.get(url, timeout=(3, 10))
            if response.status_code not in retryable:
                response.raise_for_status()
                return response
            if attempt == attempts - 1:
                response.raise_for_status()
        except (requests.Timeout, requests.ConnectionError):
            if attempt == attempts - 1:
                raise
        time.sleep(min(8, 0.5 * (2 ** attempt)) + random.uniform(0, 0.25))
    raise RuntimeError("retry loop exhausted")
```

Production clients should respect `Retry-After`, cap total waiting time and distinguish failure types. Never apply a generic retry loop to non-idempotent POST operations without duplicate protection.

Exercises: add structured attempt logs and explain why repeated ticket-create POST requests can create duplicates.
