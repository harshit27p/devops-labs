# Alert Quality and Signal Selection

An alert should prompt a meaningful action. Not every unusual measurement deserves a page.

## Good alert characteristics
- User or business impact is plausible.
- Threshold and evaluation window are documented.
- Alert has an owner and runbook.
- Notification includes evidence and affected scope.
- Duplicate notifications are suppressed.
- Recovery is detected and closure is clear.

## Prefer symptoms
Alert on user-visible error rate or sustained latency before paging on a low-level CPU fluctuation alone. Infrastructure signals remain useful for diagnosis.

Review noisy alerts and tune them; alert fatigue is an operational risk.
