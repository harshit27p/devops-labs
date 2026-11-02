# GitHub API Integration

Use cases include listing issues, reading comments, applying labels, creating issues and generating repository reports.

```python
import os
import requests

def get_open_issues(owner, repo):
    response = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}/issues",
        params={"state": "open", "per_page": 100},
        headers={
            "Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
            "Accept": "application/vnd.github+json",
        },
        timeout=(3, 15),
    )
    response.raise_for_status()
    items = response.json()
    return [item for item in items if "pull_request" not in item]
```

Issue-list endpoints may also return pull requests; filter them when the workflow needs issues only. Prefer fine-grained tokens or GitHub Apps with minimum required repository permissions.

Exercises: list issues from a test repository, filter pull requests and export a sanitized summary.
