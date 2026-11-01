# 08 — High Availability and Reliability Engineering

## Failure domains

Identify failure domains at the application, Pod, node, zone, region, cluster, and external dependency levels. Replicas on the same node do not protect against node failure; replicas in one zone do not protect against zone failure.

## Availability patterns

- multiple replicas for stateless services;
- topology spread and anti-affinity for failure-domain distribution;
- PodDisruptionBudgets for voluntary disruptions;
- redundant control-plane components according to distribution design;
- resilient storage and tested restore procedures;
- redundant DNS, ingress/gateway, and external dependencies.

## Readiness and graceful termination

Readiness controls whether a Pod receives Service traffic. Graceful termination should stop accepting new work, finish or safely cancel in-flight requests, and exit within the termination grace period. See Module 01 for probe and lifecycle details.

## Reliability objectives

Use SLIs and SLOs to define user-visible reliability. Error budgets help balance feature delivery and reliability work. See Module 09 for SLO design and burn-rate alerting.

## Dependency failure

Use bounded timeouts, retries with backoff and jitter, circuit breakers, bulkheads, and queue limits where appropriate. Retries without limits can amplify an outage.

## Test failure assumptions

Perform controlled experiments in non-production first. Validate node loss, Pod eviction, dependency unavailability, zone loss assumptions, and restore procedures. Define abort criteria and ensure operators can stop the exercise.
