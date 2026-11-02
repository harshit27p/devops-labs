# 5. Sets

## What is a set?
A set is a mutable collection of unique, hashable elements. It does not support positional indexing.

```python
regions = {"ap-south-1", "us-east-1", "ap-south-1"}
print(regions)  # duplicate removed
```

Create an empty set with `set()`, not `{}` (an empty dictionary).

## Common operations

```python
regions.add("eu-west-1")
regions.discard("us-east-1")  # safe if absent
```

`remove()` raises `KeyError` if the value is absent; `discard()` does not.

## Set algebra

```python
required = {"nginx", "sshd", "node-exporter"}
installed = {"nginx", "sshd", "docker"}

print(required & installed)  # intersection
print(required - installed)  # required but missing
print(installed - required)  # unexpected
print(required | installed)  # union
```

## DevOps example: configuration comparison

```python
desired = {"nginx", "sshd", "node-exporter"}
actual = {"nginx", "sshd", "docker"}

missing = desired - actual
unexpected = actual - desired

print("Missing:", sorted(missing))
print("Unexpected:", sorted(unexpected))
```

A real configuration-management check must also consider service state, package versions, host scope, and approved exceptions.

## Membership
Set membership is typically efficient compared with scanning a list, though actual performance depends on workload and data.

## Exercises
Remove duplicate hostnames, find required-but-missing services, compare environment inventories, and explain `remove()` versus `discard()`.
