# AWS Zero to Hero — Cloud Fundamentals & AWS Account Setup

> **Series:** Abhishek Veeramalla — 30-Day AWS Learning Series  
> **Session:** Day 01 — Introduction to AWS, Public Cloud and Account Creation  
> **Video:** https://www.youtube.com/watch?v=n6RWhajimZg  
> **Audience:** Cloud and DevOps beginners progressing toward production-grade infrastructure  
> **Updated:** October 2026

## Learning objectives

By the end of this session you should be able to explain cloud computing, contrast on-premises and cloud environments, distinguish public/private/hybrid deployments, describe virtualization and multi-tenancy, reason about cloud economics, and create a secured AWS learning account with billing safeguards.

## Scope and learning-series boundaries

This README expands the introductory concepts described in the video with independent background research and safe onboarding procedures. It is **not a verbatim transcript**. The video summary supplies the session outline; AWS documentation supplies current account and billing information. This lesson intentionally **does not** provide full EC2 provisioning, VPC subnet design, IAM policy engineering, S3 administration, Terraform, or Kubernetes labs. Those deserve separate READMEs in later sessions.

## Table of contents

1. [Cloud computing: definition and history](#1-cloud-computing-definition-and-history)
2. [On-premises infrastructure and its constraints](#2-on-premises-infrastructure-and-its-constraints)
3. [Virtualization and resource pooling](#3-virtualization-and-resource-pooling)
4. [Cloud characteristics and service models](#4-cloud-characteristics-and-service-models)
5. [Public, private and hybrid cloud](#5-public-private-and-hybrid-cloud)
6. [Why public cloud became popular](#6-why-public-cloud-became-popular)
7. [Why AWS and what are its trade-offs?](#7-why-aws-and-what-are-its-trade-offs)
8. [Cloud economics and repatriation](#8-cloud-economics-and-repatriation)
9. [AWS global infrastructure primer](#9-aws-global-infrastructure-primer)
10. [AWS account creation walkthrough](#10-aws-account-creation-walkthrough)
11. [Day-one security and cost controls](#11-day-one-security-and-cost-controls)
12. [Hands-on verification lab](#12-hands-on-verification-lab)
13. [Troubleshooting](#13-troubleshooting)
14. [Interview questions and review exercises](#14-interview-questions-and-review-exercises)
15. [Glossary, references and next steps](#15-glossary-references-and-next-steps)

---

## 1. Cloud computing: definition and history

**Cloud computing** is the on-demand delivery of configurable computing capabilities—compute, storage, networking, databases and managed services—over a network, typically with metered or usage-based pricing.

A simplified evolution:

```text
Dedicated physical servers
        ↓
Virtualized data centers (multiple VMs per host)
        ↓
Self-service infrastructure + automation + APIs
        ↓
Public cloud, managed platforms, containers and serverless
```

**Important distinction:** virtualization is an enabling technology, not the complete definition of cloud. A virtualized data center without self-service provisioning, elasticity, automation or metering is not necessarily a cloud platform.

### Five essential cloud characteristics (NIST model)

| Characteristic | Meaning | Example |
|---|---|---|
| On-demand self-service | Provision without a manual procurement ticket | Launch a compute resource via console/API |
| Broad network access | Access through standard networks and clients | HTTPS-based management console |
| Resource pooling | Provider dynamically allocates shared capacity | Virtualized hosts supporting multiple customers |
| Rapid elasticity | Scale capacity up/down as demand changes | Add or remove application instances |
| Measured service | Track and account for usage | Metered compute hours or storage consumption |

Cloud does not guarantee low cost, zero maintenance, zero outages or automatic security.

## 2. On-premises infrastructure and its constraints

In a traditional data center, an organization procures physical servers, racks, networking equipment, power, cooling, storage, physical security and support contracts. Teams install operating systems, apply patches, maintain hardware and plan capacity.

```text
Users → Internet/Corporate WAN → Firewall → Load Balancer
                                        ↓
                                 Physical Servers
                                        ↓
                                  Storage/Database
```

### Common challenges

- **Up-front capital expense (CapEx):** hardware, facilities and licensing may be purchased before demand is known.
- **Procurement lead time:** adding capacity may require approvals, shipping and installation.
- **Capacity mismatch:** buying for peak demand can leave equipment idle; buying for average demand can cause saturation.
- **Operations overhead:** hardware replacement, power, cooling and facilities resilience are owned by the organization.
- **Disaster recovery:** a second site requires separate infrastructure and replication planning.

### When on-premises remains sensible

Predictable high-utilization workloads, strict locality requirements, specialized hardware, existing depreciated investments, or limited connectivity can favor on-premises. A sound decision uses total cost of ownership (TCO), not a blanket claim that cloud is always cheaper.

## 3. Virtualization and resource pooling

Virtualization lets multiple isolated **virtual machines (VMs)** share one physical host. A **hypervisor** mediates access to CPU, memory, storage and devices.

```text
+---------------------+---------------------+
| VM A: Linux + App   | VM B: Linux + DB    |
+---------------------+---------------------+
|          Hypervisor / Virtualization       |
+-------------------------------------------+
|       Physical CPU / RAM / Disk / NIC      |
+-------------------------------------------+
```

**Type 1 hypervisor:** runs on or close to bare metal (examples: KVM-based stacks, VMware ESXi, Hyper-V). **Type 2 hypervisor:** runs as an application on a host operating system (example: VirtualBox). Product architectures differ, so this is a conceptual classification.

### How virtualization improves utilization

Suppose a server has 32 vCPUs worth of scheduling capacity and four isolated applications each usually need 4 vCPUs. Consolidation can improve average utilization versus dedicating one large physical machine to each app. This is **not** free capacity: concurrent peaks, memory limits, storage I/O and noisy-neighbor effects still matter.

### Virtual machines vs containers

| Dimension | Virtual machine | Container |
|---|---|---|
| Isolation boundary | Virtual hardware + guest kernel | OS-level isolation sharing a kernel |
| Typical startup | Slower | Faster |
| OS requirement | Each VM can run its own kernel | Shares host kernel family |
| Common use | Strong workload separation, full OS | Application packaging and deployment |

Containers and virtualization can be combined: containers commonly run inside cloud VMs.

### Multi-tenancy and isolation

Cloud providers share infrastructure across tenants while applying isolation mechanisms. Security still depends on hypervisor hardening, network controls, identity policies and customer configuration. Multi-tenancy is not synonymous with public access to customer data.

## 4. Cloud characteristics and service models

### IaaS, PaaS and SaaS

| Model | You typically manage | Provider typically manages | Example |
|---|---|---|---|
| IaaS | Guest OS, runtime, app, data | Facilities, physical servers, core virtualization | Amazon EC2 |
| PaaS | App logic, configuration, data | More of runtime and platform operations | AWS Elastic Beanstalk (platform example) |
| SaaS | Users, configuration and data governance | Application and most underlying stack | Web-based hosted productivity application |

The exact division varies by product. **Serverless** is an execution/operations model, not a guarantee that servers do not exist; servers are abstracted from the customer.

### Elasticity vs scalability

- **Scalability:** ability to support greater load by adding capacity.
- **Elasticity:** ability to adjust capacity dynamically as demand rises and falls.
- **Vertical scaling:** increase resources for an existing instance.
- **Horizontal scaling:** add more instances or nodes.

For DevOps, APIs and automation are foundational: repeatable provisioning enables infrastructure as code, CI/CD, autoscaling and controlled rollback.

## 5. Public, private and hybrid cloud

| Attribute | Public cloud | Private cloud | Hybrid cloud |
|---|---|---|---|
| Infrastructure ownership | Third-party provider | Dedicated to one organization | Combination |
| Provisioning | Provider services/APIs | Organization-managed platform | Both |
| Physical maintenance | Mostly provider | Mostly organization or contracted operator | Split |
| Elasticity | Large provider pool, subject to quotas | Limited by purchased capacity | Depends on integration |
| Typical use | Startups, digital products, burst demand | Special-purpose regulated or legacy systems | Phased migration, data locality, mixed workloads |

**Public cloud** refers to the provider's service model—not to making your application publicly reachable. Private networking, encryption and access controls remain available in public clouds.

**Private cloud** requires cloud-like automation/self-service on dedicated infrastructure; simply owning servers does not make a private cloud.

**Hybrid cloud** connects on-premises/private resources and public cloud resources. Challenges include identity federation, network latency, data transfer costs, observability, policy consistency and operational complexity.

**Multi-cloud** uses more than one public-cloud provider. It is not the same as hybrid cloud, although architectures can be both.

## 6. Why public cloud became popular

1. **Faster experimentation:** start with small capacity rather than buying a data center.
2. **Global reach:** choose deployment locations near users and business requirements.
3. **Managed building blocks:** reduce some operational toil around databases, messaging and infrastructure.
4. **Automation:** expose infrastructure through APIs and infrastructure-as-code tools.
5. **Elastic capacity:** respond to changing traffic without buying for every potential peak.
6. **Resilience options:** build redundant architectures across failure domains.

### Example: product launch

An early-stage application may have 100 daily users but could grow to 100,000. On-premises hardware procurement requires guessing demand. Cloud infrastructure allows incremental growth—but **the application must still be designed to scale** and costs must be monitored.

### Cloud responsibility is not eliminated

Cloud customers remain responsible for application correctness, appropriate identity permissions, data protection, workload configuration and many operating-system responsibilities depending on the service.

## 7. Why AWS and what are its trade-offs?

AWS launched foundational infrastructure services early in the commercial cloud era and developed a broad ecosystem of services, training, partners and operational tooling. Its first-mover advantage helps explain adoption, but market share fluctuates and is not itself proof that AWS is optimal for every workload.

### Factors to evaluate

| Factor | Question |
|---|---|
| Service breadth | Does the platform provide the capabilities needed? |
| Regions and compliance | Can data be located and processed appropriately? |
| Reliability | Can the design tolerate AZ or regional failures? |
| Talent and tooling | Can the team operate it safely? |
| Pricing | What are compute, storage, egress, support and operations costs? |
| Lock-in | How difficult is it to migrate data and proprietary APIs? |

**AWS vs Azure vs Google Cloud:** all offer mature compute, storage, networking and managed services. Choose based on workload fit, compliance, existing identity/tooling, operational capability and total cost—not brand popularity alone.

### AWS for DevOps engineers

AWS exposes programmable infrastructure for repeatable deployment and automation. Later lessons should cover CLI/SDK access, IAM, VPC, EC2, S3, monitoring, CI/CD, containers and infrastructure as code separately.

## 8. Cloud economics and repatriation

### CapEx and OpEx

- **CapEx:** upfront purchase of assets such as servers and networking gear.
- **OpEx:** ongoing spending such as metered compute, managed services and subscriptions.

Cloud shifts many expenses toward consumption-based OpEx, but financial accounting treatment depends on the contract and organization.

### A simplified TCO model

```text
On-prem TCO ≈ hardware + licenses + facilities + power/cooling
            + staff + maintenance + network + DR + refresh

Cloud TCO ≈ compute + storage + network/egress + managed services
          + support + security tooling + staff + migration
```

**Illustrative example only:** a VM costing $0.10 per running hour would cost about $73 for 730 hours, *before* storage, networking, taxes and other charges. This is arithmetic, not an AWS quote.

### Hidden or underestimated cloud costs

- Internet and cross-region data transfer
- Idle resources, orphaned storage and snapshots
- Logging/monitoring ingestion and retention
- Managed database capacity and backup retention
- Enterprise support and third-party licenses
- Architectural complexity and engineering labor

### Cloud repatriation

**Cloud repatriation** means moving some workloads or data from public cloud back to on-premises, colocation or private infrastructure. Motivations may include predictable sustained utilization, egress costs, sovereignty, latency, or a desire for greater control.

Avoid unverified numerical claims about what percentage of companies repatriate. Organizations may repatriate **selected workloads** while continuing to grow their cloud usage. A useful decision compares workload-specific TCO, risk and operational capability.

### Advanced: unit economics

Track cost per meaningful business unit, such as cost per 1,000 API requests or per active customer. A falling cloud bill is not always an improvement if throughput falls faster; similarly, a rising bill can be acceptable if unit cost decreases and revenue grows.

## 9. AWS global infrastructure primer

```text
AWS Global Infrastructure
  └── Region (geographic area)
        ├── Availability Zone A (isolated failure domain)
        ├── Availability Zone B
        └── Availability Zone C
```

- **Region:** separate geographic location; many AWS resources are region-scoped.
- **Availability Zone (AZ):** isolated infrastructure location within a Region; an AZ can contain one or more data centers.
- **Edge location:** point of presence used by certain edge/network-delivery services.

Deploying across multiple AZs can reduce the impact of one AZ failure, but it does not automatically make an application highly available. Dependencies, state replication, traffic routing and testing still matter.

AWS's live count of Regions and AZs changes. See the official infrastructure page instead of treating a snapshot count as permanent: https://aws.amazon.com/about-aws/global-infrastructure/

## 10. AWS account creation walkthrough

> **October 2026 update:** AWS onboarding has changed since older introductory videos. AWS now offers new and advanced sign-up paths, and many new customers using the new path do **not** need to provide a credit card. Some applicants are asked for payment verification. The older blanket claim that every account requires a card is no longer reliable.

### Before you begin

- Use an email account you control and protect with MFA.
- Have a working phone number and accurate contact details.
- Decide whether this is a personal lab account or a business account.
- Check current AWS eligibility and billing terms for your country.
- Do not use a production company's account for experiments without authorization.

### Step-by-step

1. Open https://aws.amazon.com/resources/create-account/ or https://aws.amazon.com/free/.
2. Choose the **new** signup path for a simple learning environment, or **advanced** when you need explicit account configuration and broader services.
3. Supply the requested sign-in identity, account name and verification information. Exact screens depend on signup path and country.
4. Verify your email and complete any requested phone or identity checks.
5. If prompted, enter valid payment details and review any temporary authorization hold.
6. Review the **Free** versus **Paid** plan choice. A Free plan can restrict service access; a Paid plan can generate charges beyond credits or excluded usage.
7. Complete the signup and sign in through the appropriate AWS console or Builder ID flow.
8. Open **Billing and Cost Management** and verify your account plan, credit balance and any spend-control options.
9. Set up strong authentication and complete the security checklist in the next section.

### Current Free Tier basics

AWS documents up to **$200 in credits for eligible new customers** ($100 at signup and up to $100 earned through eligible activities). The Free plan is limited to **six months or until credits are depleted**, whichever happens first; the plan then ends and the account closes unless upgraded. Always Free offers have service-specific usage limits. Eligibility and offer terms can change.

**Never assume a service is free merely because you have a Free Tier account.** Before launching any resource, check plan restrictions, current pricing and credit applicability.

Official sources:
- https://aws.amazon.com/resources/create-account/
- https://docs.aws.amazon.com/us_en/awsaccountbilling/latest/aboutv2/free-tier.html
- https://docs.aws.amazon.com/us_en/awsaccountbilling/latest/aboutv2/free-tier-plans.html

## 11. Day-one security and cost controls

### Security checklist

- [ ] Secure the primary sign-in identity and recovery email with MFA.
- [ ] For accounts with a root user, enable root-user MFA and avoid root for everyday administration.
- [ ] Use least-privilege access and short-lived credentials where available.
- [ ] Do **not** create root access keys.
- [ ] Never commit passwords, access keys, account recovery details or payment information to GitHub.
- [ ] Review security notifications and account contact details.
- [ ] Confirm the account's actual permission model before creating IAM users or roles; some new signup paths have simplified defaults.

### Cost checklist

- [ ] Confirm Free or Paid plan and credit expiration date.
- [ ] Review Free Tier eligibility for each service before using it.
- [ ] Configure a budget and email alerts where available; note that alerts are **not** a hard stop on charges.
- [ ] Inspect running resources in all Regions you have used.
- [ ] Remove lab resources after testing and verify deletion.
- [ ] Revisit the Billing dashboard after each lab.

**Shared responsibility:** AWS secures the underlying cloud infrastructure; customers secure what they configure and deploy **in** the cloud. The exact division changes with IaaS, managed services and SaaS.

## 12. Hands-on verification lab

**Goal:** verify the account is ready for later sessions without deploying chargeable infrastructure.

### Lab A — Console orientation

1. Sign in to your AWS account.
2. Locate the Region selector; record your selected Region.
3. Open the Billing and Cost Management area.
4. Locate Free Tier usage/credits, if shown for your plan.
5. Locate your security or identity settings and check MFA status.
6. Open the service catalog but **do not provision resources**.

### Lab B — Account readiness record

Create a local file named `account-readiness.md` (do not commit sensitive details):

```markdown
# AWS Account Readiness
- Account plan: Free / Paid / Other
- MFA enabled: Yes / No
- Default Region: <region-code>
- Credits/expiry reviewed: Yes / No
- Billing controls reviewed: Yes / No
- No unexpected resources: Confirmed / Needs review
- Next action: Begin dedicated identity/network/compute labs
```

Avoid screenshots exposing your account ID, email, billing address, payment method or personal details.

### Success criteria

You can log in securely, explain your plan's cost exposure, locate the Region selector and Billing console, and describe the difference between the AWS account, Region and individual cloud resources.

## 13. Troubleshooting

| Symptom | Likely explanation | Safe next step |
|---|---|---|
| Signup asks for card | Country, verification or eligibility requirements | Follow the official signup instructions; do not use fake payment details |
| Payment verification hold | Temporary fraud-prevention authorization | Review AWS guidance and bank notifications |
| Console access denied | Incorrect identity, permissions or incomplete setup | Check sign-in path and permissions; avoid broadening access blindly |
| Service not available | Free-plan limitation or Region/service availability | Check plan and regional availability before upgrading |
| Unexpected cost | Paid usage, unsupported credits, residual resources | Inspect Billing and Cost Explorer; delete unneeded resources and contact AWS Support if necessary |
| Resource seems missing | Wrong Region or account | Verify account identity and selected Region |

## 14. Interview questions and review exercises

### Questions with concise answers

**Q1. Is virtualization the same as cloud computing?**  
No. Virtualization abstracts hardware; cloud adds on-demand provisioning, networking, elasticity, metering and service management.

**Q2. Can a public-cloud application be private?**  
Yes. Public cloud refers to the service delivery model, not whether a workload is internet-facing.

**Q3. Why does cloud reduce procurement lead time?**  
Providers maintain resource pools exposed through APIs, so customers can provision without purchasing individual servers.

**Q4. Is cloud always cheaper than on-premises?**  
No. Utilization, data transfer, support, staffing, commitment discounts and workload architecture determine TCO.

**Q5. What is the difference between scalability and elasticity?**  
Scalability supports increasing demand; elasticity adapts capacity to changing demand.

**Q6. What is an Availability Zone?**  
An isolated infrastructure location inside a Region, designed to help customers build fault-tolerant architectures.

**Q7. What is cloud repatriation?**  
Moving selected workloads or data from public cloud back to privately controlled infrastructure.

**Q8. Who patches an EC2 guest OS?**  
Generally the customer, unless a specific managed arrangement changes that responsibility.

**Q9. Does a billing alert prevent charges?**  
No. Alerts notify; they are not automatically a spending cutoff.

**Q10. Why avoid root access keys?**  
They are long-lived, highly privileged credentials with substantial compromise risk.

### Scenario exercises

1. A retailer gets a 10× traffic spike for two days per year. Compare cloud elasticity with on-prem peak provisioning.
2. A factory has low-latency equipment with limited internet connectivity. Evaluate on-prem, cloud and hybrid options.
3. A SaaS startup's AWS bill doubles while active users triple. Which unit-economics metric would you inspect?
4. A team places its entire application in one AZ. Identify the failure domain and propose a high-level mitigation.
5. A new AWS learner wants to create resources immediately. Explain the security and billing checks required first.

## 15. Glossary, references and next steps

### Glossary

- **CapEx:** capital expenditure on long-lived assets.
- **OpEx:** ongoing operating expense.
- **TCO:** total cost of ownership over a defined time horizon.
- **Hypervisor:** software layer that supports virtual machines.
- **Tenant:** customer or organizational workload sharing a provider platform.
- **Region:** geographic AWS infrastructure location.
- **AZ:** isolated AWS infrastructure location within a Region.
- **MFA:** multi-factor authentication.
- **FinOps:** collaborative practices for cloud financial accountability and optimization.
- **Repatriation:** moving selected cloud workloads back to private infrastructure.

### Video

- Abhishek Veeramalla, **Day 1 — Introduction to AWS | What is Public Cloud? | Create an AWS Account**: https://www.youtube.com/watch?v=n6RWhajimZg
- Playlist: https://www.youtube.com/playlist?list=PLdpzxOOAlwvIc1TjTwopNSjRJkzES2ZXk

### Authoritative references

- NIST, *The NIST Definition of Cloud Computing (SP 800-145)*: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-145.pdf
- AWS, *Create an AWS Account*: https://aws.amazon.com/resources/create-account/
- AWS, *AWS Free Tier*: https://aws.amazon.com/free/
- AWS, *Free Tier plans*: https://docs.aws.amazon.com/us_en/awsaccountbilling/latest/aboutv2/free-tier-plans.html
- AWS, *Global Infrastructure*: https://aws.amazon.com/about-aws/global-infrastructure/
- AWS, *Regions and Availability Zones*: https://docs.aws.amazon.com/global-infrastructure/latest/regions/aws-regions-availability-zones.html
- AWS, *Shared Responsibility Model*: https://aws.amazon.com/compliance/shared-responsibility-model/
- AWS, *IAM security best practices*: https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html
- AWS, *Billing and Cost Management*: https://docs.aws.amazon.com/cost-management/latest/userguide/what-is-costmanagement.html

### Recommended repository structure

```text
aws-zero-to-hero/
├── README.md                         # Series index and navigation
├── 01-cloud-fundamentals/
│   └── README.md                     # This lesson
├── 02-next-session/
│   └── README.md                     # Use actual video topic when available
└── assets/
    └── README.md                     # Optional diagrams and attribution
```

### Future-lesson writing policy

- Start each lesson with the **specific video's new objectives**, not a repeated cloud introduction.
- Refer back to foundational explanations by relative links, e.g. `[Cloud foundations](../01-cloud-fundamentals/README.md)`.
- Separate **what the presenter covered** from **additional research and operational best practices**.
- Provide architecture diagrams, commands, labs, troubleshooting and interview questions only where relevant to the session.
- Validate prices, service limits, CLI syntax and console workflows against current official documentation.
- Avoid invented timestamps, transcript quotations, benchmark figures or market-share percentages.

---

**Disclaimer:** Independent educational notes inspired by the linked video; not an official transcript, AWS endorsement or affiliation with the presenter. Always check current AWS documentation before incurring costs or changing production infrastructure.
