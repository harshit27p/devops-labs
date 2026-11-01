# 11 — SLIs, SLOs, and Error Budgets

## Definitions

- **SLI (Service Level Indicator):** a measured indicator of service behavior, such as successful request ratio or latency.
- **SLO (Service Level Objective):** a target for an SLI over a defined time window.
- **SLA (Service Level Agreement):** an external agreement, often with contractual consequences.
- **Error budget:** the permitted unreliability implied by an SLO.

Example: an availability SLO of 99.9% over 30 days permits approximately 0.1% of eligible events to fail during that window. Define eligible events and exclusions explicitly.

## Choose user-centered indicators

Good SLIs measure outcomes users care about:
- availability: successful eligible requests / total eligible requests;
- latency: proportion of eligible requests below a threshold;
- freshness: data delivered within a defined age;
- correctness: successful valid transactions / eligible transactions.

Infrastructure metrics are often diagnostic signals, not SLIs by themselves.

## Burn rate

Error-budget burn rate compares the observed error rate to the rate that would consume the budget over the SLO window. Multi-window, multi-burn-rate alerting can detect both fast severe incidents and slower sustained degradation.

A practical alert should include the SLO, affected service, evaluation window, and runbook. Do not copy burn-rate thresholds blindly; tune them to the service's traffic and response model.

## SLO lifecycle

1. Identify user journeys and service boundaries.
2. Define eligible events and measurement source.
3. Choose SLIs and windows.
4. Agree on realistic targets with stakeholders.
5. Build dashboards and burn-rate alerts.
6. Review error-budget consumption and reliability work.
7. Revisit targets when architecture or user expectations change.

## Common mistakes

- Setting 100% availability targets without a compelling reason.
- Measuring only infrastructure uptime.
- Changing the SLI definition after an incident.
- Using low-traffic ratios without minimum-volume handling.
- Treating error budgets as a punishment instead of a prioritization tool.

## Further reading

- https://sre.google/sre-book/service-level-objectives/
- https://sre.google/workbook/alerting-on-slos/
