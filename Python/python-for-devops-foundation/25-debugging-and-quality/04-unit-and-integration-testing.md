# Unit and Integration Testing

Unit tests isolate a function. Integration tests verify that multiple components work together.

```python
def clamp(value: int, low: int, high: int) -> int:
    return max(low, min(value, high))

def test_clamp():
    assert clamp(5, 1, 10) == 5
    assert clamp(-2, 1, 10) == 1
    assert clamp(20, 1, 10) == 10
```

## Test categories
- Happy path
- Boundary values
- Invalid input
- Permission and network failures
- Timeout behavior
- Duplicate events
- Partial or malformed reports

Tests should be deterministic and should not depend on a live production service.
