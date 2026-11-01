# 06 — Ingress Controller Architecture

## Reconciliation

A controller watches the Kubernetes API for relevant Ingress, Service, EndpointSlice, Secret, and IngressClass changes. It translates desired state into data-plane configuration and reports status where supported.

## Typical components

- Controller Pod(s): watch API resources and render configuration.
- Proxy/data plane: accepts client connections and forwards requests.
- Service or external load balancer: makes the controller reachable.
- ConfigMap/CRDs/annotations: implementation-specific configuration.
- Metrics/logging: operational visibility.

## Controller choices

Kubernetes does not ship one universal Ingress controller. Select an actively maintained implementation, verify conformance and supported features, and review its lifecycle and security model. Examples listed by Kubernetes include cloud-provider controllers and third-party implementations such as Cilium, Contour, Traefik, and others.

The community `kubernetes/ingress-nginx` project was retired in March 2026. Its repository is archived; do not choose it for new production deployments. Existing clusters should plan a supported migration.

## Operational design

- Run multiple controller replicas where supported.
- Use disruption budgets and topology spread/anti-affinity appropriately.
- Size CPU and memory for TLS handshakes and request volume.
- Monitor 4xx/5xx, latency, connection count, reload failures, and certificate expiry.
- Review controller permissions and admission behavior.
- Keep controller configuration in version control.

## Reference

- [Ingress controllers](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/)
- [Ingress NGINX retirement](https://kubernetes.io/blog/2025/11/11/ingress-nginx-retirement/)
