# 03 — Services Overview

## Why Services?

Pods are replaceable and their IP addresses can change. A Service provides a stable virtual address and DNS name for a logical set of backend endpoints. With selector-based Services, labels identify the Pods that should receive traffic.

## Core fields

```yaml
apiVersion: v1
kind: Service
metadata:
  name: api
spec:
  type: ClusterIP
  selector:
    app: api
  ports:
    - name: http
      port: 80
      targetPort: 8080
      protocol: TCP
```

- `port`: Service port.
- `targetPort`: destination port on selected endpoints; can be numeric or a named Pod port.
- `protocol`: TCP, UDP, or SCTP where supported.
- `selector`: labels matched against Pods.
- `type`: exposure behavior.

## Service types

| Type | Purpose |
|---|---|
| ClusterIP | Internal virtual IP; default |
| NodePort | Exposes a port on each eligible node |
| LoadBalancer | Requests an external load balancer integration |
| ExternalName | DNS CNAME-style alias to an external DNS name |

Headless Services (`clusterIP: None`) omit the virtual IP and provide DNS records for endpoint discovery.

## Selector and endpoints

A Service selector is matched against Pod labels. Kubernetes publishes backend addresses through EndpointSlices. If a Service has no endpoints, check selector labels, Pod readiness, namespace, and port configuration.

## Named ports

A Pod can declare a named port and a Service can use that name as `targetPort`. This can make backend port changes easier to manage, provided the Pod template and Service agree.

## Commands

```bash
kubectl get svc -n <ns>
kubectl describe svc <service> -n <ns>
kubectl get endpointslices -n <ns> -l kubernetes.io/service-name=<service>
kubectl get pods -n <ns> --show-labels
```

## Reference

- [Service](https://kubernetes.io/docs/concepts/services-networking/service/)
