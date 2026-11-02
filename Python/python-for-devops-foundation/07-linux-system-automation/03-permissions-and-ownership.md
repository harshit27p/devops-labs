# 3. Permissions and Ownership

## Linux permission model
Linux file metadata includes an owner user, owner group, and permission bits for user, group, and others.

Common permission bits:
- Read (`r`): 4
- Write (`w`): 2
- Execute (`x`): 1

For example, `755` means owner has read/write/execute and group/others have read/execute.

## Inspect permissions

```python
from pathlib import Path
import stat

path = Path("script.sh")
metadata = path.stat()

print(oct(stat.S_IMODE(metadata.st_mode)))
print(metadata.st_uid, metadata.st_gid)
```

`Path.stat()` follows symbolic links. Use `lstat()` when you need metadata about the link itself.

## Check access
`os.access()` can be useful for a preliminary check, but it is not a guarantee that a later operation will succeed. Permissions can change between checking and using a path; attempt the operation and handle `PermissionError`.

```python
import os

if os.access("sample.txt", os.R_OK):
    print("Readable according to access check")
```

## Change permissions
`Path.chmod()` changes mode bits:

```python
from pathlib import Path

Path("script.sh").chmod(0o750)
```

This changes the mode of the target path and may follow symbolic links depending on platform and API behavior. Test carefully.

## Ownership
Changing owner/group generally requires elevated privileges. Python's `os.chown()` is Unix-specific. Avoid changing ownership recursively unless the exact target tree and intended ownership are verified.

## Security principles
- Avoid world-writable files.
- Use least privilege.
- Protect private keys and secret files.
- Avoid broad recursive `chmod` commands.
- Treat symlinks and user-controlled paths carefully.

## Exercises
Inspect modes in a temporary directory, identify files readable by others, and write a report without changing permissions.
