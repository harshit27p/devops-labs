# 02 — IngressClass and Controller Selection

## IngressClass

IngressClass identifies the controller intended to implement an Ingress. Its `spec.controller` field is a controller-specific identifier. An Ingress selects a class through `spec.ingressClassName`.

```yaml
apiVersion: networking.k8s.io/v1
kind: IngressClass
metadata:
  name: example-controller
spec:
  controller: example.com/ingress-controller
```

This is a structural example only. The controller string must match the actual implementation's documented value.

## Default class

A cluster may designate one IngressClass as default using the `ingressclass.kubernetes.io/is-default-class: "true"` annotation. If no class is specified on an Ingress, default-class behavior depends on cluster configuration. Explicit class selection is clearer in multi-controller clusters.

## Multiple controllers

A cluster can run multiple controllers for separate use cases, such as internal and external ingress. Use distinct classes and carefully scoped controller configuration to prevent controllers from reconciling the same resources unintentionally.

## Inspect

```bash
kubectl get ingressclass
kubectl describe ingressclass <class>
kubectl get ingress -A -o wide
kubectl describe ingress <name> -n <ns>
```

## Selection checklist

- Which controller is actively maintained?
- Does it support the Kubernetes version and required Ingress features?
- Does it support Gateway API if migration is planned?
- How is it exposed to clients?
- How are TLS certificates and secrets managed?
- How are upgrades, security patches, metrics, and logs handled?

## Reference

- [IngressClass API](https://kubernetes.io/docs/concepts/services-networking/ingress/#ingress-class)
