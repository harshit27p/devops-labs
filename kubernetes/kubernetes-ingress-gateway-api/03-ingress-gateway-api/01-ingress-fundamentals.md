# 01 — Ingress Fundamentals

## What is Ingress?

Ingress is a Kubernetes API object that describes HTTP and HTTPS routing from outside the cluster to Services. It can express host-based and path-based routing and TLS termination. It does not itself implement a proxy or create an external load balancer.

An **Ingress controller** watches Ingress resources and configures a data plane such as a reverse proxy, cloud load balancer, or edge router.

## Control plane vs data plane

- Control plane: API server stores Ingress objects; controller watches changes and reconciles configuration.
- Data plane: proxy/load balancer receives client traffic and forwards it to backend endpoints.

Creating an Ingress without a compatible controller generally has no traffic-routing effect.

## Request path

```text
Client -> DNS -> External LB / edge -> Ingress controller -> Service -> ready Pod
```

The exact hops vary by controller and deployment mode. Some controllers integrate with cloud load balancers; others run as Pods and are exposed through a Service.

## Minimal Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app
  namespace: default
spec:
  ingressClassName: example-controller
  rules:
    - host: app.example.test
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: app-service
                port:
                  number: 80
```

The `example-controller` class must correspond to a real IngressClass/controller in the cluster.

## API status

Ingress has been stable since Kubernetes v1.19. The API is frozen: it is not being removed, but Kubernetes recommends Gateway API for new functionality. Choose a maintained controller and verify its feature support.

## What Ingress does not cover

Ingress is designed for HTTP(S), not arbitrary TCP/UDP exposure. For non-HTTP protocols, use appropriate Service types or implementation-specific capabilities. Advanced routing and infrastructure delegation are better represented by Gateway API.

## References

- [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- [Ingress controllers](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/)
