# REST API Concepts

REST-style APIs expose resources such as repositories, issues, users and cloud instances. URLs identify resources; methods express intended operations.

Example resource paths:
```text
GET    /repos/{owner}/{repo}/issues
POST   /repos/{owner}/{repo}/issues
GET    /issues/{issue_id}
PATCH  /issues/{issue_id}
```

Query parameters commonly support filtering, sorting and pagination:
```text
GET /instances?state=running&limit=50
```

Before automating an API, identify its base URL/version, authentication and scopes, required fields, success/error schemas, rate limits, pagination model, idempotency behavior and sandbox availability.

Exercises: design endpoints for a host inventory service and document the fields required to create a ticket.
