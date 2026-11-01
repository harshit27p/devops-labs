# 04 — ClusterIP Services

## Purpose

ClusterIP is the default Service type. It provides an internal virtual IP reachable from within the cluster, making it the common choice for internal microservice communication.

## Example

See [`manifests/clusterip-service.yaml`](manifests/clusterip-service.yaml). It selects Pods labelled `app: demo-web`.

## DNS name

Within the same namespace, clients can typically use the short name:

```text
demo-web
```

Across namespaces, use:

```text
demo-web.networking-lab
```

The fully qualified service DNS name is generally:

```text
demo-web.networking-lab.svc.cluster.local
```

The cluster domain may differ from `cluster.local`; inspect the cluster configuration if needed.

## Traffic path

A client sends traffic to the Service ClusterIP and port. The service dataplane chooses a backend endpoint and forwards traffic to the Pod IP and target port. Session affinity can be configured, but it is not a substitute for application session design.

## Testing

```bash
kubectl get svc demo-web -n networking-lab
kubectl get endpointslices -n networking-lab -l kubernetes.io/service-name=demo-web
kubectl run curl-client -n networking-lab --rm -it --restart=Never --image=curlimages/curl -- curl -sS http://demo-web
```

If the test image is not available or the cluster blocks image pulls, use an approved diagnostic image.

## Troubleshooting

- No endpoints: selector mismatch or no Ready Pods.
- Connection refused: process not listening on target port, wrong targetPort, or app bound only to loopback.
- Timeout: policy, routing, dataplane, or firewall issue.
- DNS resolves but connection fails: DNS is only one part of the path.

## Reference

- [Service virtual IPs and proxies](https://kubernetes.io/docs/reference/networking/virtual-ips/)
