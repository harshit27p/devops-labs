# Day 06 — Amazon Route 53: DNS, Hosted Zones, Records, and Health Checks

> **Series:** AWS DevOps Zero to Hero  
> **Instructor:** Abhishek Veeramalla  
> **Video:** [Watch the Route 53 session](https://www.youtube.com/watch?v=6BoTfTtNsGU&list=PLdpzxOOAlwvIc1TjTwopNSjRJkzES2ZXk&index=60)  
> **Curriculum reference:** [aws-devops-zero-to-hero](https://github.com/iam-veeramalla/aws-devops-zero-to-hero)  
> **Focus:** DNS fundamentals, Route 53, domain registration, hosted zones, DNS records, routing policies, health checks, and public/private DNS architecture.

These notes expand the provided video outline with practical examples and operational guidance. The focus is DNS and traffic steering; VPC routing, Security Groups, and NACLs are covered in earlier lessons and are referenced rather than repeated in full.

---

## Contents

- [1. Learning objectives](#1-learning-objectives)
- [2. What is DNS?](#2-what-is-dns)
- [3. How DNS resolution works](#3-how-dns-resolution-works)
- [4. What is Amazon Route 53?](#4-what-is-amazon-route-53)
- [5. Domain registration and DNS hosting](#5-domain-registration-and-dns-hosting)
- [6. Hosted zones: public and private](#6-hosted-zones-public-and-private)
- [7. DNS record types](#7-dns-record-types)
- [8. Alias records and CNAME records](#8-alias-records-and-cname-records)
- [9. Route 53 routing policies](#9-route-53-routing-policies)
- [10. Health checks and failover](#10-health-checks-and-failover)
- [11. Hands-on lab: point a domain to an application](#11-hands-on-lab-point-a-domain-to-an-application)
- [12. Private DNS for internal applications](#12-private-dns-for-internal-applications)
- [13. DNS troubleshooting](#13-dns-troubleshooting)
- [14. Security, availability, and cost](#14-security-availability-and-cost)
- [15. AWS CLI and DNS commands](#15-aws-cli-and-dns-commands)
- [16. Assignment](#16-assignment)
- [17. Interview questions](#17-interview-questions)
- [18. Further reading](#18-further-reading)

---

## 1. Learning objectives

After completing this lesson, you should be able to:

1. Explain DNS and the difference between a domain name and an IP address.
2. Trace a typical DNS lookup from a client to an authoritative nameserver.
3. Describe Route 53's role as a managed DNS service and domain registrar.
4. Distinguish domain registration, hosted zones, and DNS records.
5. Explain A, AAAA, CNAME, MX, TXT, NS, and SRV records.
6. Understand Route 53 alias records and when they differ from CNAME records.
7. Compare common Route 53 routing policies.
8. Explain health checks, DNS failover, TTL, and caching limitations.
9. Configure public DNS for an application endpoint.
10. Troubleshoot common DNS configuration and resolution failures.

### Prerequisites

- Basic networking and IP address knowledge.
- Familiarity with EC2, VPC, subnets, and load balancers.
- A registered domain is optional for the hands-on lab; some tests can use a temporary DNS name or local resolution tools.
- AWS account permissions for Route 53, if creating resources.
- Awareness that domain registration, hosted zones, queries, and health checks may incur charges.

---

## 2. What is DNS?

The **Domain Name System (DNS)** is a distributed naming system that maps domain names to information such as IP addresses and mail servers.

Humans find names such as `example.com` easier to remember than numeric IP addresses. DNS lets a client ask for the information associated with a name, then connect to the returned destination.

### Common terms

- **Domain name:** A human-readable name, such as `example.com`.
- **DNS resolver:** A service that looks up DNS answers for a client.
- **Authoritative nameserver:** A server that provides authoritative records for a DNS zone.
- **DNS record:** A record defining data for a name, such as an IPv4 address or mail server.
- **TTL (Time to Live):** The time a DNS answer may be cached by resolvers.
- **Zone:** An administrative portion of the DNS namespace containing records.
- **Registrar:** An organization through which a domain name is registered.

DNS does not host the website itself. It helps clients discover where the website or service is reachable. Web traffic then uses protocols such as HTTP or HTTPS to connect to that endpoint.

### Why DNS matters in cloud environments

- Public endpoints can change during deployments or scaling.
- Load balancers provide stable DNS names that can front changing backend targets.
- Private DNS supports internal service discovery.
- Routing policies can steer users toward different endpoints.
- Health checks can inform DNS failover decisions in supported configurations.

DNS-based routing is not the same as packet-level load balancing. Resolver caching and TTLs mean that changes may not affect all clients immediately.

---

## 3. How DNS resolution works

A simplified recursive DNS lookup:

```text
Browser / application
        |
        | Query: www.example.com
        v
Configured recursive resolver
        |
        | If answer is not cached:
        v
Root DNS servers
        |
        v
TLD nameservers (e.g. .com)
        |
        v
Authoritative nameservers for example.com
        |
        v
DNS record / answer
        |
        v
Resolver returns answer to client
        |
        v
Client connects to the returned endpoint
```

In normal operation, the client usually queries a recursive resolver rather than directly querying every level. The recursive resolver follows referrals as needed and caches answers according to their TTLs.

### Example

Suppose `app.example.com` has an A record or alias that ultimately resolves to an application endpoint. The resolver returns address information, and the browser then attempts an HTTPS connection to that endpoint.

The DNS lookup can succeed while the application is still unavailable. DNS resolution and network/application connectivity must be tested separately.

### DNS caching and TTL

If a record has a TTL of 300 seconds, caching resolvers may retain that answer for up to five minutes. Changing the authoritative record does not instantly erase existing cached answers. Some clients and resolvers may also apply their own caching behavior.

For migrations, lower TTLs ahead of a planned change when appropriate, allow old cached answers to expire, then update the record and monitor both old and new paths.

---

## 4. What is Amazon Route 53?

**Amazon Route 53** is AWS's scalable, highly available DNS web service. It supports DNS hosting, domain registration for supported TLDs, health checking, and routing policies.

Route 53 can answer DNS queries for public domains and, through private hosted zones, names used within associated VPCs and connected DNS environments.

### Route 53 capabilities

- Host public DNS zones.
- Host private DNS zones for internal applications.
- Register and manage eligible domain names.
- Create records pointing to IP addresses, domain names, and AWS endpoints.
- Use routing policies to answer queries according to configured rules.
- Use health checks with supported routing configurations to help steer traffic away from unhealthy endpoints.
- Integrate with AWS services such as Elastic Load Balancing and CloudFront.

Route 53 is not a replacement for VPC route tables, Security Groups, or load balancers. It answers DNS queries; other services route packets and serve application traffic.

---

## 5. Domain registration and DNS hosting

These are related but separate tasks.

### Domain registration

Registration reserves the right to use a domain name under the relevant registry and registrar terms. Registration does not automatically create a working website or guarantee that DNS records are correct.

### DNS hosting

DNS hosting stores and serves the DNS records for a domain. A domain can be registered with one registrar while its DNS is hosted by another provider.

### Nameserver delegation

When a public hosted zone is created in Route 53, Route 53 assigns a set of authoritative nameservers. For the public internet to use that hosted zone, the domain's delegation must point to the correct authoritative nameservers at the registrar/parent zone.

If the domain is registered elsewhere, update the registrar's nameserver settings to the Route 53 nameservers for the intended hosted zone. Copy the nameservers exactly.

### Typical setup sequence

1. Register a domain or use an existing domain.
2. Create a public hosted zone for the exact domain.
3. Record the Route 53 authoritative nameservers.
4. Configure the registrar/parent delegation to use those nameservers.
5. Create the required records.
6. Validate delegation and resolution from an external resolver.
7. Configure the application endpoint and HTTPS certificate separately.

Do not create multiple public hosted zones for the same domain without a deliberate migration plan. A record created in a hosted zone that is not delegated from the registrar may not be used by public resolvers.

---

## 6. Hosted zones: public and private

A **hosted zone** is a container for DNS records associated with a domain or subdomain.

### Public hosted zone

A public hosted zone contains records intended to be resolvable through public DNS. It is used for internet-facing websites, public APIs, mail records, and other publicly discoverable names.

Examples:
- `example.com`
- `www.example.com`
- `api.example.com`

The record itself does not make the target reachable; the target's routing, network controls, and application must also work.

### Private hosted zone

A private hosted zone provides DNS resolution within associated VPCs and supported connected DNS environments. It is commonly used for internal services that should not be exposed through public DNS.

Examples:
- `db.internal.example.com`
- `api.corp.example.com`
- `service.dev.example.com`

A private hosted zone requires correct VPC association and DNS settings. Hybrid networks may need Route 53 Resolver endpoints and forwarding rules to resolve names between on-premises networks and VPCs.

### Public vs. private hosted zone

| Feature | Public hosted zone | Private hosted zone |
|---|---|---|
| Intended audience | Public DNS resolvers | Associated VPCs and configured connected networks |
| Typical purpose | Public website/API/email records | Internal service discovery |
| Delegation | Requires correct public DNS delegation | Uses VPC association and private resolver behavior |
| Public discoverability | Records can be publicly resolvable | Not published as public authoritative records |
| Security note | DNS visibility does not equal application access | Private DNS alone does not replace network security |

---

## 7. DNS record types

| Record | Purpose | Example |
|---|---|---|
| A | Maps a name to an IPv4 address | `app.example.com → 192.0.2.10` |
| AAAA | Maps a name to an IPv6 address | `app.example.com → 2001:db8::10` |
| CNAME | Aliases one DNS name to another DNS name | `www.example.com → app.example.net` |
| MX | Specifies mail servers for a domain | `example.com → mail.example.com` with priority |
| TXT | Stores text data used for verification and policies | Domain verification, SPF policy |
| NS | Identifies authoritative nameservers for a zone/delegation | Nameservers for `example.com` |
| SOA | Provides zone authority and serial/timing metadata | Zone apex metadata |
| SRV | Identifies service targets and ports | Service discovery for supported protocols |
| PTR | Used for reverse DNS lookups | Address-to-name mapping |

The IP addresses in the examples are documentation examples, not real service endpoints.

### A and AAAA records

Use A for IPv4 and AAAA for IPv6. A record can point directly to a static public IP, but this may be operationally brittle if the endpoint changes. For AWS resources such as supported load balancers, a Route 53 alias record is often a better option.

### CNAME records

A CNAME maps one DNS name to another DNS name. Under DNS rules, a CNAME generally cannot coexist with other record data at the same name, so it is not used at the zone apex in the ordinary way.

### MX and TXT records

MX records direct email delivery to mail servers. TXT records are used for domain verification and policies such as SPF, DKIM-related values, and DMARC. Email security records must be created according to the mail provider's exact instructions.

---

## 8. Alias records and CNAME records

Route 53 supports **alias records**, an AWS-specific capability that lets a DNS record point to supported AWS resources and certain other targets. Alias records are commonly used for root/apex domains and AWS endpoints.

### Alias vs. CNAME

| Feature | Route 53 alias | CNAME |
|---|---|---|
| Points to | Supported AWS resources or eligible DNS targets | Another DNS name |
| Zone apex | Can be used at the zone apex for supported targets | Ordinary CNAME is generally not allowed at the zone apex |
| Query billing | Alias queries to many AWS resources have special Route 53 pricing treatment; verify current pricing | Standard DNS query pricing applies under the applicable plan |
| AWS resource awareness | Can track supported AWS target endpoint changes | Refers to a DNS name |
| Use case | Root domain or subdomain pointing to supported AWS endpoints | Alias a subdomain to another DNS name |

### Common pattern: domain to load balancer

```text
example.com
    |
    | Route 53 alias record
    v
Application Load Balancer DNS name
    |
    v
Load balancer target group
    |
    v
Application instances
```

The load balancer distributes application traffic. Route 53 resolves the name to the load balancer endpoint. These are separate layers of the request path.

---

## 9. Route 53 routing policies

Routing policies determine which answer Route 53 returns for a DNS query. They do not replace the routing inside the VPC or the load balancer's request distribution.

| Policy | What it does | Typical use |
|---|---|---|
| Simple | Returns a simple configured answer | Basic website or endpoint |
| Weighted | Splits responses across records using configured weights | Gradual rollout or traffic experiments |
| Latency-based | Returns an endpoint associated with lower measured network latency for the user/resolver context | Multi-Region applications |
| Failover | Returns primary or secondary answers based on health configuration | Active/passive disaster recovery |
| Geolocation | Routes based on the geographic location of the DNS query source | Region- or country-specific content |
| Geoproximity | Routes based on geographic distance and optional bias | Adjusting geographic traffic distribution |
| IP-based | Routes according to client IP CIDR lists | Network-specific steering |
| Multivalue answer | Returns multiple healthy records where applicable | Simple DNS-level distribution and health-aware answers |

Actual availability and behavior depend on record type, target, policy configuration, and health-check setup. Consult current Route 53 documentation before using a policy for a production requirement.

### Weighted routing example

A deployment might send a smaller proportion of DNS responses to a new endpoint and the rest to an existing endpoint. Weighted DNS is not a precise per-request load balancer: caching and resolver behavior affect the actual distribution.

### Latency-based routing

Route 53 uses AWS latency measurements to choose an appropriate configured Region/endpoint for a DNS query. This does not guarantee the application is healthy unless health checks and routing behavior are configured appropriately.

### Failover routing

A primary record can be paired with a secondary record. Health-check state may influence which answer Route 53 returns. DNS caching means clients may continue using a previously returned endpoint until cached answers expire.

---

## 10. Health checks and failover

Route 53 health checks can monitor supported endpoints or evaluate other health-check signals. When associated with routing policies that support health-based decisions, they can help Route 53 stop returning an unhealthy endpoint and direct new DNS answers to another endpoint.

### Types of health monitoring

Depending on the setup, health checks can monitor:
- An endpoint over HTTP, HTTPS, or TCP.
- A specified path and expected response behavior for HTTP/HTTPS checks.
- The status of other health checks through calculated health checks.
- CloudWatch alarm state for supported health-check configurations.

### Important limitations

- A health check is only as meaningful as the endpoint and success criteria it tests.
- A TCP check can show that a port accepts connections without proving the application is functioning correctly.
- A health check may originate from external checkers; endpoint security controls must permit the configured check traffic where required.
- DNS failover is not instantaneous for every client because answers can be cached.
- Route 53 health checks do not automatically repair the application, replace an EC2 instance, or fix a failed database.

### Design a useful health endpoint

For an application, use a health endpoint that reflects the intended readiness condition. A very shallow endpoint might report success while the database or a critical dependency is unavailable; an overly strict endpoint might mark all instances unhealthy during a transient dependency issue. Choose the check based on the failure mode you want to detect.

---

## 11. Hands-on lab: point a domain to an application

### Objective

Create a public hosted zone and DNS record for an application endpoint. Use an AWS load balancer where available, or a suitable public endpoint for a disposable lab.

### Before you begin

- A registered domain, or an existing domain whose DNS you are authorized to manage.
- A working public endpoint, preferably an Application Load Balancer for a production-style pattern.
- An AWS account with Route 53 permissions.
- Awareness of Route 53 hosted-zone, domain-registration, health-check, and DNS query pricing.

If you do not own a domain, you can still practice DNS lookups and hosted-zone concepts without changing public production DNS. Do not attempt to control or modify a domain you do not own.

### Step 1 — Create a public hosted zone

1. Open the Route 53 console.
2. Select Hosted zones → Create hosted zone.
3. Enter the exact domain name, such as `example.com`.
4. Choose **Public hosted zone**.
5. Create the hosted zone.
6. Record the assigned NS records and SOA record.

Use a domain you control, not the example domain in this guide.

### Step 2 — Configure nameserver delegation

If the domain is registered with Route 53, check the domain's name server settings. If it is registered elsewhere, open the registrar's DNS/nameserver settings and set the authoritative nameservers to the NS values assigned to the new Route 53 hosted zone.

Copy the entire NS set exactly. A mismatch means public resolvers may continue querying another DNS provider.

### Step 3 — Create the application record

**Preferred AWS pattern:** If you have an Application Load Balancer, create an A record with Alias enabled and select the load balancer target. Add an AAAA alias only if IPv6 is configured and supported for the endpoint.

For a fixed public IPv4 endpoint, an A record can be used when appropriate, but avoid hard-coding an address that may change unexpectedly.

For a subdomain pointing to another DNS hostname, a CNAME may be appropriate.

### Step 4 — Test resolution

Use DNS tools from your workstation:

```bash
# Query the default resolver
nslookup app.YOUR_DOMAIN

# Query A records with dig (Linux/macOS; install dnsutils/bind-utils if needed)
dig app.YOUR_DOMAIN A

# Query authoritative nameservers
dig YOUR_DOMAIN NS

# Query a specific recursive resolver
dig @1.1.1.1 app.YOUR_DOMAIN A
```

Replace `YOUR_DOMAIN` with a domain you control. Not all systems have `dig` installed; `nslookup` is widely available.

### Step 5 — Test the application separately

```bash
curl -I https://app.YOUR_DOMAIN
```

A successful DNS response does not prove HTTPS is correctly configured. The load balancer or web server must have a valid certificate, listener, routing rules, healthy targets, and network permissions.

### Step 6 — Plan record changes

Before changing a production record:
1. Record the current values.
2. Understand the current TTL and cached-answer behavior.
3. Reduce TTL in advance if appropriate.
4. Make the change during an approved window.
5. Verify from multiple resolvers.
6. Monitor application health and be prepared to restore the old record.

### Cleanup

Delete lab records and hosted zones only after confirming they are not used by a real application. Removing a hosted zone or changing delegation can break DNS for every service using that zone. Domain registration and hosted-zone resources are separate.

---

## 12. Private DNS for internal applications

Private hosted zones support internal naming without publishing the records in public DNS.

### Example architecture

```text
Corporate workstation
       |
       | VPN / Direct Connect / configured resolver path
       v
Connected network
       |
       v
VPC DNS resolution
       |
       v
Private hosted zone
       |
       +--> api.internal.example.com
       |
       +--> db.internal.example.com
```

This is a conceptual design. Hybrid DNS requires the appropriate VPC associations, Route 53 Resolver endpoints and rules where needed, and network connectivity.

### Common uses

- Internal application endpoints.
- Service discovery across private application tiers.
- Private API names.
- Development, staging, and production naming separation.
- Hybrid cloud and on-premises DNS integration.

A private DNS name does not grant network access. Security Groups, routes, application authentication, and other controls still apply.

---

## 13. DNS troubleshooting

### Domain does not resolve

Check:
- Is the domain registered and active?
- Does the parent/registrar delegation point to the correct Route 53 nameservers?
- Is the record in the hosted zone that is actually authoritative?
- Does the record name match the intended FQDN?
- Are you querying public DNS or a private hosted zone?
- Could cached answers or negative caching affect the result?

### Domain resolves to the wrong endpoint

Check:
- A, AAAA, CNAME, and alias records for conflicts or unexpected values.
- Whether multiple hosted zones exist for the same domain.
- The current NS delegation.
- TTL and resolver caches.
- Weighted, latency, failover, geolocation, or other routing policy configuration.

### DNS works but the website is unavailable

DNS may be functioning correctly while the network or application is broken. Check:
- The endpoint's public/private reachability.
- Route tables, Security Groups, and NACLs.
- Load balancer listeners and target health.
- Application service status and logs.
- TLS certificate validity and hostname match.
- The correct protocol and port.

### Useful commands

```bash
# Query common record types
dig YOUR_DOMAIN A
dig YOUR_DOMAIN AAAA
dig YOUR_DOMAIN CNAME
dig YOUR_DOMAIN MX
dig YOUR_DOMAIN TXT
dig YOUR_DOMAIN NS

# Trace delegation path (if dig supports +trace)
dig +trace YOUR_DOMAIN

# Check HTTPS separately
curl -Iv https://YOUR_DOMAIN
```

`dig +trace` can help inspect public DNS delegation, but private hosted-zone resolution follows a different path. Redact internal hostnames and sensitive infrastructure details before sharing diagnostic output publicly.

---

## 14. Security, availability, and cost

### Security

- Use least-privilege IAM permissions for Route 53 changes.
- Protect domain registrar accounts with MFA and strong account recovery controls.
- Restrict who can edit NS, MX, TXT, and application records.
- Validate DNS changes before applying them to production.
- Use DNSSEC where supported and appropriate, with careful key and delegation management.
- Remember that DNSSEC provides data authenticity/integrity validation; it does not encrypt DNS queries.
- Avoid publishing private infrastructure details in public records unless required.

### Availability

- Use supported multi-Region or multi-AZ application architecture for the actual service.
- Pair health checks with routing policies only where the failure behavior is understood.
- Keep health checks representative of service readiness.
- Account for DNS TTLs and client-side caching in failover planning.
- Test failover and recovery procedures instead of assuming they work.

### Cost

Potential charges include:
- Public hosted zones.
- DNS queries according to the applicable pricing model.
- Health checks and optional monitoring integrations.
- Domain registration and renewal.
- Resolver endpoints and related networking resources for private/hybrid DNS.
- The application endpoint itself, such as load balancers and EC2 resources.

Verify current Route 53 pricing before implementing a lab or production setup. Delete only resources that are no longer needed.

---

## 15. AWS CLI and DNS commands

These AWS CLI commands require suitable permissions and a configured Region/account. They are primarily for inspection.

```bash
# Verify the AWS identity
aws sts get-caller-identity

# List hosted zones
aws route53 list-hosted-zones

# List records in a hosted zone
aws route53 list-resource-record-sets \
  --hosted-zone-id ZONE_ID

# List Route 53 health checks
aws route53 list-health-checks

# List registered domains (where permitted)
aws route53domains list-domains
```

Replace `ZONE_ID` with the actual hosted-zone ID. Route 53's global nature means its API behavior is not identical to Region-scoped EC2 operations.

### DNS command quick reference

| Command | Purpose |
|---|---|
| `nslookup name` | Basic DNS lookup |
| `dig name A` | Query IPv4 records |
| `dig name AAAA` | Query IPv6 records |
| `dig name NS` | Query nameserver records |
| `dig name MX` | Query mail-server records |
| `dig +trace name` | Inspect public delegation chain |
| `curl -Iv https://name` | Test HTTPS/TLS and HTTP connectivity after DNS resolution |

---

## 16. Assignment

### Task A — DNS fundamentals

1. Explain the difference between a domain, registrar, hosted zone, authoritative nameserver, and DNS record.
2. Draw the recursive DNS resolution process.
3. Explain why DNS resolution can succeed while a website is unavailable.
4. Explain TTL and how it affects DNS migrations.

### Task B — Route 53 records

1. Create a test public hosted zone for a domain you control.
2. Identify its NS and SOA records.
3. Create a suitable record for an application endpoint.
4. Verify resolution using `dig` or `nslookup`.
5. Document whether the endpoint is an IP record, alias, or CNAME and why.

### Task C — Routing policies

Compare simple, weighted, latency-based, failover, geolocation, and multivalue answer routing. Provide one suitable use case and one limitation for each.

### Task D — Health checks

Design a health-check strategy for a multi-Region web application. Explain what the check measures, what it cannot guarantee, how failover is configured, and why DNS caching delays full convergence.

### Task E — Private DNS

Draw a design for an internal application using a private hosted zone. Explain VPC association, hybrid DNS requirements, and why private DNS is not a replacement for network security.

### Evidence for GitHub

Include a DNS flow diagram, sanitized record examples, terminal lookup output, a brief explanation of routing policy choices, and cleanup notes. Never publish credentials, domain account recovery information, or sensitive internal records.

---

## 17. Interview questions

**1. What is DNS?**  
A distributed naming system that resolves domain names to records such as IP addresses and mail servers.

**2. What is Amazon Route 53?**  
AWS's managed DNS service that supports public and private hosted zones, domain registration for supported TLDs, health checks, and routing policies.

**3. What is a hosted zone?**  
A container for DNS records associated with a domain or subdomain.

**4. What is the difference between a public and private hosted zone?**  
Public zones serve public DNS records; private zones resolve names within associated VPCs and configured connected networks.

**5. What is the purpose of an NS record?**  
It identifies authoritative nameservers for a DNS zone or delegation.

**6. What is TTL?**  
The time a DNS answer can be cached by a resolver before it should query again.

**7. What is the difference between A and AAAA records?**  
A maps a name to IPv4; AAAA maps a name to IPv6.

**8. What is the difference between an alias and a CNAME in Route 53?**  
An alias can point to supported AWS resources and can be used at the zone apex for supported targets; a CNAME maps a name to another DNS name and is generally not used at the zone apex.

**9. Does Route 53 replace a load balancer?**  
No. Route 53 resolves names and can steer DNS answers; a load balancer distributes application traffic among targets.

**10. How does Route 53 failover work?**  
With appropriate health checks and failover records, Route 53 can return the healthy endpoint's DNS answer. Resolver caching means clients may continue using a previous answer until it expires.

**11. Why might a domain not resolve after creating a hosted zone?**  
The domain's public nameserver delegation may not point to the new hosted zone, or the record may have been created in a non-authoritative zone.

**12. Why does DNS work but HTTPS fail?**  
The endpoint may be unreachable, the load balancer or web server may be misconfigured, targets may be unhealthy, or TLS/certificate settings may be wrong.

**13. What is weighted routing used for?**  
To distribute DNS answers among configured records according to weights, often for controlled rollout or traffic experiments. It is not an exact per-request load balancer.

**14. Does a Route 53 health check repair an unhealthy server?**  
No. It reports health according to its configuration and can influence supported routing decisions, but repair or replacement requires other operational mechanisms.

**15. What is a private hosted zone used for?**  
Internal DNS names for resources in associated VPCs and configured connected networks.

---

## 18. Further reading

- [Amazon Route 53 Developer Guide](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/Welcome.html)
- [How Amazon Route 53 routes traffic](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy.html)
- [Working with hosted zones](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/hosted-zones-working-with.html)
- [Route 53 record types](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/ResourceRecordTypes.html)
- [Route 53 alias records](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/alias-resource-record-sets.html)
- [Route 53 health checks](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover.html)
- [Route 53 pricing](https://aws.amazon.com/route53/pricing/)
- [DNS concepts — ICANN](https://www.icann.org/resources/pages/dns-2012-02-25-en)
- [AWS DevOps Zero to Hero repository](https://github.com/iam-veeramalla/aws-devops-zero-to-hero)

---

## Lesson summary

Amazon Route 53 provides managed DNS hosting, domain registration options, health checks, and DNS routing policies. Hosted zones hold records; domain delegation determines which nameservers public resolvers trust; and records map names to application endpoints or other DNS data. Routing policies can influence which DNS answer a client receives, but they do not replace VPC routing, load balancing, or application health management.

For reliable deployments, validate DNS delegation and records, understand TTL and resolver caching, test application connectivity separately from name resolution, and protect DNS changes with appropriate access controls and change management.
