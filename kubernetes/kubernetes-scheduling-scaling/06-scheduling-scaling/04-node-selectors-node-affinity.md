# 04 — Node Selectors and Node Affinity

Node labels provide a way to classify nodes by hardware, zone, workload role, or policy.

## nodeSelector
A simple exact-match constraint:
```yaml
nodeSelector:
  workload: batch
```

## Node affinity
`requiredDuringSchedulingIgnoredDuringExecution` is a hard placement requirement. `preferredDuringSchedulingIgnoredDuringExecution` is a soft preference with weights.

```yaml
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
        - matchExpressions:
            - key: kubernetes.io/arch
              operator: In
              values: ["amd64"]
    preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 80
        preference:
          matchExpressions:
            - key: node-role
              operator: In
              values: ["compute"]
```

`IgnoredDuringExecution` means changing/removing a matching label after placement does not automatically evict the running Pod.

## Label nodes
```bash
kubectl label node <node> workload=batch
kubectl get nodes --show-labels
```

Use stable, governed labels. Avoid scheduling all workloads to a small subset of nodes without capacity analysis.
