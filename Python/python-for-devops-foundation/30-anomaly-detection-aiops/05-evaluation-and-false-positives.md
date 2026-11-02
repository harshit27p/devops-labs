# Model Evaluation and False Positives

Unsupervised models can be difficult to evaluate when labels are unavailable.

## Evaluation options
- Review a sample of flagged intervals with operators.
- Use known incident windows where available.
- Measure precision among reviewed alerts.
- Track missed incidents (false negatives).
- Compare against a simple baseline rule.
- Evaluate by service and operating period.

## Operational metrics
- Alert precision
- Detection delay
- False alerts per service/day
- Missed known incidents
- Percentage of anomalies with actionable context

Do not optimize only for a low alert count; that can hide important incidents.
