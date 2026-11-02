# Explainability and Deployment

An anomaly score alone is not an incident explanation.

## Include supporting context
- Which features were unusual?
- What was the baseline range?
- How many observations were used?
- What changed around the same time?
- Was there a deployment, traffic shift or dependency event?
- Is telemetry complete?

## Deployment controls
- Version the model and feature schema.
- Monitor drift and input quality.
- Refit only through a controlled process.
- Keep a fallback threshold-based detector.
- Start in shadow mode before alerting.
- Never trigger destructive remediation solely from a model output.
