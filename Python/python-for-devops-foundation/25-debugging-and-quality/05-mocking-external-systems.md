# Mocking External Systems

Mocks replace external dependencies so tests can verify behavior without making real API calls or changing cloud resources.

```python
from unittest.mock import Mock

def get_status(client, resource_id):
    response = client.describe(resource_id)
    return response["status"]

def test_get_status():
    client = Mock()
    client.describe.return_value = {"status": "available"}
    assert get_status(client, "resource-1") == "available"
    client.describe.assert_called_once_with("resource-1")
```

For cloud automation, use mocks for fast unit tests and dedicated sandbox accounts for carefully controlled integration tests. Never point destructive tests at production.
