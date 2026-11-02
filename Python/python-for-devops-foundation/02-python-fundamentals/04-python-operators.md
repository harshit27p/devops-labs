# 4. Python Operators

Operators perform arithmetic, comparisons, logical tests, and membership or identity checks.

## Arithmetic

| Operator | Meaning | Example |
|---|---|---|
| `+` | Addition | `5 + 2` → `7` |
| `-` | Subtraction | `5 - 2` → `3` |
| `*` | Multiplication | `5 * 2` → `10` |
| `/` | True division | `5 / 2` → `2.5` |
| `//` | Floor division | `5 // 2` → `2` |
| `%` | Remainder | `5 % 2` → `1` |
| `**` | Exponentiation | `5 ** 2` → `25` |

## Comparisons
`==`, `!=`, `<`, `<=`, `>`, and `>=` return Boolean values.

```python
cpu_percent = 86
if cpu_percent >= 80:
    print("CPU warning threshold exceeded")
```

`=` assigns; `==` compares.

## Logical operators
- `and`: both conditions must be true.
- `or`: at least one condition must be true.
- `not`: reverses truthiness.

```python
cpu_percent = 75
memory_percent = 88

if cpu_percent > 80 or memory_percent > 80:
    print("Resource warning")
```

`and` and `or` short-circuit evaluation.

## Assignment operators

```python
retry_count = 0
retry_count += 1
retry_count *= 2
```

## Membership

```python
allowed_regions = {"ap-south-1", "us-east-1"}
if "ap-south-1" in allowed_regions:
    print("Region allowed")
```

## Identity
`is` and `is not` test whether references point to the same object. Use `is None` for a `None` check.

## Bitwise operators
`&`, `|`, `^`, `~`, `<<`, and `>>` operate on integer bits. They are useful for flags and bit masks. Do not confuse them with logical `and` and `or`.

## Precedence
Use parentheses to make compound expressions clear:

```python
should_alert = (cpu_percent > 80) and (memory_percent > 80)
```

## Exercise
Write a condition that returns true if CPU is at least 80%, memory at least 85%, or disk usage at least 90%. Test values exactly on each boundary.
