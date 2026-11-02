# Pagination and Rate Limits

Large collections are split into pages. Common schemes include page/per-page, offset/limit, cursor tokens and `Link` headers.

Page-based example:
```python
import requests

def list_items(url, token):
    results = []
    for page in range(1, 101):  # hard safety cap
        response = requests.get(
            url,
            params={"per_page": 100, "page": page},
            headers={"Authorization": f"Bearer {token}"},
            timeout=(3, 15),
        )
        response.raise_for_status()
        items = response.json()
        if not items:
            break
        results.extend(items)
    return results
```
Adapt to the provider's documented pagination model and maximum page size.

Respect rate-limit headers and `Retry-After`; avoid unnecessary polling, cache suitable data and request only required fields. Validate next-page URLs against the expected trusted host.

Exercises: fetch all pages, enforce a maximum page count and handle a simulated 429.
