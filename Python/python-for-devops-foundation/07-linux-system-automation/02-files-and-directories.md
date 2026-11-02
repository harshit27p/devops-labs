# 2. Files and Directories

## Use `pathlib`
`pathlib.Path` provides an object-oriented interface for filesystem paths.

```python
from pathlib import Path

log_dir = Path("/var/log")
print(log_dir.exists())
print(log_dir.is_dir())
```

## List directory entries

```python
from pathlib import Path

directory = Path(".")
for entry in directory.iterdir():
    kind = "directory" if entry.is_dir() else "file"
    print(entry.name, kind)
```

`iterdir()` is not recursive. Use `rglob()` for recursive searches, but be mindful of directory size and permissions.

## Read a text file

```python
from pathlib import Path

path = Path("sample.log")
with path.open("r", encoding="utf-8") as file:
    for line_number, line in enumerate(file, start=1):
        if "ERROR" in line:
            print(line_number, line.rstrip())
```

Streaming line by line avoids loading a large file into memory.

## Create directories and files

```python
from pathlib import Path

report_dir = Path("reports")
report_dir.mkdir(parents=True, exist_ok=True)

report_path = report_dir / "summary.txt"
report_path.write_text("Automation report\n", encoding="utf-8")
```

`write_text()` replaces existing content. Use append mode when you intend to add content.

## File operations
`shutil.copy2`, `shutil.move`, and `Path.unlink` can modify or remove data. Validate paths and targets before using them. Never construct deletion targets from untrusted input without strict validation.

## Atomic replacement pattern
For important configuration updates, write a temporary file in the same filesystem and replace the target with `Path.replace()` after validation. Preserve ownership, permissions, metadata, and backups as required by the environment; atomic replacement alone does not preserve every operational property.

## Exercises
1. List files in a test directory.
2. Count lines in a sample log.
3. Find files by suffix.
4. Create a report directory and write a report.
5. Add a dry-run mode before any file deletion.
