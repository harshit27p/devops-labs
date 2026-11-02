# Abstract Base Classes

An abstract base class defines a contract that concrete plugins must implement.

```python
from abc import ABC, abstractmethod

class SecurityCheck(ABC):
    name: str

    @abstractmethod
    def run(self, target: str) -> dict:
        """Return a structured, read-only assessment result."""
        raise NotImplementedError

class RuntimeVersionCheck(SecurityCheck):
    name = "runtime-version"

    def run(self, target: str) -> dict:
        import platform
        return {
            "check": self.name,
            "target": target,
            "python": platform.python_version(),
            "status": "informational",
        }
```

Use type hints and document error behavior. A plugin should not silently perform destructive actions.
