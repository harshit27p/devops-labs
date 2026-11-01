# 11 — Kubernetes Network Troubleshooting

## Golden rule: isolate the layer

Do not assume every timeout is a CNI issue. Separate name resolution, Service selection, endpoint health, Pod listener, routing, policy, and external infrastructure.

## Layered checklist

### 1. Confirm context and namespace

```bash
kubectl config current-context
kubectl get ns
```

### 2. Inspect Pods and nodes

```bash
kubectl get pods -n <ns> -o wide
kubectl describe pod <pod> -n <ns>
kubectl get nodes -o wide
```

### 3. Inspect Service and EndpointSlices

```bash
kubectl get svc <service> -n <ns> -o yaml
kubectl get endpointslices -n <ns> -l kubernetes.io/service-name=<service> -o wide
kubectl get pods -n <ns> --show-labels
```

### 4. Verify process listener

Inside the application container or a suitable debug container:

```bash
ss -lntup
```

Check whether the application listens on `0.0.0.0` or the Pod interface rather than only `127.0.0.1`.

### 5. Test DNS and TCP separately

```bash
getent hosts <service>.<namespace>.svc
nslookup <service>.<namespace>.svc
nc -vz <service>.<namespace>.svc <port>
curl -v http://<service>.<namespace>.svc:<port>/
```

### 6. Inspect NetworkPolicy

```bash
kubectl get networkpolicy -n <ns>
kubectl describe networkpolicy <policy> -n <ns>
```

Remember that enforcement depends on the CNI.

### 7. Inspect cluster networking components

```bash
kubectl get pods -n kube-system -o wide
kubectl get daemonsets -n kube-system
kubectl get events -A --sort-by=.metadata.creationTimestamp
```

## Symptom-to-cause map

| Symptom | Likely areas |
|---|---|
| DNS name does not resolve | resolver config, CoreDNS, DNS policy, search domain |
| Service has no endpoints | selector mismatch, Pod not Ready, namespace |
| Pod IP works but Service IP fails | Service dataplane, EndpointSlice, port mapping |
| Same-node works, cross-node fails | CNI routing, tunnel, firewall, MTU |
| Small requests work, large payloads fail | MTU/path MTU, fragmentation |
| Egress blocked after policy added | missing egress rule, DNS not allowed |
| NodePort unreachable | node address, firewall, port range, service dataplane |
| LoadBalancer pending | controller, provider quota, subnet, permissions |

## Safe diagnostics

Use temporary diagnostic Pods in a lab namespace. Avoid installing tools into production containers or changing node-level networking during an incident without an approved change and rollback plan.

## References

- [Debug Services](https://kubernetes.io/docs/tasks/debug/debug-application/debug-service/)
- [DNS debugging](https://kubernetes.io/docs/tasks/administer-cluster/dns-debugging-resolution/)
