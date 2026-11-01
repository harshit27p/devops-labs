# 10 — Vertical Pod Autoscaler (VPA)

VPA analyzes container resource usage and can recommend or adjust CPU/memory requests and limits, depending on configured mode.

## Main components
- Recommender: computes resource recommendations.
- Updater: may evict Pods to apply recommendations in supported modes.
- Admission controller: applies recommendations to newly created Pods.

VPA is an add-on and is not installed by default in many clusters. Installation and compatibility depend on Kubernetes version and distribution.

## Modes
- `Off`: recommendation only.
- `Initial`: applies recommendations at Pod creation.
- `Recreate`: may evict/recreate Pods to apply changes.
- `InPlaceOrRecreate`: where supported, attempts in-place updates and falls back to recreation.

## Example (requires VPA CRDs and components)
```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: web-demo-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-demo
  updatePolicy:
    updateMode: "Off"
```

Start with recommendation-only mode. Understand disruption and HPA interaction before enabling automatic updates. HPA and VPA should not both independently control the same CPU/memory dimension without a deliberate design.
