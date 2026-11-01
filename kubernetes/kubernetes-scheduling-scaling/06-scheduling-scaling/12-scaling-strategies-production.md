# 12 — Scaling Strategies and Production Design

## Three scaling layers
1. **Application replicas:** HPA or a workload controller.
2. **Per-Pod resources:** right-sized requests/limits; optionally VPA.
3. **Cluster capacity:** Cluster Autoscaler or another node provisioner.

## Metrics
- CPU and memory.
- Request rate, queue depth, latency, and error rate.
- Custom application metrics.
- Node utilization and pending Pods.

CPU alone may be a poor signal for I/O-bound or queue-driven workloads. Use custom/external metrics where they better represent demand.

## Avoid oscillation
- Configure HPA stabilization windows and scaling policies.
- Avoid overly aggressive scale-down.
- Ensure startup/readiness behavior prevents traffic reaching unready replicas.
- Account for warm-up, cache, connection pools, and downstream capacity.

## Capacity planning
- Requests drive scheduling and influence autoscaling.
- Limits protect nodes but overly tight CPU limits can throttle applications.
- Include DaemonSets, system reservations, disruption headroom, and failure-domain capacity.
- Set realistic min/max replicas and node group bounds.

## Production checklist
- [ ] Resource requests measured from representative load.
- [ ] Limits chosen with throttling/OOM implications understood.
- [ ] HPA metric and target reflect actual bottleneck.
- [ ] Metrics API/adapter health monitored.
- [ ] Node autoscaler integration and quotas validated.
- [ ] PDBs and topology constraints reviewed.
- [ ] Scale-up latency and warm-up tested.
- [ ] Scale-down and disruption tested.
- [ ] Alerts for Pending Pods, unschedulable Pods, OOM, throttling, and saturation.
