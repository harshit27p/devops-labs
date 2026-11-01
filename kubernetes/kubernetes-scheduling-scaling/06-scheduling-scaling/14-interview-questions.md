# 14 — Kubernetes Scheduling & Scaling Interview Questions

1. Explain the Kubernetes scheduling workflow.
2. What is the difference between Filter and Score?
3. How do requests differ from limits?
4. Explain CPU throttling vs memory OOM kill.
5. What are Guaranteed, Burstable, and BestEffort QoS classes?
6. Compare nodeSelector and node affinity.
7. Compare Pod affinity and anti-affinity.
8. Explain taints and tolerations. Does a toleration force placement?
9. What is a topology spread constraint?
10. Explain PriorityClass and preemption.
11. How does HPA calculate CPU utilization?
12. Why are CPU requests important for CPU-based HPA?
13. Compare HPA and VPA.
14. What is Cluster Autoscaler responsible for?
15. Why might a Pending Pod not trigger node scale-up?
16. How can PDBs affect node scale-down?
17. How do you diagnose an HPA with unknown metrics?
18. How would you prevent autoscaling oscillation?

## Scenario prompts
- A Pod remains Pending with `Insufficient cpu`. How do you diagnose?
- A Pod tolerates a taint but still does not schedule. What else can block it?
- HPA is configured but replicas never increase. What do you inspect?
- HPA scales Pods but they remain Pending. What component should respond next?
- A node group will not scale down. What workload constraints might prevent it?

Strong answers separate Pod scheduling, workload scaling, and node provisioning; cite events and metrics; and explain disruption and capacity trade-offs.
