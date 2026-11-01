# 07 — Topology Spread Constraints

Topology spread constraints distribute matching Pods across failure domains such as nodes or zones.

## Key fields
- `maxSkew`: maximum permitted difference between the most- and least-populated eligible domains.
- `topologyKey`: node label defining the domain.
- `whenUnsatisfiable`: `DoNotSchedule` (hard) or `ScheduleAnyway` (soft).
- `labelSelector`: selects the Pods counted for the spread calculation.
- `minDomains`: optional minimum eligible domains, supported in modern Kubernetes versions.

## Example
```yaml
topologySpreadConstraints:
  - maxSkew: 1
    topologyKey: kubernetes.io/hostname
    whenUnsatisfiable: ScheduleAnyway
    labelSelector:
      matchLabels:
        app: web
```

## Node vs zone spreading
Use hostname to distribute replicas across nodes; use `topology.kubernetes.io/zone` for zone distribution. Ensure nodes actually carry the labels and are eligible.

## Hard vs soft
`DoNotSchedule` may leave Pods Pending when constraints cannot be met. `ScheduleAnyway` allows placement but scores nodes to improve balance.

Topology spread complements Pod anti-affinity and should be chosen based on availability requirements.
