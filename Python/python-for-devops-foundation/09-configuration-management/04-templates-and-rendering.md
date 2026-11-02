# Configuration Templates and Rendering

Automation may generate Nginx virtual hosts, service definitions, monitoring targets or application settings from validated inventory data.

```python
template = """server {
    listen {port};
    server_name {hostname};
}
"""
rendered = template.format(port=8080, hostname="app.example.test")
```

Validate inserted values and escape them for the target configuration language. Do not concatenate untrusted input into shell commands.

A safe deployment workflow is: render candidate → run the application's config test → back up current file → install candidate → reload service → verify health → rollback on failure. For Nginx, `nginx -t` is commonly used to test configuration before reload.

Exercises: render a virtual host, reject hostnames containing whitespace/newlines and validate before installing.
