import hashlib
import hmac
from signature import verify_github_signature

def test_valid_signature():
    secret = "local-test-secret"
    body = b'{"action":"created"}'
    digest = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    assert verify_github_signature(secret, body, f"sha256={digest}")

def test_modified_body_rejected():
    secret = "local-test-secret"
    body = b'{"action":"created"}'
    digest = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    assert not verify_github_signature(secret, body + b" ", f"sha256={digest}")
