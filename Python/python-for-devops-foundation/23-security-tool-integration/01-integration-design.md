# Security Tool Integration Design

A good integration separates collection, parsing, normalization, enrichment and reporting.

## Pipeline
1. Obtain an approved report artifact.
2. Validate file size and format.
3. Parse with a schema-aware parser.
4. Normalize tool-specific fields into a common finding model.
5. Preserve original evidence and tool metadata.
6. Deduplicate without discarding provenance.
7. Generate a report and remediation queue.

Never silently discard malformed records. Report parse errors and keep the original input available for audit.
