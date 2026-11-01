# Kubernetes Workloads — Interview Questions

## Fundamentals

1. What is a Pod, and why is it the smallest deployable unit?
2. Why are Pods considered ephemeral?
3. What resources do containers in the same Pod share?
4. When would you use multiple containers in one Pod?
5. What is the difference between a Pod phase and a container state?

## Controllers

6. Explain the reconciliation loop of a ReplicaSet.
7. Why is a Deployment generally preferred over a standalone ReplicaSet?
8. Explain `maxSurge` and `maxUnavailable`.
9. Compare RollingUpdate and Recreate strategies.
10. What is a Deployment revision, and how does rollback work?
11. When should you choose StatefulSet over Deployment?
12. What is a headless Service used for with StatefulSets?
13. What does a DaemonSet guarantee, and what can prevent scheduling on a node?
14. Compare a DaemonSet with a static Pod.

## Batch workloads

15. Compare Job and CronJob.
16. Explain `completions`, `parallelism`, and `backoffLimit`.
17. What does `concurrencyPolicy: Forbid` do?
18. Why should batch jobs be idempotent?
19. How would you prevent a scheduled task from running indefinitely?

## Health and lifecycle

20. Compare startup, readiness, and liveness probes.
21. What happens to Service traffic when readiness fails?
22. Why can checking a database in a liveness probe be harmful?
23. Explain `CrashLoopBackOff`.
24. What happens during graceful Pod termination?
25. What is the difference between a container restart and Pod replacement?

## Scenario questions

26. A Deployment has 3 desired replicas but only 2 Pods are Ready. How do you investigate?
27. A rollout is stuck. Which commands and Events do you inspect?
28. A Pod is repeatedly OOMKilled. What evidence do you collect and what changes might help?
29. A CronJob overlaps with its previous execution. How do you prevent that?
30. A database Pod is rescheduled and must reconnect to its original data. Which workload/storage concepts are relevant?

## Practical command set

```bash
kubectl get deploy,rs,sts,ds,job,cronjob,pods -A
kubectl describe deployment <name> -n <ns>
kubectl rollout status deployment/<name> -n <ns>
kubectl rollout history deployment/<name> -n <ns>
kubectl rollout undo deployment/<name> -n <ns>
kubectl get pods -n <ns> -o wide
kubectl describe pod <pod> -n <ns>
kubectl logs <pod> -n <ns> --previous
kubectl get events -n <ns> --sort-by=.metadata.creationTimestamp
```
