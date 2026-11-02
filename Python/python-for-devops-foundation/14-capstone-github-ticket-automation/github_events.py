def should_create_ticket(event_name: str, payload: dict,
                         allowed_repository: str) -> bool:
    if event_name != "issue_comment" or payload.get("action") != "created":
        return False
    repository = payload.get("repository") or {}
    if repository.get("full_name") != allowed_repository:
        return False
    issue = payload.get("issue") or {}
    if "pull_request" in issue:
        return False
    comment = payload.get("comment") or {}
    body = comment.get("body", "")
    return isinstance(body, str) and body.strip() == "/jira"
