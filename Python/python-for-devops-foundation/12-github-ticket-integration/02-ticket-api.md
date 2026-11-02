# Ticket API Integration — Jira Cloud Pattern

Keep authentication, base URL, payload construction, timeouts and response parsing inside a small client module.

For Jira Cloud REST API v3, descriptions commonly use Atlassian Document Format (ADF), not a plain string:
```python
payload = {
    "fields": {
        "project": {"key": "OPS"},
        "summary": "Investigate disk usage",
        "issuetype": {"name": "Task"},
        "description": {
            "type": "doc",
            "version": 1,
            "content": [{
                "type": "paragraph",
                "content": [{"type": "text", "text": "Disk usage exceeded threshold."}]
            }]
        }
    }
}
```

The required fields and available issue types depend on project configuration. A 400 response may indicate invalid fields or payload schema; 401/403 usually indicates authentication or permission issues. Do not retry unchanged requests for these errors.

Exercises: separate payload construction from HTTP transport, validate summary and mock a successful response.
