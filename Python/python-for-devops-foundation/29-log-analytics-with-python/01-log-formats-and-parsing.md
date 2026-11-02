# Log Formats and Parsing Strategy

Common formats include plain text, syslog, JSON Lines and application-specific formats.

## Parsing workflow
1. Preserve the raw source.
2. Identify encoding and format.
3. Parse into typed fields.
4. Validate required fields.
5. Record malformed-line counts.
6. Normalize timestamps and units.
7. Keep provenance for each record.

Do not silently skip malformed records. A sudden parsing failure may indicate a format change or a collection problem rather than clean data.
