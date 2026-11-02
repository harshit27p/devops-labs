# Normalized Findings and Reporting

Different scanners use different field names. A normalized model makes comparison and reporting easier.

## Suggested fields
- `source_tool`, `source_version`
- `asset`, `component`
- `finding_id`, `title`, `description`
- `severity`, `confidence`
- `evidence`, `location`
- `first_seen`, `last_seen`
- `status`, `owner`, `remediation`

## Severity mapping
Do not map severity labels blindly. Preserve the original severity and add a separate normalized severity with documented mapping rules.

## Exercise
Combine two synthetic scanner exports into a JSON report. Include a `source` object for each finding and deduplicate only when identifiers and affected components match.
