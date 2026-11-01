# 07 — Headless Services and ExternalName

## Headless Service

Set `clusterIP: None` to create a headless Service. There is no Service virtual IP. DNS returns records for backing endpoints, enabling clients to discover individual Pods.

Common use cases include StatefulSet peer discovery and applications that implement their own client-side load balancing.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-peers
  namespace: networking-lab
spec:
  clusterIP: None
  selector:
    app: web
  ports:
    - name: http
      port: 80
      targetPort: 8080
```

A headless Service does not itself provide load balancing or failover. Clients must handle multiple records, stale addresses, retries, and endpoint health appropriately.

## ExternalName Service

An ExternalName Service maps a Kubernetes Service name to an external DNS name using a CNAME-style response. It does not create a proxy or allocate a ClusterIP.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: payments-db
  namespace: networking-lab
spec:
  type: ExternalName
  externalName: database.example.net
```

This can provide a stable in-cluster name for an external dependency. It does not make the external service reachable; DNS resolution, routing, firewall rules, TLS hostnames, and application configuration still matter.

## Comparison

| Feature | Headless | ExternalName |
|---|---|---|
| ClusterIP | None | None |
| DNS result | Endpoint records | CNAME-style alias |
| Backend | Selected cluster endpoints | External DNS hostname |
| Proxying | No virtual IP proxy | No proxy |
| Typical use | Stateful peer discovery | External dependency alias |

## Reference

- [Headless Services](https://kubernetes.io/docs/concepts/services-networking/service/#headless-services)
- [ExternalName](https://kubernetes.io/docs/concepts/services-networking/service/#externalname)
