# 2. Function Arguments and Return Values

## Positional and keyword arguments

```python
def describe_instance(name, region):
    return f"{name} in {region}"

print(describe_instance("web-01", "ap-south-1"))
print(describe_instance(region="ap-south-1", name="web-01"))
```

Keyword arguments make calls easier to read when a function has several parameters.

## Default arguments

```python
def connect(host, port=22, timeout=5):
    return {"host": host, "port": port, "timeout": timeout}
```

Avoid mutable default values such as `items=[]`. That list would be shared between calls.

```python
def add_target(target, targets=None):
    if targets is None:
        targets = []
    targets.append(target)
    return targets
```

## Variable-length arguments: `*args` and `**kwargs`

```python
def print_targets(*hosts):
    for host in hosts:
        print(host)

def show_config(**settings):
    for key, value in settings.items():
        print(f"{key}={value}")

print_targets("web-01", "db-01")
show_config(region="ap-south-1", environment="test")
```

`*args` collects extra positional arguments into a tuple. `**kwargs` collects extra keyword arguments into a dictionary.

## Unpacking arguments

```python
connection = ("web-01", 22)
options = {"timeout": 10}

# connect_host must accept these values
# connect_host(*connection, **options)
```

## Return multiple values
Python returns one object; comma-separated return values are packed into a tuple.

```python
def parse_resource(text):
    name, state = text.split(",")
    return name, state

resource_name, resource_state = parse_resource("web-01,running")
```

## Exceptions versus return codes
Use exceptions for exceptional failures or invalid operations. Use explicit return values for expected outcomes, such as a check returning `True` or `False`. Document the contract.

## Exercises
Create a reusable retry helper that accepts a function and a maximum attempt count. Add validation for invalid attempt counts and avoid silently swallowing exceptions.
