# Automation Run Metadata

Every run should produce enough metadata to answer: what ran, where, when, against which scope, and with what result?

## Useful fields
- Job name and version
- Run ID and correlation ID
- Start/end timestamps and duration
- Environment and target scope
- Actor or workload identity
- Items examined/changed
- Status, warnings and sanitized errors

Do not record secrets or excessive personal data. Keep audit records access-controlled and define retention.

## Exercise
Add a JSON summary to an existing read-only automation script and test both success and failure output.
