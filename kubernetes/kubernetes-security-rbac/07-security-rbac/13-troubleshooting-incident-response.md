# 13 — Security Troubleshooting and Incident Response

## RBAC Forbidden
```bash
kubectl auth whoami
kubectl auth can-i get pods -n <namespace>
kubectl auth can-i --list -n <namespace>
kubectl get role,rolebinding -n <namespace>
kubectl get clusterrole,clusterrolebinding
```
Check identity, group mapping, namespace, API group, resource, verb, and subresource. Do not solve every Forbidden error by granting `cluster-admin`.

## Pod rejected by Pod Security
Inspect namespace Pod Security labels and admission warning/error. Identify the violated field (privileged, host namespace, runAsNonRoot, capabilities, seccomp, hostPath, etc.) and harden the workload rather than weakening namespace policy broadly.

## NetworkPolicy blocks traffic
Check selected Pod labels, namespace selectors, ingress/egress direction, DNS allowances, ports, and CNI enforcement. Test from both source and destination contexts.

## Image pull/security policy failure
Check image name/digest, registry reachability, credentials, signature policy, and admission webhook health. Do not bypass signature enforcement as a routine fix.

## Incident response sequence
1. Confirm scope and severity.
2. Preserve audit/runtime evidence.
3. Contain compromised credentials and workloads.
4. Rotate/revoke tokens and external credentials.
5. Remove persistence and close exploited access paths.
6. Rebuild from trusted images and declarative configuration.
7. Validate integrity and restore service.
8. Review root cause and improve controls.

Use your organization's incident process. Do not destroy evidence or expose credentials while troubleshooting.
