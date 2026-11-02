import hashlib
import hmac

def verify_github_signature(secret: str, body: bytes, supplied: str) -> bool:
    if not supplied.startswith("sha256="):
        return False
    digest = hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(f"sha256={digest}", supplied)
