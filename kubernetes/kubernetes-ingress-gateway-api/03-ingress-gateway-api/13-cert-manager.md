# 13 — cert-manager and Certificate Automation

## What cert-manager does

cert-manager automates certificate issuance and renewal inside Kubernetes. It integrates with certificate authorities and issuers, then stores resulting certificate/key pairs in Kubernetes Secrets.

It is an optional component, not built into Kubernetes.

## Main resources

- `Issuer`: namespace-scoped certificate issuer.
- `ClusterIssuer`: cluster-scoped issuer.
- `Certificate`: requests and manages a certificate.
- ACME challenges: prove control of a domain, commonly through HTTP-01 or DNS-01.

## HTTP-01 vs DNS-01

- HTTP-01: the CA validates a token over HTTP. Requires the challenge endpoint to be reachable and correctly routed.
- DNS-01: validation uses a DNS TXT record. Supports wildcard certificates but requires secure DNS provider credentials and automation.

## Operational safeguards

- Use least-privilege credentials for DNS automation.
- Protect private keys and issuer secrets.
- Monitor Certificate and CertificateRequest conditions.
- Plan renewal rate limits and staging environments.
- Do not commit private key material to Git.
- Verify DNS and external reachability before debugging the controller.

## Inspect

```bash
kubectl get issuer,clusterissuer
kubectl get certificate -A
kubectl describe certificate <name> -n <ns>
kubectl get certificaterequest,order,challenge -A
```

## References

- [cert-manager documentation](https://cert-manager.io/docs/)
- [ACME configuration](https://cert-manager.io/docs/configuration/acme/)
