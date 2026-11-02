# 1. Introduction to Python

## What is Python?
Python is a high-level, general-purpose programming language. Its readable syntax and extensive ecosystem make it useful for scripting, automation, web services, data processing, and infrastructure tooling.

DevOps use cases include:
- Automating repetitive operational tasks.
- Calling cloud-provider APIs.
- Parsing configuration files, JSON, and logs.
- Building command-line tools and internal services.
- Connecting CI/CD workflows with external systems.
- Analyzing metrics and operational events.

Python complements Bash, Ansible, Terraform, and cloud-native services; it does not automatically replace them.

## Python and shell scripting

| Task | Often a good fit |
|---|---|
| Chain Unix commands and utilities | Shell |
| Run a few local administrative commands | Shell |
| Complex data transformations | Python |
| Consume REST APIs and process JSON | Python |
| Cross-platform automation | Often Python |
| Provision infrastructure declaratively | Terraform or another IaC tool |

Choose the simplest tool that makes the task reliable and maintainable.

## Install and verify

Use the official installer or your operating system's package manager. Avoid replacing the OS-managed Python on Linux.

```bash
python3 --version
python3 -c "print('Python is ready')"
```

Run a script with:

```bash
python3 hello.py
```

The command `python` may refer to a different interpreter depending on the OS and environment. Use the interpreter associated with your project or virtual environment.

## First program

```python
message = "Hello, DevOps!"
print(message)
```

## How Python executes code
At a high level, the interpreter parses source code, compiles it to an internal bytecode representation, and executes that bytecode using the Python virtual machine. Implementation details differ between Python implementations.

## Good habits
- Use descriptive names such as `backup_directory`.
- Use four spaces for indentation.
- Keep one responsibility per function.
- Comment on intent, not obvious syntax.
- Keep credentials out of source code.
- Test scripts with harmless sample data first.

## Exercise
Create `system_message.py` that prints a title, the Python version using `sys.version`, and a short description of an operational task.

```python
import sys
print(sys.version)
```

Further reading: [Python tutorial](https://docs.python.org/3/tutorial/) · [Python downloads](https://www.python.org/downloads/)
