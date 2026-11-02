# Capstone — GitHub Issue to Ticket Automation

## Goal
Create a ticket when an authorized user posts `/jira` on an issue in an allowlisted repository.

## Requirements
- Flask receives `issue_comment` webhook events.
- Verify `X-Hub-Signature-256`.
- Require action `created`, an allowed repository and exact `/jira` command.
- Create a ticket through a REST API.
- Persist delivery IDs and ticket IDs.
- Log outcomes without exposing secrets.

## Suggested layout
```text
14-capstone-github-ticket-automation/
├── app.py
├── github_events.py
├── signature.py
├── ticket_client.py
├── event_store.py
├── requirements.txt
├── .env.example
└── tests/
```

## Environment
See `.env.example`. It contains placeholders only. Never commit a real `.env`.

## Milestones
1. Implement pure event filtering and signature verification.
2. Unit-test valid and invalid signatures.
3. Build a ticket client with explicit timeouts and status checks.
4. Build the Flask route.
5. Add persistent duplicate prevention.
6. Test against sandbox accounts.
7. Deploy behind Gunicorn/Nginx and HTTPS after review.

## Acceptance tests
- Invalid signatures rejected.
- Wrong events, repositories and ordinary comments ignored.
- Valid command creates one ticket.
- Re-delivery does not create a duplicate.
- 429/5xx errors handled with bounded retry or reconciliation.
- Logs contain event/ticket IDs but no secrets.

Stretch: queue-based processing, metrics, dead-letter queue and operator replay command.
