# EventBridge Scheduling

EventBridge can trigger automation on a schedule or in response to supported events. Scheduling options and service interfaces evolve; use the current AWS console or API documentation for the chosen scheduling feature.

## Common pattern
1. EventBridge schedule triggers Lambda.
2. Lambda receives a small event payload.
3. Function performs read-only inventory.
4. Results are stored in S3 or a database.
5. Metrics and logs record success/failure.

## Idempotency
A scheduled function may run more than once or overlap with a previous run. Use run IDs, conditional writes or a lock/lease where necessary. Avoid assuming exactly-once execution.

## Exercises
1. Design a daily EC2 inventory schedule.
2. Define how overlapping runs are handled.
3. Add a failure notification path.
