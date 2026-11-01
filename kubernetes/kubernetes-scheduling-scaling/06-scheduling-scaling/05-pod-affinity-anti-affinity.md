# 05 — Pod Affinity and Anti-Affinity

Pod affinity places a Pod near other Pods matching a label selector within a topology domain. Anti-affinity prefers or requires separation.

## Topology key
`topologyKey` identifies the domain, such as:
- `kubernetes.io/hostname` for per-node placement.
- `topology.kubernetes.io/zone` for zone-level placement.

## Example
```yaml
affinity:
  podAntiAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        podAffinityTerm:
          topologyKey: kubernetes.io/hostname
          labelSelector:
            matchLabels:
              app: frontend
```

This prefers spreading matching Pods across nodes. Required anti-affinity can make Pods Pending if the cluster lacks enough eligible topology domains.

## Design guidance
- Prefer topology spread constraints for many general replica-spreading use cases.
- Use affinity when co-location is beneficial, such as tightly coupled components.
- Use anti-affinity for failure-domain separation.
- Consider scheduler cost and selector scope in large clusters.

## Debug
Check label selectors, topology labels, taints, available resources, and events when placement rules prevent scheduling.
