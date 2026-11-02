# Production Readiness

Security:
- Verify webhook HMAC before trusting payload.
- Use constant-time signature comparison.
- Keep secrets in a secret manager.
- Restrict repositories, event types and payload sizes.
- Use HTTPS.

Reliability:
- Persist delivery IDs.
- Use a queue for slow work.
- Set timeouts and bounded retries.
- Avoid duplicate ticket creation after ambiguous POST failures.
- Record ticket IDs for reconciliation.

Deployment: use Flask behind Gunicorn and Nginx with TLS. Flask's development server is not a production server.

Log event IDs, repository/issue identifiers, status codes and safe failure categories. Never log secrets, authorization headers or unredacted sensitive payloads.

Exercises: write a failure runbook, add a non-sensitive health endpoint and define alert conditions.
