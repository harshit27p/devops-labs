# HMAC Webhook Signature Validation

GitHub's `X-Hub-Signature-256` is an HMAC-SHA256 digest of the raw request body, prefixed with `sha256=`.

```python
import hashlib
import hmac

def verify_signature(secret: str, body: bytes, supplied: str) -> bool:
    if not supplied.startswith("sha256="):
        return False
    digest = hmac.new(
        secret.encode("utf-8"),
        body,
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(f"sha256={digest}", supplied)
```

Verify the exact raw body bytes before parsing or re-serializing JSON. Whitespace or key-order changes alter the digest. Reject missing or malformed signatures. Store the secret outside source control.

Exercises: generate a test signature, change one byte and verify rejection.
