# 12 — Production Validation and Game Days

## Why validate?

A design document does not prove that recovery, failover, alerts, or operational procedures work. Controlled drills reveal gaps before a real incident.

## Validation categories

- deployment and rollback;
- node drain and replacement;
- Pod and node failure;
- storage restore and database recovery;
- DNS and ingress failure;
- metrics/logging/alert delivery;
- credential rotation;
- cluster upgrade;
- regional failover where designed.

## Game-day process

1. Define hypothesis and measurable success criteria.
2. Select a safe environment and limit blast radius.
3. Notify stakeholders and establish a stop condition.
4. Capture baseline health and telemetry.
5. Introduce one controlled failure.
6. Observe detection, response, and recovery.
7. Stop or roll back the experiment if safety criteria are breached.
8. Record findings and assign corrective actions.

## Example exercise: node loss assumption

- Confirm at least two healthy replicas across separate nodes.
- Confirm disruption policy and spare capacity.
- In a lab, make one worker unavailable using the environment's approved method.
- Observe scheduling, readiness, traffic, and alerting.
- Restore the node and verify cluster health.

Do not terminate production nodes or manipulate cloud infrastructure without explicit authorization and an approved change plan.

## Success measures

Measure detection time, mitigation time, recovery time, data loss, user impact, and whether runbooks were sufficient. Repeat drills after major architecture changes.
