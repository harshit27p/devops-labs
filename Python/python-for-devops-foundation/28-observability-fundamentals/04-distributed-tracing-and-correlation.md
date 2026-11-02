# Distributed Tracing and Correlation

A trace represents a request journey. Each span represents an operation, such as an API call, database query or queue publish.

## Correlation
Propagate trace and request identifiers across service boundaries. Include them in logs so operators can move between a trace and related log events.

## What traces reveal
- Slow downstream dependencies
- Repeated calls
- Queueing delays
- Error propagation
- Critical path latency

Do not place secrets or personal data in trace attributes. Sampling is often required at scale; document sampling behavior because not every request may be retained.
