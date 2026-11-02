# Structured Logging and Redaction

Logs should support diagnosis without becoming a data leak.

## Include
- Timestamp and severity
- Event name
- Request/job correlation ID
- Component and operation
- Outcome and duration
- Sanitized error category

## Exclude
- Passwords, API tokens, private keys
- Full authorization headers
- Unnecessary personal data
- Entire request bodies by default

Use Python's `logging` module. Prefer structured fields or JSON formatting for centralized log systems. Redaction should happen before data leaves the process.
