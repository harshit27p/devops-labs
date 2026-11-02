# 3. Data Types and Variables

## Variables
A variable is a name bound to an object. Python is dynamically typed, so a name can later be rebound to another type. For maintainable automation, keep a variable's meaning and type consistent.

```python
resource_count = 4
region = "ap-south-1"
```

## Common built-in types

| Type | Example | DevOps use |
|---|---|---|
| `int` | `8080` | Ports and counts |
| `float` | `72.5` | CPU and latency |
| `str` | `"web-server"` | Names and paths |
| `bool` | `True` | Health flags |
| `NoneType` | `None` | Missing value |
| `list` | `["web", "db"]` | Ordered inventory |
| `tuple` | `(80, 443)` | Fixed sequence |
| `dict` | `{"region": "ap-south-1"}` | Structured data |
| `set` | `{"dev", "prod"}` | Unique values |

Use `type(value)` to inspect a value.

## Type conversion

```python
port = int("8080")
timeout = float("2.5")
```

Be careful: `bool("False")` is `True`, because the string is non-empty. Parse text booleans explicitly:

```python
def parse_bool(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"true", "yes", "1", "on"}:
        return True
    if normalized in {"false", "no", "0", "off"}:
        return False
    raise ValueError(f"Invalid boolean: {value!r}")
```

## Mutable and immutable objects
Strings, integers, and floats are immutable. Lists, dictionaries, and sets are mutable. Tuples cannot be structurally modified, though they may contain mutable objects.

```python
name = "web-01"
name = name.upper()  # creates a new string

servers = ["web-01"]
servers.append("web-02")  # modifies the list
```

## Equality and identity
`==` compares values; `is` compares object identity.

```python
first = [1, 2]
second = [1, 2]
print(first == second)  # True
print(first is second)  # False
```

Use `is None` to test for `None`. Do not use `is` to compare strings, numbers, resource IDs, or other ordinary values.

## Scope
Names created inside a function are local unless declared otherwise. Prefer passing values through parameters and returning results rather than depending on mutable global state.

```python
region = "ap-south-1"

def display_region(selected_region):
    print(f"Selected region: {selected_region}")

display_region(region)
```

## Practical example: validate a port

```python
def validate_port(value: str) -> int:
    port = int(value)
    if not 1 <= port <= 65535:
        raise ValueError("Port must be between 1 and 65535")
    return port

print(validate_port("443"))
```

## Exercises
1. Store an instance count, CPU value, and region.
2. Convert a port supplied as text.
3. Write a safe textual Boolean parser.
4. Demonstrate `==` versus `is`.
5. Explain why `bool("False")` is `True`.
