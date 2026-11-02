# SLI, SLO and Error Budgets

- **SLI:** a measured indicator of service behavior.
- **SLO:** a target for that indicator over a defined window.
- **SLA:** an external agreement that may include remedies or commitments.

## Example
SLI: percentage of valid API requests completed successfully within 500 ms.
SLO: 99.9% over a rolling 30-day window.

An error budget is the tolerated unreliability implied by the SLO. It helps balance feature delivery and reliability work.

Define exclusions carefully. A metric that excludes too much traffic can look healthy while users experience failures.
