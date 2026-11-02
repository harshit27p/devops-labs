# 1. Classes and Objects

## Class and object
A class defines a type; an object is an instance of that class. Attributes store state and methods define behavior.

```python
class Server:
    def __init__(self, hostname: str, region: str):
        self.hostname = hostname
        self.region = region

    def describe(self) -> str:
        return f"{self.hostname} is in {self.region}"

web = Server("web-01", "ap-south-1")
print(web.describe())
```

`self` refers to the current instance. `__init__` initializes a newly created instance.

## Instance and class attributes

```python
class Service:
    platform = "Linux"  # class attribute

    def __init__(self, name):
        self.name = name  # instance attribute
```

Use class attributes for values genuinely shared by all instances. Mutable class attributes can accidentally be shared across instances.

## Encapsulation by convention
Python uses naming conventions rather than strict private access:
- `name`: public.
- `_name`: internal-use convention.
- `__name`: name-mangled attribute, not a security boundary.

## Properties

```python
class Port:
    def __init__(self, value: int):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if not 1 <= new_value <= 65535:
            raise ValueError("Invalid TCP/UDP port")
        self._value = new_value
```

Properties allow validation while keeping attribute-style access.

## Dataclasses
For classes primarily storing data, `dataclasses` can reduce boilerplate.

```python
from dataclasses import dataclass

@dataclass
class Instance:
    instance_id: str
    region: str
    state: str = "unknown"
```

## Exercises
Model a Linux service with a name, port, and state. Add validation and methods to start, stop, and describe the model without executing real system commands.
