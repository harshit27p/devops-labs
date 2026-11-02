# Entry Points and Packaging

Python package entry points provide a standard mechanism for installed packages to advertise plugins.

```python
from importlib.metadata import entry_points

def discover_checks():
    selected = entry_points(group="mytool.security_checks")
    return list(selected)
```

Discovery returns metadata objects. Loading an entry point imports and executes its plugin code, so only install trusted packages from approved sources.

## Packaging
Declare entry points in `pyproject.toml`, version the package, and test installation in a clean virtual environment. Pin dependencies and review release provenance.
