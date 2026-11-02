# File Integrity and Hashing

Cryptographic hashes provide a compact fingerprint of file content. They can help compare artifacts, detect unexpected changes and verify downloads against a trusted published digest.

```python
import hashlib
from pathlib import Path

def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
```

## Important distinctions
- A hash detects differences; it does not prove who created a file.
- A checksum is useful only when the expected checksum comes from a trusted channel.
- Use digital signatures when publisher authenticity matters.
- Do not use MD5 or SHA-1 for new security-sensitive integrity designs.

## Exercise
Hash two sample files, modify one byte, and compare the results. Record the algorithm and source of the expected digest.
