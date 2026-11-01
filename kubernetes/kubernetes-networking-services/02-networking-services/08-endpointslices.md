# 08 — EndpointSlices

## What are EndpointSlices?

EndpointSlices represent network endpoints associated with a Service. They provide a scalable and extensible way to track backend addresses and ports. Kubernetes may split large endpoint sets across multiple slices rather than storing all endpoints in one legacy Endpoints object.

## How they are associated

A selector-based Service is associated with EndpointSlices labelled:

```text
kubernetes.io/service-name=<service-name>
```

EndpointSlice data includes address type, ports, endpoint addresses, and conditions such as readiness, serving, and terminating (depending on Kubernetes version and endpoint state).

## Inspect

```bash
kubectl get endpointslices -n <ns>
kubectl get endpointslices -n <ns> -l kubernetes.io/service-name=<service>
kubectl describe endpointslice <slice> -n <ns>
kubectl get endpointslices -n <ns> -o yaml
```

## Debugging empty endpoints

1. Confirm Service and Pod are in the same namespace.
2. Compare Service selector with Pod labels.
3. Confirm Pods are Ready.
4. Confirm the Service targetPort matches a declared/named Pod port.
5. Inspect EndpointSlice conditions and Events.
6. Check whether the Service is selectorless and endpoints are managed manually.

## Selectorless Services

A Service without a selector can be paired with manually managed EndpointSlices, useful for external or non-Pod backends. This is an advanced pattern and requires careful lifecycle management and security review.

## Reference

- [EndpointSlices](https://kubernetes.io/docs/concepts/services-networking/endpoint-slices/)
