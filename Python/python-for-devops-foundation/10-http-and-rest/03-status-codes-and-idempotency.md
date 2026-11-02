# HTTP Status Codes and Idempotency

Status code groups:
- 2xx: success (`200`, `201`, `202`, `204`).
- 3xx: redirection.
- 4xx: client-side issue (`400`, `401`, `403`, `404`, `409`, `422`, `429`).
- 5xx: server-side failure (`500`, `502`, `503`, `504`).

An operation is idempotent when repeating it has the same intended effect as performing it once. GET and PUT are generally designed to be idempotent; POST often is not.

A timeout during ticket creation does not prove that the server failed to create the ticket. Blindly retrying can create duplicates. Use provider-supported idempotency keys, stable event IDs or a lookup/reconciliation strategy.

Retry transient network failures, 429 and selected 5xx responses with bounded backoff. Respect `Retry-After`. Do not retry unchanged 400/401/403/404 responses.

Exercises: classify errors, explain ambiguous POST timeouts and design a duplicate-prevention key.
