# 23 — Security Tool Integration

Integrate approved tools using stable structured exports such as JSON and XML. This is more reliable than scraping human-formatted terminal output.

## Chapters
1. Security-tool integration design
2. Bandit JSON reports
3. Trivy JSON reports
4. Nmap XML parsing for authorized inventories
5. Normalize findings and generate reports

## Authorization
Only scan assets explicitly owned by you or covered by written authorization. Prefer importing reports produced by an approved scan process; this stage does not automate broad network scanning.
