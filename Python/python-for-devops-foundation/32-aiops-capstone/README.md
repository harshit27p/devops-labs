# 32 — Capstone: AIOps Log Anomaly Detection and Incident Triage

## Goal
Build an offline Python pipeline that reads sanitized synthetic application logs, aggregates operational features, detects unusual intervals, and creates a human-reviewable incident summary.

## Requirements
- Input: CSV or JSONL logs with timestamp, service, level, event and optional duration.
- Validate schema, timestamp, severity and numeric fields.
- Aggregate INFO/WARNING/ERROR/CRITICAL counts and latency by fixed time windows.
- Establish a baseline and implement a threshold detector.
- Optionally train Isolation Forest and compare results.
- Include evidence and feature deviations for each flagged interval.
- Group related anomalies into incident candidates.
- Generate JSON and Markdown reports.
- Include tests for malformed, missing and out-of-order data.
- Run offline; do not send alerts or modify infrastructure.

## Suggested project structure
```text
aiops-log-analyzer/
├── pyproject.toml
├── data/
│   └── sample-logs.csv
├── src/aiops_analyzer/
│   ├── cli.py
│   ├── ingest.py
│   ├── validate.py
│   ├── features.py
│   ├── detectors/
│   │   ├── thresholds.py
│   │   └── isolation_forest.py
│   ├── incidents.py
│   └── reports.py
├── tests/
└── README.md
```

## Suggested feature columns
`info_count`, `warning_count`, `error_count`, `critical_count`, `request_count`, `error_rate`, `p95_latency_ms`.

## Milestones
1. Create synthetic logs with normal and injected unusual intervals.
2. Parse and validate timestamps and severity.
3. Aggregate into 5-minute windows.
4. Implement transparent threshold rules.
5. Add Isolation Forest as an optional detector.
6. Compare flags and review false positives.
7. Group adjacent flagged windows and build incident context.
8. Export JSON and Markdown.
9. Add tests and document limitations.

## Acceptance criteria
- Missing telemetry is not misreported as healthy.
- A zero-event interval is distinguished from a missing interval.
- Threshold and model outputs include evidence and time window.
- Results are reproducible with a fixed random seed.
- No automatic production remediation is performed.
- The report states that anomalies are investigation leads, not confirmed incidents.

## Example CLI
```bash
python -m aiops_analyzer   --input data/sample-logs.csv   --window 5min   --detector both   --output build/
```

## Stretch goals
- Add service-level baselines.
- Compare rolling median/MAD with Isolation Forest.
- Add deployment-event annotations.
- Export Prometheus-compatible metrics.
- Add an optional webhook adapter that only emits to a local test receiver.
