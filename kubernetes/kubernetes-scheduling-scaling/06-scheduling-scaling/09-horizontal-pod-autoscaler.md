# 09 — Horizontal Pod Autoscaler (HPA)

HPA adjusts a workload's desired replica count based on observed metrics such as CPU, memory, or custom/external metrics.

## Architecture
HPA controller periodically reads metrics and updates the target scale subresource. Metrics commonly come from Metrics Server for resource metrics or an adapter for custom/external metrics.

## CPU utilization
CPU utilization is calculated relative to the relevant resource requests. CPU requests should therefore be defined for containers when using CPU utilization targets.

Example:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-demo
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 60
```

## Inspect
```bash
kubectl get hpa
kubectl describe hpa web-hpa
kubectl top pods
kubectl get apiservices | grep metrics
```

## Behavior and stabilization
HPA supports scaling behavior policies, stabilization windows, and rate limits. Tune them to prevent flapping and protect downstream dependencies. HPA changes replicas; it does not create nodes.
