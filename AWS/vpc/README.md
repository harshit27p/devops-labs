# Day 04 — Amazon VPC: Cloud Networking Fundamentals

> **Series:** AWS DevOps Zero to Hero  
> **Instructor:** Abhishek Veeramalla  
> **Video:** [Watch the VPC session](https://www.youtube.com/watch?v=P8g7Z4NYk3Q&list=PLdpzxOOAlwvIc1TjTwopNSjRJkzES2ZXk&index=58)  
> **Curriculum reference:** [aws-devops-zero-to-hero](https://github.com/iam-veeramalla/aws-devops-zero-to-hero)  
> **Focus:** VPCs, CIDR blocks, subnets, route tables, Internet Gateways, public/private subnet design, load balancers, security groups, NAT Gateways, and VPC Flow Logs.

These notes expand the video summary into a practical reference. They distinguish core networking concepts from architecture patterns and operational details. AWS Console labels and service pricing may change, so validate current behavior in the official documentation before implementing in a real account.

---

## Contents

- [1. Learning objectives](#1-learning-objectives)
- [2. What is a VPC?](#2-what-is-a-vpc)
- [3. VPC architecture overview](#3-vpc-architecture-overview)
- [4. CIDR blocks and IP addressing](#4-cidr-blocks-and-ip-addressing)
- [5. Subnets and Availability Zones](#5-subnets-and-availability-zones)
- [6. Route tables and routing](#6-route-tables-and-routing)
- [7. Internet Gateway and public subnets](#7-internet-gateway-and-public-subnets)
- [8. Private subnets and NAT Gateways](#8-private-subnets-and-nat-gateways)
- [9. Security groups and network ACLs](#9-security-groups-and-network-acls)
- [10. Load balancers in a VPC](#10-load-balancers-in-a-vpc)
- [11. VPC Flow Logs](#11-vpc-flow-logs)
- [12. DNS in a VPC](#12-dns-in-a-vpc)
- [13. Hands-on lab: design a two-tier VPC](#13-hands-on-lab-design-a-two-tier-vpc)
- [14. Troubleshooting checklist](#14-troubleshooting-checklist)
- [15. Security, resilience, and cost considerations](#15-security-resilience-and-cost-considerations)
- [16. AWS CLI quick reference](#16-aws-cli-quick-reference)
- [17. Assignment](#17-assignment)
- [18. Interview questions](#18-interview-questions)
- [19. Further reading](#19-further-reading)

---

## 1. Learning objectives

After completing this lesson, you should be able to:

1. Explain why Amazon VPC is the foundation of AWS networking.
2. Design a VPC IPv4 CIDR plan and divide it into non-overlapping subnets.
3. Explain public and private subnets precisely.
4. Read route tables and understand longest-prefix matching.
5. Explain how Internet Gateways and NAT Gateways differ.
6. Distinguish security groups from network ACLs.
7. Describe how load balancers connect clients to application targets.
8. Enable and interpret VPC Flow Logs for troubleshooting.
9. Diagnose common routing and connectivity failures.
10. Design a basic two-tier network with web/application and private tiers.

### Prerequisites

- Basic IPv4 networking: addresses, subnet masks, default gateways, TCP/UDP.
- Familiarity with EC2, security groups, Regions, and Availability Zones.
- An AWS account for optional hands-on exercises.
- Awareness that NAT Gateways, load balancers, data transfer, and some logging destinations incur charges.

---

## 2. What is a VPC?

**Amazon Virtual Private Cloud (Amazon VPC)** lets you define a logically isolated virtual network in an AWS Region. You choose IP address ranges, create subnets, configure routes, and apply network security controls to AWS resources.

A VPC is like a gated community:

- The **VPC** is the overall community.
- **CIDR blocks** define the address space available inside it.
- **Subnets** are smaller sections of the community.
- **Route tables** are signboards that determine where traffic should go.
- An **Internet Gateway** is a connection point for internet routing.
- A **NAT Gateway** enables eligible outbound connections from private subnets.
- **Security groups** are stateful traffic rules attached to network interfaces.
- **Network ACLs** are stateless subnet-level traffic filters.
- **VPC Flow Logs** record information about IP traffic to help with analysis and troubleshooting.

The analogy is useful, but a VPC is a software-defined network—not a physical building or a guarantee that every resource is automatically private.

### Why use a VPC?

- Define network address ranges and segmentation.
- Separate application tiers and environments.
- Control how traffic enters, exits, and moves within the network.
- Connect AWS resources to other networks through supported connectivity services.
- Apply layered network controls.
- Capture traffic metadata for investigation and operations.

### VPC isolation is not complete security by itself

A VPC provides a network boundary, but security also depends on routing, security groups, network ACLs, IAM, operating-system configuration, application security, and the services you expose. A public subnet does not mean every resource inside it is automatically reachable from the internet.

---

## 3. VPC architecture overview

A common two-tier design places a public load balancer in public subnets and application instances in private subnets.

```text
                         Internet users
                               |
                               v
                        Internet Gateway
                               |
                 +-------------+-------------+
                 |           VPC             |
                 |                            |
                 |  Public subnet (AZ-a)      |
                 |  +----------------------+  |
                 |  | Load balancer        |  |
                 |  +----------+-----------+  |
                 |             |              |
                 |  Private subnet (AZ-a)     |
                 |  +----------------------+  |
                 |  | Application EC2      |  |
                 |  +----------------------+  |
                 |                            |
                 |  Public subnet (AZ-b)      |
                 |  +----------------------+  |
                 |  | Load balancer node    |  |
                 |  +----------------------+  |
                 |             |              |
                 |  Private subnet (AZ-b)     |
                 |  +----------------------+  |
                 |  | Application EC2      |  |
                 |  +----------------------+  |
                 +----------------------------+
```

This is a conceptual design. An AWS load balancer manages its own nodes and networking; users generally create the load balancer and select subnets rather than manually placing individual load-balancer nodes.

A NAT Gateway may be placed in a public subnet for private instances that need outbound internet access. Production designs commonly use multiple AZs for resilience and make explicit decisions about cross-AZ routing and NAT cost.

### Core components at a glance

| Component | Main purpose |
|---|---|
| VPC | Regional logical network boundary |
| CIDR block | Defines an IP address range |
| Subnet | Segment of a VPC IP range associated with one AZ |
| Route table | Chooses next hop for network destinations |
| Internet Gateway (IGW) | Enables internet routing for resources with appropriate public addressing and routes |
| NAT Gateway | Allows private-subnet resources to initiate outbound connections to supported destinations |
| Security group | Stateful traffic control for network interfaces |
| Network ACL | Stateless traffic filter at subnet boundaries |
| Load balancer | Distributes client connections/requests to targets |
| VPC Flow Logs | Captures metadata about IP traffic |
| VPC endpoints | Private connectivity to supported AWS services without needing an internet gateway/NAT for that service path |

---

## 4. CIDR blocks and IP addressing

**CIDR** stands for Classless Inter-Domain Routing. CIDR notation represents an IP network using an address and a prefix length, such as `10.20.0.0/16`.

For IPv4, the prefix length specifies how many leading bits represent the network. The remaining bits are available for addresses within that range.

### Common IPv4 prefix sizes

| CIDR | Total IPv4 addresses | Typical use |
|---|---:|---|
| `/16` | 65,536 | Larger VPC address space |
| `/20` | 4,096 | Medium-sized network range |
| `/24` | 256 | Common subnet size |
| `/26` | 64 | Smaller subnet |
| `/28` | 16 | Smallest IPv4 subnet size supported for ordinary VPC subnets |

AWS reserves five IPv4 addresses in each subnet, so the number of IPv4 addresses available to resources is lower than the total address count. For example, a `/24` has 256 total IPv4 addresses and 251 are usable by resources under the standard reservation rule.

### Example address plan

Suppose a lab VPC uses `10.20.0.0/16`. The following subnet ranges are non-overlapping:

| Subnet | CIDR | Example purpose |
|---|---|---|
| Public-A | `10.20.1.0/24` | Load balancer and NAT Gateway in AZ-a |
| Public-B | `10.20.2.0/24` | Load balancer in AZ-b |
| Private-App-A | `10.20.11.0/24` | Application instances in AZ-a |
| Private-App-B | `10.20.12.0/24` | Application instances in AZ-b |
| Private-Data-A | `10.20.21.0/24` | Data tier in AZ-a |
| Private-Data-B | `10.20.22.0/24` | Data tier in AZ-b |

These are example ranges only. Check that your planned CIDRs do not overlap with on-premises networks, VPN-connected networks, other VPCs, or existing allocations.

### CIDR planning best practices

1. Choose private address ranges appropriate to your organization's network plan.
2. Avoid overlapping CIDRs if you expect to connect VPCs, VPNs, or corporate networks.
3. Allocate separate subnets by tier, AZ, and operational purpose.
4. Leave address space for growth and managed services.
5. Document every subnet's CIDR, AZ, route table, and intended workload.
6. Consider IPv6 separately; IPv6 routing and public reachability differ from IPv4.

### Private IPv4 ranges

Common RFC 1918 IPv4 private ranges are:

- `10.0.0.0/8`
- `172.16.0.0/12`
- `192.168.0.0/16`

Private addresses are not directly routable over the public internet, but private networks can still communicate through connected networks, VPNs, transit routing, or other configured paths.

---

## 5. Subnets and Availability Zones

A **subnet** is a range of IP addresses within a VPC. Each subnet belongs to one Availability Zone in a Region. Subnets are commonly used to separate application tiers and apply different routing policies.

### Public subnet

A subnet is conventionally called public when its associated route table has a route to an Internet Gateway for internet-bound IPv4 traffic, commonly `0.0.0.0/0 -> igw-...`.

For an IPv4 resource to be reachable from the internet, routing alone is not sufficient. It also needs an appropriate public IPv4 address or Elastic IP, permitted security-group/NACL rules, and a listening service.

### Private subnet

A private subnet does not have a direct route to an Internet Gateway for general internet-bound IPv4 traffic. Its route table may contain routes to a NAT Gateway, a virtual private gateway, a transit gateway, VPC endpoints, or other destinations.

Private does not mean “no network access.” A private instance can still communicate with permitted VPC resources and connected networks.

### Isolated subnet

An isolated subnet has no route to destinations outside the VPC beyond the local VPC route (and any intentionally configured local/private connectivity). It is often used for sensitive data tiers that should not have general outbound internet access.

### Public vs. private vs. isolated

| Characteristic | Public subnet | Private subnet | Isolated subnet |
|---|---|---|---|
| Direct IGW default route | Commonly yes | No | No |
| Direct inbound internet reachability | Possible with public IP and allowed rules | Not through direct IGW routing | Not through direct IGW routing |
| Outbound internet | Often via IGW | May use NAT or a proxy | Generally no general internet route |
| Typical workloads | Public load balancers, bastions where needed, NAT Gateways | App servers, internal services | Databases or tightly restricted workloads |
| Security controls still required | Yes | Yes | Yes |

The subnet name does not determine its behavior; the route table and resource configuration do.

---

## 6. Route tables and routing

A **route table** contains rules that determine where traffic is sent based on its destination IP range. Each subnet is associated with one route table; if no explicit association is set, the VPC's main route table applies.

### Common route targets

| Destination | Target | Meaning |
|---|---|---|
| VPC CIDR, e.g. `10.20.0.0/16` | `local` | Routes traffic within the VPC |
| `0.0.0.0/0` | Internet Gateway | Default IPv4 route toward the internet |
| `0.0.0.0/0` | NAT Gateway | Default IPv4 route for outbound access through NAT |
| Corporate CIDR | Virtual private gateway / Transit Gateway | Route to a connected network |
| Service-specific prefix list | VPC endpoint | Route to a supported AWS service through a gateway endpoint |

The exact target depends on the connectivity design and the AWS service being used.

### Longest-prefix match

When multiple routes match a destination, routing generally selects the most specific matching prefix (the longest prefix), subject to AWS routing behavior and route-target rules.

For example, a route for `10.20.0.0/16` is less specific than one for `10.20.11.0/24`. Traffic for `10.20.11.25` matches both, but the `/24` route is more specific.

### Example public route table

| Destination | Target |
|---|---|
| `10.20.0.0/16` | `local` |
| `0.0.0.0/0` | `igw-xxxxxxxx` |

### Example private application route table

| Destination | Target |
|---|---|
| `10.20.0.0/16` | `local` |
| `0.0.0.0/0` | `nat-xxxxxxxx` |

A private route table's NAT route provides a path for supported outbound IPv4 connections through the NAT Gateway. Return traffic for connections initiated from the private instance is handled by connection tracking; unsolicited inbound connections from the internet are not enabled by the NAT Gateway.

### Common route-table mistakes

- Subnet associated with the wrong route table.
- Missing `0.0.0.0/0` route for the intended internet path.
- Internet Gateway not attached to the VPC.
- NAT Gateway is in a subnet without the required internet route.
- NAT Gateway is unavailable or placed in the wrong AZ for the intended design.
- Overlapping or overly broad routes send traffic through an unexpected target.
- A route exists, but security groups or network ACLs block the traffic.

---

## 7. Internet Gateway and public subnets

An **Internet Gateway (IGW)** is a VPC component that allows communication between a VPC and the internet when the associated routing and addressing requirements are met. It is horizontally scaled, redundant, and managed by AWS.

### To make an EC2 instance reachable over IPv4

Check all of the following:

1. An Internet Gateway is attached to the VPC.
2. The subnet route table has an appropriate route to the IGW.
3. The instance has a public IPv4 address or Elastic IP.
4. The security group permits the intended inbound traffic.
5. Network ACL rules permit the inbound and return traffic.
6. The host firewall and application allow the traffic.
7. The client uses the correct public endpoint and port.

An IGW does not automatically assign a public IP address, open ports, or make every VPC resource public.

### Internet Gateway vs. NAT Gateway

| Internet Gateway | NAT Gateway |
|---|---|
| Supports internet routing for appropriately addressed resources | Allows private resources to initiate outbound IPv4 connections |
| Used by public-subnet route tables | Commonly used by private-subnet route tables |
| Does not itself provide a firewall policy | Does not itself replace security groups or host firewalls |
| No need to route all traffic through a single NAT appliance | Has hourly and data processing charges under current pricing |
| Public IPv4 addressing and routes still matter | Public NAT Gateway generally resides in a public subnet and uses an Elastic IP |

---

## 8. Private subnets and NAT Gateways

A **NAT Gateway** lets resources in a private subnet initiate connections to supported external destinations without allowing those destinations to initiate new connections directly to the private resource through the NAT Gateway.

Common uses include downloading OS updates, retrieving packages, and accessing external APIs.

### Typical NAT architecture

```text
Private EC2 instance
       |
       | Default route: 0.0.0.0/0
       v
Private route table
       |
       v
NAT Gateway in public subnet
       |
       v
Public route table
       |
       v
Internet Gateway
       |
       v
External service
```

### NAT Gateway requirements

For a standard public NAT Gateway setup:

1. Create the NAT Gateway in a public subnet.
2. Allocate and associate an Elastic IP as required by the creation workflow.
3. Ensure the public subnet route table routes internet-bound traffic to an IGW.
4. Add a route in the private subnet route table to the NAT Gateway.
5. Ensure security groups and network ACLs permit the required flows.
6. Validate DNS and external endpoint access from the private instance.

### NAT Gateway limitations and design considerations

- A NAT Gateway does not allow unsolicited inbound internet connections to private instances.
- A public NAT Gateway provides outbound internet connectivity for private IPv4 workloads; other NAT designs and IPv6 egress use different patterns.
- NAT Gateways incur charges, including hourly usage and data processing, plus related data transfer costs where applicable.
- A single NAT Gateway can create an AZ dependency and cross-AZ data charges when private resources in other AZs use it.
- Production designs often use a NAT Gateway per AZ for resilience and predictable AZ-local routing, balancing cost against availability needs.
- VPC endpoints can reduce NAT usage for supported AWS services, such as S3 and DynamoDB through gateway endpoints, or other supported services through interface endpoints.

### NAT Gateway vs. NAT instance

NAT instances are EC2 instances configured to perform NAT. NAT Gateways are managed AWS networking infrastructure. NAT instances require the customer to manage OS updates, capacity, availability, and routing behavior; NAT Gateways reduce that operational burden but have service pricing and feature constraints.

---

## 9. Security groups and network ACLs

VPC network security uses multiple layers. Security groups and network ACLs are not interchangeable.

### Security groups

- Associated with network interfaces and used by resources such as EC2 instances.
- Stateful: response traffic for an allowed connection is automatically permitted.
- Rules define allowed traffic; there are no explicit deny rules in a security group.
- Can reference other security groups as sources or destinations for supported traffic patterns.

### Network ACLs (NACLs)

- Applied at subnet boundaries.
- Stateless: inbound and outbound traffic must be allowed independently.
- Support allow and deny rules.
- Rules are evaluated in numerical order, and the first matching rule is applied.
- Ephemeral ports and return traffic need to be considered.

### Comparison

| Feature | Security group | Network ACL |
|---|---|---|
| Scope | Network interface/resource | Subnet |
| Stateful | Yes | No |
| Rules | Allow rules | Allow and deny rules |
| Rule evaluation | All applicable rules considered | Numbered rules, first match |
| Return traffic | Automatically allowed for tracked connections | Must be allowed by opposite-direction rules |
| Common role | Primary workload-level control | Additional subnet-level guardrail |

### Example web application rules

A public load balancer's security group might allow inbound HTTPS from intended client networks. The application instance's security group can allow application traffic only from the load balancer's security group. The database security group can allow its database port only from the application tier's security group.

This security-group reference pattern is generally safer than allowing all sources to reach every tier.

---

## 10. Load balancers in a VPC

A load balancer distributes traffic across targets such as EC2 instances. Elastic Load Balancing supports different load balancer types for different traffic and protocol requirements.

### Common types

- **Application Load Balancer (ALB):** Layer 7 HTTP/HTTPS routing, host/path rules, and application-aware features.
- **Network Load Balancer (NLB):** Layer 4 TCP/UDP/TLS use cases requiring high performance or static IP options.
- **Gateway Load Balancer (GWLB):** Deploys and scales virtual network appliances for supported inspection use cases.
- **Classic Load Balancer:** Legacy option; evaluate modern types for new designs.

### Example traffic flow

```text
Client
  |
  | HTTPS
  v
Public Application Load Balancer
  |
  | HTTP or HTTPS to target group
  v
Private EC2 targets in multiple AZs
  |
  v
Application response
```

### Security-group pattern

- Load balancer security group: allow the intended client traffic.
- Application security group: allow the application port from the load balancer security group.
- Database security group: allow database traffic from only the application tier.

Health checks should use a suitable endpoint and reflect whether the application can serve requests. A healthy EC2 instance is not necessarily a healthy application target.

---

## 11. VPC Flow Logs

**VPC Flow Logs** capture metadata about IP traffic to network interfaces, subnets, or VPCs. They help investigate connectivity issues, understand traffic patterns, and support security monitoring.

Flow Logs are not packet captures. They do not record full packet payloads and should not be treated as a complete substitute for application logs or packet-level troubleshooting.

### Common fields

Depending on the selected format, records may include:

- Source and destination addresses.
- Source and destination ports.
- Protocol number.
- Packet and byte counts.
- Start and end times.
- Action such as `ACCEPT` or `REJECT`.
- Interface ID and flow direction, when included in the selected format.
- Log status and other metadata.

### Where logs can be delivered

Common destinations include CloudWatch Logs and Amazon S3. Supported delivery options and record formats may change, so consult current documentation.

### Flow Log action values

- `ACCEPT`: Traffic was accepted by the relevant network controls represented in the record.
- `REJECT`: Traffic was rejected by a network control such as a security group or network ACL, or otherwise not accepted as represented by the record.

Flow Logs are aggregated telemetry and may be delayed. A missing record does not always prove that no traffic occurred; consider log configuration, delivery status, aggregation, and the scope being observed.

### Troubleshooting with Flow Logs

1. Confirm Flow Logs are enabled for the correct VPC, subnet, or network interface.
2. Confirm the configured destination is receiving logs.
3. Filter by the source/destination IP, protocol, and port.
4. Compare timestamps with the connection attempt.
5. Look for accepted or rejected traffic.
6. Correlate the result with route tables, security groups, NACLs, host firewall, and service logs.

---

## 12. DNS in a VPC

AWS VPC networking integrates with DNS resolution. VPC settings include DNS support and DNS hostnames, which affect how resources resolve names and whether DNS hostnames are assigned or used as expected.

Important distinctions:

- A DNS name resolving to an IP does not prove the destination is reachable.
- Security groups and routing still determine whether a connection can succeed.
- Private hosted zones can resolve names for resources inside associated VPCs.
- Route 53 Resolver provides DNS resolution capabilities for VPCs and connected networks.
- VPC endpoints may provide private service paths, but endpoint DNS and policies must be configured correctly.

When troubleshooting, test both name resolution and network connectivity separately.

---

## 13. Hands-on lab: design a two-tier VPC

This lab is a design and console exercise. It is intentionally not a one-click script: route tables, NAT Gateways, load balancers, and public IPv4 resources can incur costs. Review the account's current pricing before creating them.

### Goal

Design a VPC with public subnets for an internet-facing load balancer and private subnets for application instances in two Availability Zones.

### Example address plan

Use a non-overlapping CIDR plan such as:

- VPC: `10.20.0.0/16`
- Public subnet A: `10.20.1.0/24`
- Public subnet B: `10.20.2.0/24`
- Private application subnet A: `10.20.11.0/24`
- Private application subnet B: `10.20.12.0/24`

Confirm these ranges do not overlap with any connected network in your environment.

### Step 1 — Create the VPC

1. Open the VPC console in the intended Region.
2. Create a VPC with the selected IPv4 CIDR.
3. Enable DNS resolution as required.
4. Enable DNS hostnames if your design needs them.
5. Add descriptive tags, for example `Project=VPC-Lab` and `Environment=Learning`.

### Step 2 — Create subnets

Create four subnets using the CIDR plan. Place the two public subnets in different AZs and the two private application subnets in those same AZs.

Verify each subnet's CIDR and AZ before proceeding.

### Step 3 — Attach an Internet Gateway

1. Create an Internet Gateway.
2. Attach it to the lab VPC.
3. Confirm the gateway state is attached.

### Step 4 — Configure the public route table

1. Create a route table for public subnets.
2. Keep the local VPC route.
3. Add `0.0.0.0/0` with the Internet Gateway as target.
4. Associate the route table with both public subnets.

Do not associate the public route table with private application subnets.

### Step 5 — Configure private routing

Choose one of the following approaches according to the lab objective:

- **No internet egress:** Keep only the local route, and use VPC endpoints or other private connectivity as required.
- **Outbound IPv4 internet access:** Create a NAT Gateway in a public subnet, allocate an Elastic IP as required, and add a default route from the private route table to the NAT Gateway.

For production resilience, evaluate per-AZ NAT Gateway design and the associated cost.

### Step 6 — Configure security groups

Create a load balancer security group and an application security group.

Example policy:

- Load balancer: allow inbound HTTPS from the intended client range.
- Application instances: allow only the required application port from the load balancer security group.
- SSH administration: avoid opening SSH broadly; use Systems Manager or a restricted administrative source when appropriate.

If this is a simple learning-only direct-to-EC2 test, restrict the web port to your IP and remove it after the test.

### Step 7 — Validate routes and traffic

Check:

- Public subnets have the correct IGW route.
- Private subnets do not have a direct IGW default route.
- If configured, the NAT Gateway is available and the private route targets it.
- Security-group rules match the intended traffic path.
- NACLs do not block required traffic.
- The application is listening on the expected port.
- DNS resolution and routing work independently.

### Step 8 — Add Flow Logs (optional)

Enable Flow Logs for the VPC or relevant subnet/network interface and send records to a suitable destination. Use a narrow filter around a test connection to practice interpreting accepted and rejected traffic.

### Step 9 — Clean up

Delete resources in dependency-aware order. Remove load balancers, NAT Gateways, Elastic IP allocations, instances, endpoints, and other resources created for the lab before deleting the VPC. Some resources must be deleted or detached before the VPC can be removed.

Review billing after the lab.

---

## 14. Troubleshooting checklist

### Instance cannot reach the internet

- Does the instance have a public IP if using direct IGW IPv4 access?
- Does the subnet route table have the intended default route?
- Is the IGW attached?
- If the instance is private, is there a working NAT route or VPC endpoint for the intended destination?
- Do security groups, NACLs, and host firewall allow the traffic?
- Does DNS resolution work?

### Internet client cannot reach a public instance

- Is the instance in a subnet with a route to the IGW?
- Does it have an appropriate public IP or Elastic IP?
- Does the security group allow the exact protocol and port from the client source?
- Do NACLs permit the inbound flow and return traffic?
- Is the application listening on the expected interface and port?
- Is the client using the correct address and protocol?

### Private instance cannot download packages

- Is the private route table targeting an available NAT Gateway, or is a suitable private endpoint configured?
- Is the NAT Gateway in a public subnet with an IGW route?
- Are outbound security-group and NACL rules sufficient, including return ephemeral ports for stateless ACLs?
- Does DNS resolve the package repository?
- Is the repository itself available?

### Load balancer targets are unhealthy

- Does the target application listen on the configured port?
- Does the health-check path return the expected response?
- Does the target security group allow traffic from the load balancer security group?
- Are the targets registered and in enabled AZs?
- Are host firewall rules and application logs consistent with the health-check failure?

### Flow Logs show `REJECT`

- Identify source, destination, protocol, port, interface, and timestamp.
- Check the security group and NACL associated with the flow.
- Check whether return traffic is blocked by stateless NACL rules.
- Verify that the log's scope and fields match the resource being investigated.

---

## 15. Security, resilience, and cost considerations

### Security

- Use least-privilege security-group rules.
- Prefer security-group references for tier-to-tier communication where appropriate.
- Avoid direct public exposure of application and database tiers.
- Keep administrative access restricted; consider Systems Manager Session Manager.
- Use VPC endpoints for supported AWS services when private access is suitable.
- Enable Flow Logs and retain them according to operational and compliance needs.
- Review routes and security rules regularly.

### Resilience

- Distribute production resources across multiple AZs where supported.
- Avoid relying on a single AZ for critical NAT or application paths without accepting the availability trade-off.
- Use load-balancer health checks and automated replacement where appropriate.
- Test failure scenarios and recovery procedures.
- Consider multi-Region architecture only when recovery objectives and business requirements justify the complexity.

### Cost

Potential costs include NAT Gateway hourly and data processing charges, public IPv4 usage, load balancers, data transfer, interface endpoints, and log ingestion/storage. A VPC itself may not be the primary cost driver, but the resources placed inside and connected to it can be.

Use AWS Budgets and billing tools to watch spend. Delete temporary resources after labs and confirm no orphaned NAT Gateways, Elastic IPs, load balancers, or endpoints remain.

---

## 16. AWS CLI quick reference

These examples require AWS CLI credentials with the appropriate permissions. They inspect resources and do not create or delete them.

```bash
# Confirm the active AWS identity
aws sts get-caller-identity

# List VPCs
aws ec2 describe-vpcs \
  --query 'Vpcs[].[VpcId,CidrBlock,State,IsDefault]' \
  --output table

# List subnets
aws ec2 describe-subnets \
  --query 'Subnets[].[SubnetId,VpcId,CidrBlock,AvailabilityZone,MapPublicIpOnLaunch]' \
  --output table

# List route tables and routes
aws ec2 describe-route-tables \
  --query 'RouteTables[].[RouteTableId,VpcId,Routes]' \
  --output json

# List Internet Gateways and attachments
aws ec2 describe-internet-gateways \
  --output table

# List NAT Gateways
aws ec2 describe-nat-gateways \
  --query 'NatGateways[].[NatGatewayId,VpcId,SubnetId,State]' \
  --output table

# List security groups
aws ec2 describe-security-groups \
  --query 'SecurityGroups[].[GroupId,GroupName,VpcId]' \
  --output table

# List VPC Flow Logs
aws ec2 describe-flow-logs \
  --query 'FlowLogs[].[FlowLogId,ResourceId,TrafficType,LogDestinationType,FlowLogStatus]' \
  --output table
```

To inspect one route table:

```bash
aws ec2 describe-route-tables \
  --route-table-ids rtb-REPLACE_WITH_ID
```

Replace placeholders with real IDs. Confirm the configured Region and account before running operational commands.

---

## 17. Assignment

### Task A — Networking fundamentals

1. Define a VPC, subnet, CIDR, route table, IGW, NAT Gateway, security group, NACL, and Flow Logs.
2. Explain the gated-community analogy and where it has limitations.
3. Calculate the total IPv4 addresses and usable addresses in a `/24` subnet under AWS's standard IPv4 reservation rule.

### Task B — Address planning

1. Design a VPC with at least four non-overlapping subnets across two AZs.
2. Document CIDR, subnet name, AZ, route table, and purpose.
3. Explain how you would avoid overlap with a corporate network.

### Task C — Route design

1. Draw the traffic path from an internet client to a public load balancer.
2. Draw the path from a private EC2 instance to an external package repository through a NAT Gateway.
3. Explain why a NAT Gateway does not allow arbitrary inbound internet connections to the private instance.

### Task D — Security

1. Design load balancer, application, and database security groups.
2. Explain stateful security groups vs. stateless NACLs.
3. Identify the risks of allowing SSH from `0.0.0.0/0`.
4. Explain how VPC Flow Logs can help investigate a rejected connection.

### Task E — Hands-on implementation

Create a learning VPC, subnets, IGW, and route tables. Add a NAT Gateway only if the lab requires outbound internet access and you have checked the cost. Validate the network paths and then remove temporary resources.

### Evidence for GitHub

Include:

- A network diagram.
- CIDR/subnet table.
- Screenshots of route tables and security-group rules (redact account-sensitive information).
- A short connectivity test and explanation.
- Flow Log example, if enabled.
- Cleanup checklist.

Never include credentials, private keys, or secrets in the repository.

---

## 18. Interview questions

**1. What is Amazon VPC?**  
A logically isolated virtual network in AWS where you define IP ranges, subnets, routing, and network security controls.

**2. What makes a subnet public?**  
Conventionally, its associated route table includes a route to an Internet Gateway for internet-bound traffic. Resources still need appropriate public addressing and permitted network rules to be reachable.

**3. What is the difference between a public and private subnet?**  
The key distinction is routing, especially whether the subnet has a direct route to an IGW. A private subnet may still have outbound access through NAT or private connectivity.

**4. What does a route table do?**  
It selects the next hop for traffic based on destination IP prefixes.

**5. What is an Internet Gateway?**  
A VPC component that enables internet routing for appropriately configured resources.

**6. What is a NAT Gateway?**  
A managed service that allows private resources to initiate supported outbound connections without making those resources directly reachable for unsolicited inbound internet connections through NAT.

**7. Does a public subnet automatically make an EC2 instance public?**  
No. The instance also needs suitable addressing, security rules, host configuration, and a working route.

**8. What is the difference between a security group and a NACL?**  
Security groups are stateful and associated with network interfaces; NACLs are stateless subnet-level filters with numbered allow/deny rules.

**9. Why might a private instance fail to download packages?**  
It may lack a NAT route or suitable endpoint, the NAT path may be broken, DNS may fail, or security rules may block the flow.

**10. What is VPC Flow Logs used for?**  
To capture metadata about IP traffic for network troubleshooting, visibility, and security analysis.

**11. Are Flow Logs packet captures?**  
No. They provide flow metadata, not full packet payloads.

**12. Why use multiple Availability Zones?**  
To reduce dependence on a single isolated infrastructure location and improve resilience when the application and data architecture support multi-AZ operation.

**13. Why can overlapping VPC CIDRs be a problem?**  
Overlapping address ranges complicate or prevent routing between connected networks, such as VPC peering, VPN, and corporate networks.

**14. How can a database be protected in a VPC?**  
Place it in private or isolated subnets, restrict its security group to the application tier, use encryption and authentication, patch it, and monitor access.

**15. How would you troubleshoot a failed connection?**  
Check DNS, routes, addressing, security groups, NACLs, host firewall, listening service, and logs in a systematic order.

---

## 19. Further reading

Use the official documentation as the source of truth for service behavior, supported configurations, and current pricing.

- [Amazon VPC User Guide](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)
- [VPC CIDR blocks](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-cidr-blocks.html)
- [Subnet route tables](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Route_Tables.html)
- [Internet Gateways](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html)
- [NAT Gateways](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html)
- [Security groups](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html)
- [Network ACLs](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html)
- [VPC Flow Logs](https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html)
- [Elastic Load Balancing](https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/what-is-load-balancing.html)
- [AWS VPC pricing](https://aws.amazon.com/vpc/pricing/)
- [AWS DevOps Zero to Hero repository](https://github.com/iam-veeramalla/aws-devops-zero-to-hero)

---

## Lesson summary

Amazon VPC provides the network foundation for AWS workloads. CIDR blocks define address space, subnets segment that space by purpose and Availability Zone, and route tables determine where traffic travels. Internet Gateways support internet routing for public resources, while NAT Gateways enable supported outbound IPv4 connections from private subnets. Security groups, NACLs, load balancers, DNS, and Flow Logs contribute to controlled connectivity and operational visibility.

The key lesson is that **network reachability is the result of multiple layers working together**. A route alone does not guarantee access, and a subnet name alone does not determine whether a resource is public. Design, validate, monitor, and clean up each layer deliberately.
