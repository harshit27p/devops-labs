# Data Quality and Missing Telemetry

AIOps quality depends on telemetry quality. Bad or incomplete data can create false alarms and missed incidents.

## Validate
- Missing timestamps and fields
- Duplicate records
- Clock skew and out-of-order events
- Invalid status codes or negative durations
- Sudden drops in event volume
- Parser failure rate
- Gaps in collection

A quiet log stream may mean a healthy service—or a broken log shipper. Monitor telemetry ingestion itself.
