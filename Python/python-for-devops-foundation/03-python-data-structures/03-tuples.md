# 3. Tuples

## What is a tuple?
A tuple is an ordered collection that cannot be structurally modified after creation. It is useful for fixed groups of related values.

```python
server = ("web-01", "ap-south-1", 443)
```

## Creating tuples

```python
empty = ()
single_item = ("nginx",)  # comma is required
ports = 22, 80, 443
```

## Access and unpacking

```python
hostname, region, port = server
print(hostname, region, port)
```

The number of variables must match the tuple length unless starred unpacking is used:

```python
first, *middle, last = (1, 2, 3, 4, 5)
```

## Immutability nuance
A tuple cannot have its elements reassigned, but it may contain a mutable object:

```python
record = ("web-01", ["nginx", "sshd"])
record[1].append("node-exporter")
print(record)
```

## Tuple dictionary keys
A tuple can be a dictionary key if all its elements are hashable:

```python
resource_state = {
    ("ap-south-1", "web-01"): "running"
}
```

A tuple containing a list cannot be used as a key because lists are unhashable.

## Exercises
Represent a server as a tuple, unpack it, explain the one-element comma, and test a tuple containing a list as a dictionary key.
