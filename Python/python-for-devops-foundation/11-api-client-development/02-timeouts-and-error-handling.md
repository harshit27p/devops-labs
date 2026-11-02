# Timeouts and Error Handling

Always set timeouts. A tuple configures connect and read timeouts:
```python
response = requests.get(url, timeout=(3, 10))
```
This is not necessarily a total end-to-end deadline.

```python
import requests

try:
    response = requests.get(url, timeout=(3, 10))
    response.raise_for_status()
    data = response.json()
except requests.Timeout:
    print("API timed out")
except requests.HTTPError as exc:
    print(f"HTTP status: {exc.response.status_code}")
except requests.ConnectionError:
    print("Connection failed")
except requests.JSONDecodeError:
    print("Response was not valid JSON")
```

Catch expected failures narrowly. Do not log authorization headers, tokens or sensitive response bodies. Log safe context such as correlation ID, endpoint category, status code and error class.

Exercises: test unreachable endpoints, distinguish 404 from 503 and confirm logs never include secrets.
