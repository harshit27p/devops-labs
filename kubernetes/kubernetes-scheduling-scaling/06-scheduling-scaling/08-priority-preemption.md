# 08 — Priority Classes and Preemption

Priority influences scheduling order and may allow a higher-priority Pod to preempt lower-priority Pods when no feasible node exists.

## PriorityClass
```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: critical-workload
value: 100000
globalDefault: false
description: "Priority for a critical application tier"
```

Pod reference:
```yaml
spec:
  priorityClassName: critical-workload
```

## Important behavior
- Higher priority affects queue ordering.
- Preemption may evict lower-priority Pods to make room.
- Preemption is not guaranteed: constraints, PDBs, and feasibility matter.
- A PodDisruptionBudget can influence voluntary disruptions and preemption decisions, but does not guarantee zero disruption in every scenario.
- Excessive high priorities can starve lower-priority workloads.

Use a small, governed priority hierarchy. Avoid assigning maximum priority to ordinary application Pods.
