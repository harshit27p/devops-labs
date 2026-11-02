# 1. Virtual Environments

## Why isolate dependencies?
Two projects may require incompatible versions of the same library. A virtual environment provides a project-specific Python interpreter context and package installation location.

## Create an environment

```bash
python -m venv .venv
```

Activate it:

```bash
# Linux/macOS
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1

# Windows Command Prompt
.venv\Scripts\activate.bat
```

Deactivate:

```bash
deactivate
```

## Verify the interpreter

```bash
python --version
python -c "import sys; print(sys.executable)"
python -m pip --version
```

Use `python -m pip` so pip belongs to the interpreter you intend to use.

## Ignore generated environment files
Add this to `.gitignore`:

```gitignore
.venv/
venv/
__pycache__/
*.py[cod]
.env
```

Do not commit a virtual environment directory. Recreate it from dependency metadata.

## Common problems
- PowerShell execution policy may block activation scripts. Follow your organization's policy; alternatively invoke the environment's Python executable directly.
- A package installed globally may not be available inside `.venv`.
- An editor or notebook may use a different interpreter than the terminal.
- Recreate a broken environment rather than manually copying it between machines.

## Exercise
Create two virtual environments with different versions of a harmless package and verify that each environment uses its own interpreter and package installation.
