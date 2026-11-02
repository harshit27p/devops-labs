# Automation Design and Job Lifecycle

A production automation job needs a clear contract.

## Job lifecycle
1. Validate configuration and identity.
2. Check prerequisites and target scope.
3. Collect or calculate the intended changes.
4. Display a plan (dry run).
5. Obtain approval when changes are consequential.
6. Execute bounded actions.
7. Verify the outcome.
8. Emit structured results and audit metadata.

## Define the contract
Document inputs, outputs, permissions, side effects, failure modes, timeouts and ownership.

## Suggested result schema
```json
{
  "job_id": "inventory-2026-001",
  "status": "success",
  "started_at": "2026-11-02T10:00:00Z",
  "duration_seconds": 2.4,
  "items_processed": 12,
  "warnings": [],
  "errors": []
}
```

Use a generated unique ID in real jobs. Timestamps above are illustrative.
