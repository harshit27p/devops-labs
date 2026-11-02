# Runbook Automation

Automated runbooks can gather evidence and perform approved low-risk actions.

## Safe automation tiers
1. Read-only diagnostics
2. Suggested remediation plan
3. Human-approved change
4. Pre-approved reversible action with strict guardrails

## Required safeguards
- Scope and identity validation
- Dry-run mode
- Approval for consequential changes
- Timeouts and bounded retries
- Audit log and post-action verification
- Rollback or recovery instructions

Never restart or scale production services solely because a model labels an interval anomalous.
