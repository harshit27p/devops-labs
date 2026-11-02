# Alert Rules and Severity

Define an alert using a signal, condition, evaluation window and action.

## Example rule
- Signal: 5xx request ratio
- Condition: above 3%
- Window: 10 minutes
- Minimum traffic: 100 requests
- Severity: high
- Action: notify service owner with dashboard and runbook links

## Severity model
Severity should reflect impact and urgency, not just the raw metric value. Define levels consistently across teams and document paging policy.
