# Lab 04 — NetworkPolicy Isolation

Prerequisite: a CNI that enforces Kubernetes NetworkPolicy.

```bash
kubectl apply -f manifests/networkpolicy-default-deny.yaml
kubectl apply -f manifests/networkpolicy-allow-dns-web.yaml
kubectl get networkpolicy -n security-lab
kubectl describe networkpolicy -n security-lab
```
Deploy test Pods with the expected labels and test allowed and denied paths. If behavior does not change, verify CNI policy enforcement and label selectors. DNS rules must match the cluster's DNS Pod labels/namespace and port configuration; adapt the example to your cluster.

Cleanup:
```bash
kubectl delete -f manifests/networkpolicy-allow-dns-web.yaml
kubectl delete -f manifests/networkpolicy-default-deny.yaml
```
