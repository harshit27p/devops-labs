# Event Processing and Idempotency

Recommended stages:
1. Verify signature.
2. Validate event type and payload shape.
3. Check action and allowlists.
4. Check delivery ID.
5. Persist or enqueue event.
6. Process business logic.
7. Persist outcome.

Use a database unique constraint on provider delivery ID to protect against concurrent duplicate deliveries. Track states such as received, processing, succeeded and failed. Define safe retry and reconciliation behavior.

Do not mark an event completed before the downstream operation succeeds. Distinguish accepted-for-processing (202) from completed.

Exercises: design a webhook-delivery table, explain check-then-insert races and define a safe replay procedure.
