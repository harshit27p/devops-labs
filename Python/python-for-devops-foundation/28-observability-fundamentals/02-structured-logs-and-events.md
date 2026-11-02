# Structured Logs and Events

Structured logs use predictable fields so systems can filter and aggregate records reliably.

## Example JSON event
```json
{
  "timestamp": "2026-11-02T10:15:30Z",
  "level": "ERROR",
  "service": "checkout-api",
  "environment": "staging",
  "event": "payment_timeout",
  "request_id": "req-example-42",
  "duration_ms": 3000
}
```

## Good practices
- Use UTC timestamps and consistent field names.
- Include service, environment, event and correlation IDs.
- Keep messages concise and machine-readable.
- Redact credentials and sensitive payloads.
- Avoid logging every request body.
- Define retention and access controls.

A log line is not a metric: do not count arbitrary text fragments as reliable service health without validating event semantics.
