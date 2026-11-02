# Safe and Atomic Configuration Updates

Opening a file in write mode truncates it immediately. For important local configuration, validate the new content, write a temporary file on the same filesystem, then replace the destination.

```python
from pathlib import Path
import json
import os
import tempfile

def write_json_atomically(destination: Path, data: dict) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(
        dir=destination.parent,
        prefix=f".{destination.name}.",
        suffix=".tmp",
        text=True,
    )
    temporary = Path(name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2)
            handle.write("\\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, destination)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise
```

The example requires `import json`. Atomic replace semantics and metadata behavior vary by filesystem and platform. Replacing a file may affect permissions, ownership or ACLs; preserve these deliberately when required.

Workflow: read → parse → validate → modify narrowly → validate result → write temporary → replace → record safe audit details.

Exercises: update one JSON key without dropping others, simulate invalid input and verify the original file remains unchanged.
