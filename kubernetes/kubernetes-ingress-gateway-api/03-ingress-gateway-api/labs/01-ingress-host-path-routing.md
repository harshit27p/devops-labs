# Lab 01 — Ingress Host and Path Routing

## Prerequisite

A maintained Ingress controller is already installed and an IngressClass exists. Do not install the retired community ingress-nginx controller for a new lab. Adapt `ingressClassName` to your controller.

## Step 1 — Deploy demo applications

```bash
kubectl apply -f manifests/demo-apps.yaml
kubectl get deploy,svc -n networking-lab
```

## Step 2 — Set IngressClass

Edit `manifests/ingress-host-path.yaml` and replace `example-controller` with the class shown by:

```bash
kubectl get ingressclass
```

## Step 3 — Apply and inspect

```bash
kubectl apply -f manifests/ingress-host-path.yaml
kubectl get ingress -n networking-lab
kubectl describe ingress demo-routing -n networking-lab
```

## Step 4 — Test routing

Use the address exposed by your controller:

```bash
curl -H 'Host: app.example.test' http://<controller-address>/
curl -H 'Host: app.example.test' http://<controller-address>/api
```

If the controller has no external address, use its documented NodePort/port-forward method for the lab.

## Step 5 — Troubleshoot

Check IngressClass, controller logs, Service selectors, EndpointSlices, and host/path matching.

## Cleanup

```bash
kubectl delete namespace networking-lab
```
