# 3. Composition, Inheritance, and Polymorphism

## Composition
Composition builds a component from other objects. It is often more flexible than a deep inheritance hierarchy.

```python
class Logger:
    def info(self, message):
        print(f"INFO: {message}")

class HealthCheck:
    def __init__(self, logger):
        self.logger = logger

    def run(self):
        self.logger.info("Running health check")

check = HealthCheck(Logger())
check.run()
```

`HealthCheck` has a logger; it is not a kind of logger.

## Inheritance

```python
class CloudResource:
    def __init__(self, resource_id):
        self.resource_id = resource_id

    def describe(self):
        return self.resource_id

class StorageBucket(CloudResource):
    def __init__(self, resource_id, region):
        super().__init__(resource_id)
        self.region = region
```

`super()` delegates to the parent implementation. Keep inheritance hierarchies shallow and meaningful.

## Polymorphism and protocols
Python commonly uses duck typing: if an object provides the operations a caller needs, it can often be used without sharing a base class.

```python
def publish(message, destination):
    destination.send(message)
```

Any destination object implementing `send()` can be passed in. Type hints can describe this contract using `typing.Protocol`.

## Choosing a design
- Prefer composition for interchangeable dependencies.
- Use inheritance for a genuine specialization relationship.
- Use polymorphism to keep callers independent of concrete implementations.
- Avoid tight coupling to cloud SDK objects in core business logic; small interfaces make tests easier.

## Exercise
Create a `Notifier` interface-like protocol and implement console and in-memory test notifiers. Test the same alert function with both.
