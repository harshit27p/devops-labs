# 05 — TLS with Ingress

## TLS termination

A common pattern is to terminate TLS at the ingress controller. The client establishes HTTPS to the controller; the controller forwards traffic to the backend Service, often over HTTP inside the cluster. Re-encryption to the backend is controller-specific.

## TLS Secret

Ingress TLS normally references a Secret of type `kubernetes.io/tls` containing `tls.crt` and `tls.key`. The Secret must be in the same namespace as the Ingress.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: secure-app
  namespace: networking-lab
spec:
  ingressClassName: example-controller
  tls:
    - hosts:
        - app.example.test
      secretName: app-example-tls
  rules:
    - host: app.example.test
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: demo-v1
                port:
                  number: 80
```

The class name is illustrative. Configure the actual controller.

## Create a lab self-signed certificate

```bash
openssl req -x509 -nodes -days 30 -newkey rsa:2048 \
  -keyout tls.key -out tls.crt \
  -subj "/CN=app.example.test"
kubectl create secret tls app-example-tls \
  --cert=tls.crt --key=tls.key -n networking-lab
```

Do not use a self-signed certificate for a public production service unless the trust model explicitly requires it.

## Security considerations

- Protect private keys and restrict Secret access through RBAC.
- Automate renewal and monitor expiration.
- Ensure certificate SANs match client hostnames.
- Define TLS policy and minimum versions in the controller/load balancer.
- Understand whether backend traffic is encrypted.
- Avoid committing private key material to Git.

## Reference

- [Ingress TLS](https://kubernetes.io/docs/concepts/services-networking/ingress/#tls)
