# 14 — Interview Questions

1. Why is a container writable layer not durable storage?
2. Compare emptyDir, hostPath, and PVC-backed volumes.
3. Explain PV, PVC, and StorageClass.
4. Does Bound guarantee mount health?
5. Compare static and dynamic provisioning.
6. What does WaitForFirstConsumer solve?
7. Compare RWO, ROX, RWX, and RWOP.
8. Why does RWO not necessarily mean one Pod?
9. Compare Filesystem and Block volume modes.
10. Explain reclaim policies.
11. Describe CSI controller and node components.
12. How does PVC expansion work?
13. What prerequisites are required for snapshots?
14. How do StatefulSet volumeClaimTemplates work?
15. Why should database replicas not casually share a data directory?
16. Explain crash-consistent vs application-consistent backup.
17. Define RPO and RTO.
18. How would you troubleshoot a Pending PVC?
19. What causes Multi-Attach?
20. How would you recover a Retain-policy PV?

## Scenario prompts
- PVC Pending despite a default class: what do you inspect?
- Pod stuck with FailedMount: how do you diagnose?
- Database disk will not attach after rescheduling: what is a safe response?
- PVC deleted with Retain: how do you recover?
- Filesystem appears to have free space but writes fail: what else might be exhausted?

Strong answers explain the object/controller/driver involved, evidence to collect, safe remediation, and data-integrity risks. Do not suggest force deletion/detach as a first step.
