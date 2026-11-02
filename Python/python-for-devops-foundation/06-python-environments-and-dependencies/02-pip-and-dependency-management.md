# 2. pip and Dependency Management

## Install and inspect packages

```bash
python -m pip install requests
python -m pip show requests
python -m pip list
python -m pip freeze
```

Upgrade pip when appropriate:

```bash
python -m pip install --upgrade pip
```

## Requirements file
A simple project may record exact installed versions in `requirements.txt`:

```text
requests==2.32.3
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

The version above is an illustrative pin; choose and test a currently supported version for your project.

## Reproducibility
- Pin dependencies for repeatable deployments.
- Upgrade deliberately and run tests.
- Review dependency licenses and security advisories.
- Avoid installing packages globally on shared systems.
- Keep development-only tools separate from runtime dependencies where practical.

## `pyproject.toml`
Modern Python projects commonly declare build metadata and dependencies in `pyproject.toml`. Tooling such as pytest, Ruff, and formatters can also be configured there.

## CI pipeline example

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m compileall -q .
```

A real pipeline should run unit tests, linting, security checks, and packaging appropriate to the project.

## Exercises
Create a small project with one third-party dependency, record its version, rebuild the environment from scratch, and verify the import.
