# Lab 03 — TLS Termination

## Objective

Create a test TLS Secret and attach it to an Ingress or Gateway HTTPS listener. Choose the branch matching your installed controller.

## Create a temporary self-signed certificate

```bash
openssl req -x509 -nodes -days 7 -newkey rsa:2048 \
  -keyout tls.key -out tls.crt \
  -subj "/CN=app.example.test"
kubectl create namespace networking-lab
kubectl create secret tls app-example-tls \
  --cert=tls.crt --key=tls.key -n networking-lab
```

For production, use a trusted certificate issuer and automated renewal.

## Ingress branch

Edit `manifests/ingress-tls.yaml` to use your actual IngressClass, then:

```bash
kubectl apply -f manifests/demo-apps.yaml
kubectl apply -f manifests/ingress-tls.yaml
kubectl describe ingress secure-demo -n networking-lab
```

## Gateway API branch

Add an HTTPS listener with `tls.mode: Terminate` and `certificateRefs` pointing to the Secret. Verify route attachment and controller support before applying.

## Verify certificate

```bash
openssl s_client -connect <address>:443 -servername app.example.test
curl --resolve app.example.test:443:<address> https://app.example.test/
```

A self-signed certificate will produce a trust warning unless explicitly trusted for the test.

## Cleanup

```bash
kubectl delete namespace networking-lab
rm -f tls.key tls.crt
```
