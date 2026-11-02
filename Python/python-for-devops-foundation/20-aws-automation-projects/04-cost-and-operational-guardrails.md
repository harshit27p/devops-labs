# Cost and Operational Guardrails

AWS automation can create ongoing charges or disrupt workloads. Before a lab:
- Check the pricing model and free-tier eligibility for the specific account.
- Set budgets and billing alerts.
- Use small instance types and short-lived resources.
- Tag resources with owner, purpose, environment and expiry.
- Avoid NAT gateways, load balancers, public IPv4 addresses and large storage unless needed.
- Stop or delete lab resources after verifying dependencies.
- Keep snapshots and backups according to an explicit retention policy.
- Review CloudWatch logs retention and data transfer costs.

Never assume a resource is free because the API call itself is free. Inventory scripts should be read-only and scoped to the smallest necessary region/service set.

Exercises: create a lab cost checklist and a mandatory resource-tag policy.
