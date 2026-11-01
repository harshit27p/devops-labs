# Lab 02 — Expose a Service with NodePort

## Objective

Expose the demo application on a node port in a lab cluster.

## Steps

```bash
kubectl apply -f manifests/demo-app.yaml
kubectl apply -f manifests/nodeport-service.yaml
kubectl get svc demo-web-nodeport -n networking-lab
kubectl get nodes -o wide
```

Find the assigned `nodePort` and test `http://<reachable-node-ip>:<nodePort>` from a network that can reach the node.

## Troubleshooting

- Confirm the NodePort exists in the Service spec.
- Confirm node firewall/security group allows the port.
- Confirm Service selector has endpoints.
- Confirm the app listens on the configured target port.
- Confirm the cluster dataplane and node routing support the path.

## Cleanup

```bash
kubectl delete namespace networking-lab
```

Do not expose a lab NodePort to the public internet.
