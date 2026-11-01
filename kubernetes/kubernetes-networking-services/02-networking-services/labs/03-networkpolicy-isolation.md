# Lab 03 — NetworkPolicy Isolation

## Objective

Observe default-deny behavior and allow only selected traffic. Requires a CNI that enforces Kubernetes NetworkPolicy.

## Step 1 — Apply demo app

```bash
kubectl apply -f manifests/demo-app.yaml
kubectl apply -f manifests/clusterip-service.yaml
```

## Step 2 — Test baseline connectivity

```bash
kubectl run client --namespace networking-lab --rm -it --restart=Never --image=curlimages/curl -- curl -m 5 -v http://demo-web
```

## Step 3 — Apply default deny

```bash
kubectl apply -f manifests/networkpolicy-default-deny.yaml
```

Repeat the test. Depending on your CNI and policy implementation, the connection should be denied or time out.

## Step 4 — Apply allow policy

```bash
kubectl apply -f manifests/networkpolicy-allow-dns-and-web.yaml
```

The example requires a source Pod labelled `access=allowed`. Create one:

```bash
kubectl run allowed-client -n networking-lab --image=curlimages/curl --labels=access=allowed -- sleep 3600
kubectl exec -n networking-lab allowed-client -- curl -m 5 -v http://demo-web
```

## Step 5 — Verify denied source

Create a client without the label and test again. Compare results.

## Cleanup

```bash
kubectl delete namespace networking-lab
```

If your cluster's CNI does not enforce NetworkPolicy, this lab cannot demonstrate traffic isolation.
