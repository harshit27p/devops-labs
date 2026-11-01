# 06 — Taints and Tolerations

Taints repel Pods from nodes unless a Pod has a matching toleration. Tolerations permit scheduling; they do not force a Pod onto the tainted node.

## Effects
- `NoSchedule`: new non-tolerating Pods are not scheduled.
- `PreferNoSchedule`: scheduler tries to avoid the node.
- `NoExecute`: non-tolerating Pods are evicted; tolerations may specify `tolerationSeconds`.

## Example toleration
```yaml
tolerations:
  - key: dedicated
    operator: Equal
    value: payments
    effect: NoSchedule
```

## Commands
```bash
kubectl taint nodes <node> dedicated=payments:NoSchedule
kubectl describe node <node>
kubectl taint nodes <node> dedicated=payments:NoSchedule-
```

## Common uses
- Dedicated workload pools.
- Control-plane isolation.
- Nodes with special hardware.
- Temporary node conditions such as memory or disk pressure.

Do not add broad tolerations to every workload without considering isolation and capacity. A toleration does not bypass resource, affinity, or volume constraints.
