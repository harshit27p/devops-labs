# Python Requests Library

Install:
```bash
python -m pip install requests
```

GET JSON:
```python
import requests

response = requests.get(
    "https://api.github.com/repos/OWNER/REPO",
    timeout=(3, 10),
)
response.raise_for_status()
repo = response.json()
print(repo.get("full_name"))
```

POST JSON:
```python
payload = {"title": "Investigate disk usage", "body": "Threshold exceeded"}
response = requests.post(
    "https://api.example.test/tickets",
    json=payload,
    headers={"Accept": "application/json"},
    timeout=(3, 15),
)
response.raise_for_status()
```

Use `json=` for JSON bodies. A `requests.Session` can reuse connections and share default headers, but do not attach credentials to a session used for unrelated hosts.

Exercises: fetch a repository, call a local mock endpoint and refactor repeated request logic into a small client module.
