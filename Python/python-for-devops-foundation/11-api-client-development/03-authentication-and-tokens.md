# API Authentication and Tokens

Common patterns include API keys, bearer tokens, Basic authentication, OAuth 2.0 and cloud workload identity. Follow the provider's documentation.

Bearer token:
```python
import os
import requests

token = os.environ["SERVICE_API_TOKEN"]
response = requests.get(
    "https://api.example.test/v1/status",
    headers={"Authorization": f"Bearer {token}"},
    timeout=(3, 10),
)
response.raise_for_status()
```

Some APIs support username plus token using Basic authentication:
```python
from requests.auth import HTTPBasicAuth
auth = HTTPBasicAuth(
    os.environ["TICKETING_EMAIL"],
    os.environ["TICKETING_API_TOKEN"],
)
```

Use dedicated automation identities, least-privilege scopes, short-lived credentials where possible, and separate development/production credentials. Never commit tokens.

Exercises: fail fast if a token is missing and test unauthorized/forbidden responses without printing the token.
