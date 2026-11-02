# Controlled Plugin Discovery

Importing a Python module executes its top-level code. Therefore, plugin discovery is not passive.

## Safer pattern
- Use an explicit allowlist of approved plugin names.
- Resolve plugin files beneath a fixed plugin directory.
- Validate the expected class/interface after loading.
- Record plugin version and source.
- Catch and report load failures.
- Do not load arbitrary paths supplied by a user.

For a small application, explicit imports or a registry dictionary may be safer and simpler than scanning directories.
