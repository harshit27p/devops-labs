# 06 — LoadBalancer Services

## Purpose

A Service of type `LoadBalancer` asks an infrastructure integration to provision or configure an external load balancer and route traffic to the Service. On many cloud platforms this is provided by a cloud controller or a load balancer controller; on bare metal, an implementation such as MetalLB may be used.

Kubernetes does not universally create a public IP by itself. The result depends on the environment, controller, permissions, quotas, subnet configuration, and provider-specific annotations.

## Example

```yaml
apiVersion: v1
kind: Service
metadata:
  name: public-api
  namespace: networking-lab
spec:
  type: LoadBalancer
  selector:
    app: demo-web
  ports:
    - name: http
      port: 80
      targetPort: 8080
```

## Provisioning workflow

1. Apply the Service.
2. The control plane records the LoadBalancer request.
3. An infrastructure controller reconciles the request.
4. The external address is reported in `.status.loadBalancer`.
5. Traffic is forwarded to the Service backends according to provider implementation.

```bash
kubectl get svc public-api -n networking-lab -w
kubectl describe svc public-api -n networking-lab
```

## Common issues

- `EXTERNAL-IP` remains pending: no compatible controller, quota, permissions, subnet, or address pool.
- Address allocated but unreachable: firewall/security group, health check, route, target port, or backend readiness.
- Unexpected source IP: inspect traffic policy and provider dataplane.
- Cost surprises: public load balancers may incur hourly and data-processing charges.

## Production guidance

- Decide whether the load balancer should be public or internal.
- Restrict allowed source ranges where supported.
- Use TLS and application authentication.
- Understand health checks, idle timeouts, source IP behavior, and provider-specific annotations.
- Avoid creating one external load balancer per microservice when a shared HTTP gateway is appropriate.

## Reference

- [Service type LoadBalancer](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer)
