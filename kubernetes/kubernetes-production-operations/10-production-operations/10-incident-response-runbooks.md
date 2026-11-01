# 10 — Incident Response and Runbooks

## Incident lifecycle

1. Detect and validate the signal.
2. Assess severity and user impact.
3. Assign incident lead and technical responders.
4. Stabilize service using safe, reversible actions.
5. Communicate status and next update time.
6. Recover and verify user-facing behavior.
7. Preserve evidence and write a blameless review.
8. Track corrective actions to completion.

## Triage commands

```bash
kubectl get nodes -o wide
kubectl get pods -A -o wide
kubectl get events -A --sort-by=.lastTimestamp
kubectl describe pod <pod> -n <namespace>
kubectl logs <pod> -n <namespace> --all-containers --since=30m
kubectl get deploy,rs,sts,ds,svc,pvc,pdb -n <namespace>
```

Use logs, events, metrics, traces, and recent deployment history together. Capture timestamps and avoid destructive changes before understanding the failure mode.

## Runbook template

### Alert and impact
- Alert name:
- User-visible symptom:
- Severity and affected scope:

### Diagnosis
- Dashboard and queries:
- Commands:
- Expected healthy state:
- Common causes:

### Mitigation
- Safe reversible actions:
- Actions requiring approval:
- Rollback criteria:

### Recovery validation
- User journey/smoke test:
- Metrics returned to normal:
- Data integrity check:

### Escalation and ownership
- Service owner:
- Platform escalation:
- Communications channel:

## Blameless post-incident review

Document what happened, impact, contributing conditions, detection gaps, response timeline, and prioritized follow-up actions. Focus on improving systems and safeguards rather than assigning personal blame.
