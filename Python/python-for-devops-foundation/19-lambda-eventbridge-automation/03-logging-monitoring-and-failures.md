# Lambda Logging, Monitoring and Failure Handling

## Logging
Use Python's `logging` module and emit structured context:
```python
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(
        "inventory_started",
        extra={"request_id": context.aws_request_id},
    )
```
Ensure the logging format actually serializes the fields required by your platform. Do not log credentials or full sensitive event bodies.

## Monitoring
Track invocation count, duration, errors, throttles and concurrency. Add application-level metrics for resources scanned, candidates found and actions performed.

## Failure handling
- Set timeouts based on expected workload.
- Use bounded retries and dead-letter or failure destinations where appropriate.
- Make processing idempotent.
- Alert on repeated failures.
- Provide an operator replay procedure.

## Exercises
1. Add start/end logs and elapsed time.
2. Define alarms for errors and throttles.
3. Write a runbook for a failed scheduled inventory.
