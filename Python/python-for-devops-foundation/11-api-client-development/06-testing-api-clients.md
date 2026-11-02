# Testing API Clients

Test URL, method, query parameters, headers, payload shape, timeouts, response parsing, error handling, pagination and retry limits.

Use mocks for unit tests so they do not depend on a live provider:
```python
from unittest.mock import Mock, patch

@patch("requests.get")
def test_repository_lookup(mock_get):
    fake = Mock()
    fake.status_code = 200
    fake.json.return_value = {"full_name": "team/demo"}
    mock_get.return_value = fake
    # Call the function under test, then assert its result and timeout.
```

For integration tests, use sandbox accounts and test projects. Keep destructive actions away from production.

Exercises: mock 200 and 404 responses, verify timeout configuration and test malformed JSON.
