# 1. Python on Linux

## Interpreter and script execution

```bash
python3 --version
which python3
python3 script.py
```

A shebang allows a script to be run directly:

```python
#!/usr/bin/env python3

def main():
    print("Linux automation started")

if __name__ == "__main__":
    main()
```

Make it executable:

```bash
chmod +x script.py
./script.py
```

The shebang `#!/usr/bin/env python3` resolves Python through the current `PATH`. In managed production environments, ensure the intended interpreter and virtual environment are selected.

## Standard library modules
Useful modules for Linux automation include:
- `os`: environment variables and process-related interfaces.
- `pathlib`: filesystem paths.
- `shutil`: high-level file operations and disk usage.
- `subprocess`: execute external programs.
- `pwd` and `grp`: Unix account and group information.
- `stat`: file metadata and mode bits.
- `platform`: operating-system information.
- `logging`: application logs.

## Privileges
Run scripts as an unprivileged user whenever possible. Use `sudo` only for the specific operation that requires elevated permissions. Avoid running downloaded scripts as root.

## Exercise
Create a read-only host report showing hostname, platform, Python executable, and current working directory.
