# Webhook Notification Safety

Webhook receivers and senders need authentication, validation and resilience.

## Receiver controls
- Verify provider signatures using the documented algorithm.
- Validate event type and source.
- Enforce request size limits.
- Make processing idempotent.
- Return promptly and process heavier work asynchronously.
- Protect secrets and redact headers from logs.

## Sender controls
- Use HTTPS and a managed secret store.
- Apply connect/read timeouts.
- Retry only appropriate failures with bounded backoff.
- Avoid leaking internal diagnostic data to external destinations.
