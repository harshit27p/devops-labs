# 26 — Capstone: Defensive Security Assessment Report Pipeline

## Goal
Build a Python CLI that imports approved, synthetic Bandit/Trivy/Nmap-style reports, normalizes findings and generates a reviewable assessment summary.

## Requirements
- Accept one or more local report files.
- Enforce a maximum file size and supported formats.
- Parse structured JSON/XML safely.
- Normalize findings while preserving original tool/source metadata.
- Summarize findings by severity and source.
- Extract CVE identifiers and hashes from evidence text.
- Generate JSON and Markdown reports.
- Include parser errors and unsupported report types.
- Never launch scans, exploit targets, or change infrastructure.

## Suggested structure
```text
security-assessment/
├── pyproject.toml
├── src/security_assessment/
│   ├── cli.py
│   ├── models.py
│   ├── parsers/
│   ├── normalize.py
│   ├── summarize.py
│   └── report.py
├── tests/
│   ├── test_parsers.py
│   ├── test_normalize.py
│   └── fixtures/
└── README.md
```

## Common finding model
`id`, `title`, `severity_original`, `severity_normalized`, `asset`, `component`, `cve_ids`, `evidence`, `source_tool`, `source_file`, `status`.

## Milestones
1. Define data models and input limits.
2. Implement one parser and tests.
3. Add remaining parsers using synthetic fixtures.
4. Normalize and deduplicate findings.
5. Generate JSON and Markdown outputs.
6. Add CLI exit codes and clear error messages.
7. Document limitations and safe usage.

## Acceptance criteria
- Malformed input produces a useful error, not a crash or silent success.
- A report with zero findings is distinguishable from a failed scan or empty file.
- Findings retain provenance and line/asset context.
- Tests run offline and do not contact external systems.
- Output does not include secrets or unnecessary sensitive data.

## Example CLI
```bash
python -m security_assessment   --input fixtures/bandit.json   --input fixtures/trivy.json   --output build/report
```

## Stretch goals
- Plugin interface for adding parsers.
- SARIF export.
- Policy-based severity thresholds.
- Signed report manifest.
- CI workflow that runs tests and static analysis.

## Ethical and operational boundary
Use only reports from approved assessments. This tool is a report processor, not a scanner or exploitation framework. Findings require human validation before remediation.
