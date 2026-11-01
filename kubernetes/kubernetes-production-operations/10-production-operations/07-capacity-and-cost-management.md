# 07 — Capacity, Quotas, and Cost Management

## Capacity planning

Plan for steady-state demand, peak demand, node failure, maintenance, and autoscaler delay. Requests influence scheduling; limits constrain runtime usage. Incorrect requests can cause overcommitment or wasted capacity.

Track:
- requested vs actual CPU and memory;
- CPU throttling and memory OOM events;
- node allocatable vs requested resources;
- pending Pods and scheduling failures;
- storage capacity and IOPS/throughput;
- network bandwidth and load-balancer costs.

## ResourceQuota and LimitRange

A ResourceQuota limits aggregate resource consumption in a namespace. A LimitRange can set defaults, minimums, and maximums for individual containers or Pods.

See `../manifests/resource-quota.yaml` and `../manifests/limit-range.yaml`. Adapt quotas to the team's workload profile; arbitrary limits can prevent legitimate deployments.

## Cost controls

- right-size requests using observed usage and safe headroom;
- scale workloads to demand;
- remove abandoned load balancers, disks, and snapshots;
- define storage retention;
- label workloads for ownership and chargeback/showback;
- review network egress and cross-zone traffic;
- set budget alerts in the cloud provider.

## Autoscaling

HPA scales workload replicas based on metrics. Cluster Autoscaler or provider-native node autoscaling changes node capacity. They solve different layers and need compatible configuration. VPA can recommend or adjust resource requests, depending on mode and operational policy.

See Module 06 for detailed scheduling and autoscaling behavior.

## Avoid false savings

Reducing requests below realistic needs can increase contention and incident risk. Cost optimization should balance utilization, reliability, and service objectives.
