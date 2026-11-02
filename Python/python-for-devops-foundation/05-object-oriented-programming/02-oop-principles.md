# 2. OOP Principles

## Encapsulation
Encapsulation keeps related data and behavior together and provides a clear interface for changing state.

```python
class RetryCounter:
    def __init__(self, limit: int):
        if limit < 1:
            raise ValueError("limit must be positive")
        self._limit = limit
        self._count = 0

    def increment(self):
        if self._count < self._limit:
            self._count += 1

    @property
    def exhausted(self):
        return self._count >= self._limit
```

The underscore indicates internal use; it does not enforce security.

## Abstraction
Abstraction exposes what a component does while hiding implementation details. A monitoring script can call `check()` without needing to know whether the implementation checks a local process or a remote endpoint.

## Inheritance
Inheritance allows a class to extend another class. Use it when the relationship is genuinely an “is-a” relationship and shared behavior is stable.

## Polymorphism
Different classes can provide the same interface and be used interchangeably.

```python
class TextReporter:
    def report(self, message):
        return f"TEXT: {message}"

class JsonReporter:
    def report(self, message):
        return {"message": message}

def send_report(reporter, message):
    return reporter.report(message)
```

Both objects support the `report()` operation, even though their implementations differ.

## Avoid overengineering
Do not create a class for every small value or wrap every function in an object. Choose the simplest design that keeps responsibilities clear and testable.

## Exercises
Create two reporter classes with the same `report()` method. Pass each to a common reporting function and explain how polymorphism simplifies the caller.
