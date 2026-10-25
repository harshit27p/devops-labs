# Day 05 — AWS Network Security: Security Groups and Network ACLs

> **Series:** AWS DevOps Zero to Hero  
> **Instructor:** Abhishek Veeramalla  
> **Video:** [Watch the networking security session](https://www.youtube.com/watch?v=TtlKFgfN3PU&list=PLdpzxOOAlwvIc1TjTwopNSjRJkzES2ZXk&index=59)  
> **Curriculum reference:** [aws-devops-zero-to-hero](https://github.com/iam-veeramalla/aws-devops-zero-to-hero)  
> **Focus:** Shared responsibility, Security Groups, Network ACLs (NACLs), rule evaluation, and a Python HTTP server lab on port 8000.

This guide expands the supplied video outline into practical notes and troubleshooting exercises. It focuses on network filtering behavior rather than repeating the full VPC and CIDR introduction from the previous lesson.

---

## Contents

- [1. Learning objectives](#1-learning-objectives)
- [2. Security in AWS: shared responsibility](#2-security-in-aws-shared-responsibility)
- [3. How network filtering works](#3-how-network-filtering-works)
- [4. Security Groups](#4-security-groups)
- [5. Network ACLs (NACLs)](#5-network-acls-nacls)
- [6. Security Groups vs. NACLs](#6-security-groups-vs-nacls)
- [7. Rule evaluation and ephemeral ports](#7-rule-evaluation-and-ephemeral-ports)
- [8. Hands-on lab: Python HTTP server on port 8000](#8-hands-on-lab-python-http-server-on-port-8000)
- [9. Demonstrate a Security Group block](#9-demonstrate-a-security-group-block)
- [10. Demonstrate a NACL block](#10-demonstrate-a-nacl-block)
- [11. Troubleshooting workflow](#11-troubleshooting-workflow)
- [12. Production security patterns](#12-production-security-patterns)
- [13. AWS CLI reference](#13-aws-cli-reference)
- [14. Assignment](#14-assignment)
- [15. Interview questions](#15-interview-questions)
- [16. Further reading](#16-further-reading)

---

## 1. Learning objectives

After completing this lesson, you should be able to:

1. Explain AWS's shared responsibility model.
2. Describe where Security Groups and NACLs apply.
3. Explain stateful versus stateless traffic filtering.
4. Understand that Security Groups allow traffic while NACLs support both allow and deny rules.
5. Explain numbered NACL rule evaluation and why rule order matters.
6. Configure a safe temporary test server on TCP port 8000.
7. Diagnose a connection failure caused by routing, Security Groups, NACLs, host firewalls, or a service that is not listening.
8. Apply least-privilege network rules to a multi-tier application.

### Prerequisites

- An AWS account with permission to create VPC, subnet, EC2, Security Group, and NACL resources.
- A custom VPC with a public subnet and suitable routing for the lab.
- SSH access to a Linux EC2 instance.
- Basic IP addressing, TCP, ports, and route-table knowledge.
- Awareness that EC2, public IPv4 addresses, storage, data transfer, and other resources may incur charges.

---

## 2. Security in AWS: shared responsibility

AWS security follows a **shared responsibility model**. AWS is responsible for security **of** the cloud, while the customer is responsible for security **in** the cloud, with exact boundaries depending on the service.

### AWS responsibilities commonly include

- Physical security of AWS data centers.
- Physical servers, storage devices, and networking infrastructure.
- Security and maintenance of the underlying virtualization infrastructure.
- Resilience of the managed infrastructure that AWS operates.

### Customer responsibilities for EC2 commonly include

- Configuring Security Groups and NACLs.
- Selecting and securing the guest operating system.
- Installing patches and maintaining software.
- Managing IAM identities and permissions.
- Protecting credentials, keys, and secrets.
- Securing applications and exposed ports.
- Configuring logging, monitoring, backups, and incident response.

### Why this matters for network security

Launching an EC2 instance in AWS does not automatically make the application secure. AWS provides network controls, but the customer must configure them appropriately. An overly permissive Security Group or NACL is a configuration risk even when the underlying AWS infrastructure is secure.

---

## 3. How network filtering works

When a client connects to an application on an EC2 instance, multiple controls may be involved:

```text
Client
  |
  v
Internet / connected network
  |
  v
VPC routing and subnet route table
  |
  v
Network ACL (subnet boundary, stateless)
  |
  v
Security Group (network interface, stateful)
  |
  v
Host firewall (e.g. UFW / firewalld / iptables/nftables)
  |
  v
Application listening on TCP port 8000
```

The response follows the network path in reverse, and the filtering behavior depends on each control:

- **Security Group:** Stateful connection tracking permits response traffic for an allowed connection.
- **NACL:** Stateless rules independently evaluate inbound and outbound packets, including response traffic.
- **Route tables:** Determine the next hop for the destination; they do not grant application-level permission.
- **Host firewall:** May allow or block traffic after it reaches the instance.
- **Application:** Must be running and listening on the expected address and port.

A connection succeeds only when all required parts of the path are correctly configured.

---

## 4. Security Groups

A **Security Group** is a stateful virtual firewall associated with an EC2 network interface or another supported AWS resource. It controls allowed inbound and outbound traffic.

### Key characteristics

- Security Groups contain allow rules; they do not have explicit deny rules.
- Inbound traffic is denied unless an inbound rule allows it.
- Outbound behavior depends on the group's outbound rules; default-created groups commonly allow all outbound traffic, but custom groups can be more restrictive.
- Security Groups are stateful: return traffic for an allowed connection is automatically permitted, even if there is no matching outbound rule for that response.
- Rules from all Security Groups associated with a network interface are combined.
- A rule can specify protocol, port or port range, and source/destination such as a CIDR or another Security Group.

### Example: allow HTTP test traffic

Suppose a Python server listens on TCP port 8000. A narrowly scoped inbound rule might be:

| Setting | Value |
|---|---|
| Type | Custom TCP |
| Protocol | TCP |
| Port | 8000 |
| Source | Your current public IP `/32` for a temporary test |
| Purpose | Permit only your client to reach the test server |

For a public demonstration intended for all IPv4 clients, `0.0.0.0/0` would allow any IPv4 source to attempt a connection on that port. Avoid this unless the service is intentionally public and suitably protected. A temporary lab should prefer a restricted source.

### Example: tier-to-tier access

For a production-like design:

- Load balancer Security Group: permits HTTPS from intended clients.
- Application Security Group: permits the app port only from the load balancer Security Group.
- Database Security Group: permits the database port only from the application Security Group.

This reduces unnecessary direct access between tiers.

---

## 5. Network ACLs (NACLs)

A **Network Access Control List (NACL)** is a stateless traffic filter associated with a subnet. It provides a subnet-level layer of network control.

### Key characteristics

- NACLs support both allow and deny rules.
- Rules are numbered and evaluated in ascending order.
- The first matching rule determines the result.
- Inbound and outbound traffic are evaluated independently.
- NACLs are stateless: response traffic must be permitted by the rules in the opposite direction.
- Each subnet is associated with one NACL at a time. If you do not explicitly associate a custom NACL, the VPC's default NACL applies.
- A custom NACL typically starts with rules that deny traffic unless you add rules to allow it. The default NACL is initially permissive, but its rules can be changed.

### Example: allow TCP 8000 from a test client

An inbound NACL rule could allow TCP destination port 8000 from the test client's public IP. But the full flow also requires outbound rules for response traffic to the client's ephemeral port range.

Because the NACL is stateless, allowing only inbound destination port 8000 is not enough to ensure the HTTP response can return.

### Why NACL rule order matters

Suppose the inbound rules are:

| Rule number | Type | Source | Action |
|---:|---|---|---|
| 100 | Custom TCP 8000 | `203.0.113.10/32` | DENY |
| 110 | Custom TCP 8000 | `0.0.0.0/0` | ALLOW |
| `*` | All traffic | `0.0.0.0/0` | DENY |

Traffic from `203.0.113.10` matches rule 100 first and is denied. The broader allow rule 110 is not evaluated for that packet. The example uses a documentation-only IP range; replace it only with the appropriate source in a real configuration.

**Rule order principle:** A lower rule number is evaluated first. The first matching rule wins.

---

## 6. Security Groups vs. NACLs

| Feature | Security Group | Network ACL |
|---|---|---|
| Scope | Network interface/resource | Subnet |
| Stateful? | Yes | No |
| Supports explicit deny? | No | Yes |
| Rule evaluation | All applicable allow rules are combined | Numbered rules; first match wins |
| Return traffic | Automatically allowed for tracked connections | Must be allowed separately in the reverse direction |
| Default behavior | Inbound denied unless allowed; outbound depends on configured rules | Default NACL is initially permissive; a custom NACL starts restrictive |
| Common purpose | Primary workload-level access control | Additional subnet-level filtering and explicit deny rules |

### Can a NACL block traffic allowed by a Security Group?

Yes. Both controls must permit the flow. If a Security Group allows TCP 8000 but the subnet's NACL denies the incoming packet, the connection is blocked. Likewise, a permissive NACL does not override a Security Group that lacks a matching allow rule.

Think of them as separate checkpoints, not as competing controls where one grants universal permission over the other.

---

## 7. Rule evaluation and ephemeral ports

### Security Group connection tracking

For an allowed inbound TCP connection to port 8000, the Security Group tracks the connection and permits response traffic. You do not need to create a separate Security Group outbound rule solely for the return packets of that tracked connection, though the overall outbound policy still matters for connections initiated by the instance.

### NACL inbound and outbound rules

A client typically connects from a temporary client-side source port (an ephemeral port) to server destination port 8000. The server response uses source port 8000 and destination port equal to the client's ephemeral port.

Conceptually:

```text
Request:
Client_IP:ephemeral_port  --->  Server_IP:8000

Response:
Server_IP:8000            --->  Client_IP:ephemeral_port
```

For a stateless NACL, rules must permit both directions. The required ephemeral port range depends on the client operating system and connection path; do not assume one universal range is correct for every client. Use the appropriate documented range for the environment and restrict source/destination CIDRs where practical.

### Common mistakes

- Allowing inbound TCP 8000 but forgetting NACL outbound response traffic.
- Adding a broad allow rule above a deny rule and assuming the deny will still apply.
- Modifying the wrong NACL or subnet association.
- Testing from a client whose public IP differs from the allowed CIDR.
- Assuming a Security Group rule can override a NACL deny.
- Forgetting that a host firewall can block traffic after AWS network controls permit it.

---

## 8. Hands-on lab: Python HTTP server on port 8000

### Objective

Launch a Linux EC2 instance in a public subnet, run a simple Python HTTP server on TCP port 8000, and test the impact of Security Group and NACL rules.

> **Safety:** Use a disposable lab instance and a restricted client source CIDR. Python's simple HTTP server is for testing, not production hosting. Do not expose sensitive files from the server's working directory.

### Architecture

```text
Your workstation
      |
      | TCP 8000
      v
Internet Gateway
      |
      v
Public subnet NACL
      |
      v
EC2 Security Group
      |
      v
Linux EC2
      |
      v
Python HTTP server :8000
```

### Step 1 — Prepare the EC2 instance

1. Use the custom VPC and public subnet from the VPC lesson, or create a dedicated lab VPC.
2. Confirm the subnet route table has an IPv4 default route to an attached Internet Gateway.
3. Launch a Linux EC2 instance with a suitable public IPv4 address.
4. Create a dedicated Security Group.
5. Allow SSH (TCP 22) only from your current public IP `/32`.
6. Initially, do not allow inbound TCP 8000. You will add the rule as part of the experiment.
7. Confirm the instance is running and status checks pass.

Do not reuse a production instance or modify production NACLs for this experiment.

### Step 2 — Connect using SSH

For an Ubuntu AMI:

```bash
ssh -i /path/to/lab-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

Replace the key path and public IP with the real values. The default SSH username varies by AMI.

### Step 3 — Check Python

```bash
python3 --version
```

If Python 3 is not installed, install it using the package manager for the instance's Linux distribution. For Ubuntu:

```bash
sudo apt update
sudo apt install -y python3
```

### Step 4 — Create a safe test directory

```bash
mkdir -p ~/http-lab
cd ~/http-lab
printf 'Hello from the EC2 Python HTTP lab\n' > index.html
```

Use a dedicated directory with only files intended to be served.

### Step 5 — Start the HTTP server

```bash
python3 -m http.server 8000 --bind 0.0.0.0
```

The `0.0.0.0` bind address makes the test server listen on all IPv4 interfaces. Keep the Security Group restricted to your client IP and stop the server when done. This is a simple development server and should not be used as a production service.

Leave the process running in this SSH session. To stop it, press `Ctrl+C`.

### Step 6 — Test from the EC2 instance

Open another SSH session, then run:

```bash
curl -I http://127.0.0.1:8000/
curl http://127.0.0.1:8000/
sudo ss -lntp | grep ':8000'
```

Expected behavior: `curl` receives an HTTP response and the port check shows a listener on TCP 8000. If localhost works but external access fails, investigate the network path.

### Step 7 — Test before changing the Security Group

From your workstation:

```bash
curl --connect-timeout 5 http://YOUR_EC2_PUBLIC_IP:8000/
```

Because the inbound Security Group rule is absent, the request should not be allowed through that Security Group. A timeout is common; exact client behavior can vary.

### Step 8 — Add the Security Group rule

In the AWS Console:

1. Open EC2 → Instances.
2. Select the lab instance.
3. Open its Security tab and select the Security Group.
4. Choose Edit inbound rules.
5. Add Custom TCP, port `8000`, source your current public IP `/32`.
6. Save the rule.

Repeat the client test. If the route, NACL, host firewall, and server are correctly configured, the request should now succeed.

### Step 9 — Record the result

| Test | Security Group TCP 8000 | NACL permits flow | Expected outcome |
|---|---|---|---|
| A | No matching allow | Yes | Blocked by Security Group |
| B | Allowed from your IP | Yes | HTTP response expected |
| C | Allowed from your IP | Inbound NACL denies | Blocked by NACL |
| D | Allowed from your IP | Inbound allowed, response path denied | Request may time out because response is blocked |

These are expected outcomes assuming the remaining route, host firewall, and service configuration is correct.

---

## 9. Demonstrate a Security Group block

1. Confirm the Python server is running and reachable locally.
2. Remove the inbound TCP 8000 rule from the instance's Security Group.
3. From your workstation, request `http://YOUR_EC2_PUBLIC_IP:8000/`.
4. Record the failure.
5. Restore the rule restricted to your current public IP `/32`.
6. Retry and record the successful response.

### What this demonstrates

The application can be healthy and listening while AWS network access is denied by the Security Group. Application health and network reachability are different things.

Do not remove SSH access while connected unless you have another supported management method configured.

---

## 10. Demonstrate a NACL block

> **Caution:** NACL changes affect every resource in the associated subnet, not just the one EC2 instance. Use a dedicated lab subnet and a dedicated custom NACL. Do not experiment with a shared or production subnet's NACL.

### Step 1 — Identify the subnet's NACL

1. Open the VPC Console.
2. Select Subnets and identify the EC2 instance's subnet.
3. Open the subnet's Network ACL association.
4. Confirm that it is a dedicated lab NACL and note the current rules.
5. Keep a record of the original configuration so you can restore it.

### Step 2 — Add a narrowly scoped deny rule

For an isolated lab, add an inbound NACL deny rule for TCP destination port 8000 from the test client's public IP CIDR, using a rule number that is evaluated before any broader allow rule.

Example logic:

| Rule number | Protocol | Port | Source | Action |
|---:|---|---:|---|---|
| 100 | TCP | 8000 | Your client IP `/32` | DENY |
| 110 | TCP | 8000 | Intended allowed CIDR | ALLOW |
| `*` | All | All | `0.0.0.0/0` | DENY (implicit final rule) |

The table is illustrative. NACL rules must be consistent with the existing rule set, and the deny should be limited to the intended test flow. Avoid accidentally denying SSH or other required traffic.

### Step 3 — Test

With the Security Group still permitting TCP 8000 from your IP, retry the HTTP request. The NACL deny should block the incoming packet.

### Step 4 — Restore the lab

1. Remove the temporary deny rule or restore the original rule set.
2. Confirm the HTTP test works again.
3. Verify SSH remains available.
4. Stop the Python server with `Ctrl+C`.
5. Remove the temporary TCP 8000 Security Group rule when finished.

### Why does the NACL block win?

The packet must pass both the subnet-level NACL and the network-interface Security Group. A Security Group allow rule does not override a NACL deny rule. The packet is rejected at the NACL boundary before the application receives it.

### Optional extension: demonstrate stateless return traffic

This is a more advanced test and should be performed only in the dedicated lab subnet. A NACL must permit the response direction to the client's ephemeral source port. If inbound traffic is allowed but the corresponding outbound response is denied, the client may send the request but never receive a usable response.

Restore the original NACL immediately after the experiment.

---

## 11. Troubleshooting workflow

When a connection to TCP 8000 fails, troubleshoot from the outside inward and change one variable at a time.

### Checklist

1. **Client:** Is the client using the correct public IP and TCP port?
2. **Instance:** Is the instance running and passing status checks?
3. **Route:** Does the subnet have a valid route to an attached Internet Gateway?
4. **Public addressing:** Does the instance have a public IPv4 address or Elastic IP?
5. **NACL:** Are inbound TCP 8000 and the necessary outbound return traffic permitted?
6. **Security Group:** Does an associated Security Group allow TCP 8000 from the actual client IP?
7. **Host firewall:** Is UFW, firewalld, or another host firewall blocking the port?
8. **Application:** Is Python listening on `0.0.0.0:8000` and serving the intended directory?
9. **Logs and telemetry:** Check VPC Flow Logs if enabled and inspect host-level state.

### Useful commands on the EC2 instance

```bash
# Verify the listener
sudo ss -lntp | grep ':8000'

# Test the local server
curl -v http://127.0.0.1:8000/

# Inspect interfaces and routes
ip address
ip route

# Ubuntu host firewall (if UFW is installed)
sudo ufw status verbose

# Recent system messages
sudo journalctl -n 100 --no-pager
```

### Interpret common outcomes

| Observation | Possible explanation |
|---|---|
| Local `curl` fails | Server is stopped, listening on the wrong port/address, or serving process has an error |
| Local works; external request times out | Security Group, NACL, route, public address, or upstream network issue |
| External request is refused | Host reachable but no listener or a local control rejects it; investigate the path and service |
| SSH fails after NACL changes | NACL may have blocked TCP 22 or the SSH return path |
| Works from one client but not another | Source CIDR, client egress policy, VPN, or route differences |
| Request reaches instance but response fails | Host firewall, NACL outbound rules, routing, or server behavior |

A timeout alone does not identify which control blocked traffic. Combine configuration inspection with logs and controlled tests.

---

## 12. Production security patterns

### Use least privilege

- Permit only required ports and source ranges.
- Prefer Security Group references for tier-to-tier access.
- Avoid exposing management ports to the whole internet.
- Remove temporary rules after a lab.
- Review inbound and outbound rules periodically.

### Layer controls deliberately

Use Security Groups as the main workload-level network control. Use NACLs when subnet-level allow/deny requirements justify them. Avoid duplicating complex rules without a clear reason, because inconsistent NACLs can make troubleshooting harder.

### Protect administrative access

- Use AWS Systems Manager Session Manager where suitable and configured.
- If using SSH, restrict source CIDRs and protect private keys.
- Use IAM roles and temporary credentials rather than long-lived keys on instances.
- Enable appropriate logging and alerting.

### Monitor and investigate

- Enable VPC Flow Logs for relevant resources.
- Retain logs according to operational and compliance needs.
- Correlate network telemetry with application and host logs.
- Test security changes in a non-production environment first.

### Remember the limits

Security Groups and NACLs are network filters, not application authentication. A port being reachable does not mean the application is secure. Use TLS, authentication, patching, secrets management, and application-level authorization as required.

---

## 13. AWS CLI reference

These read-only commands require AWS CLI and suitable IAM permissions. Confirm the configured account and Region before inspecting or changing resources.

```bash
# Confirm the active identity
aws sts get-caller-identity

# List Security Groups
aws ec2 describe-security-groups \
  --query 'SecurityGroups[].[GroupId,GroupName,VpcId]' \
  --output table

# Inspect one Security Group
aws ec2 describe-security-groups \
  --group-ids sg-REPLACE_WITH_ID

# List network ACLs
aws ec2 describe-network-acls \
  --query 'NetworkAcls[].[NetworkAclId,VpcId,IsDefault]' \
  --output table

# Inspect NACL entries and subnet associations
aws ec2 describe-network-acls \
  --network-acl-ids acl-REPLACE_WITH_ID

# List subnets and their AZs
aws ec2 describe-subnets \
  --query 'Subnets[].[SubnetId,VpcId,CidrBlock,AvailabilityZone]' \
  --output table

# Inspect route tables
aws ec2 describe-route-tables \
  --query 'RouteTables[].[RouteTableId,VpcId,Associations,Routes]' \
  --output json
```

Replace the placeholder IDs with actual IDs. These commands inspect configuration; they do not prove that an application is listening or that the entire end-to-end network path works.

---

## 14. Assignment

### Task A — Explain the concepts

1. Define shared responsibility in AWS.
2. Explain why Security Groups are stateful.
3. Explain why NACLs are stateless.
4. Describe how NACL rule order works.
5. Explain why a NACL can block traffic that a Security Group allows.

### Task B — Python HTTP lab

1. Launch a disposable Linux instance in a dedicated public subnet.
2. Run a Python HTTP server on TCP 8000 in a dedicated directory.
3. Test local access from the instance.
4. Test external access before and after adding a restricted Security Group rule.
5. Document the results and cleanup.

### Task C — NACL experiment

1. Create or select a dedicated lab NACL.
2. Associate it only with the lab subnet.
3. Add a narrow inbound deny rule for the test client and port 8000.
4. Confirm the request fails while the Security Group still allows it.
5. Remove the deny rule and verify access is restored.
6. Explain how stateless return traffic affects NACL design.

### Task D — Security review

Design a rule set for a public load balancer, private application servers, and a database. Explain which controls belong in Security Groups, which NACL rules are justified, and how administrators should connect.

### Evidence to include in your GitHub submission

- A simple network diagram.
- Security Group rules before and after the test.
- NACL rule table showing rule numbers and actions.
- Sanitized terminal output from local and external tests.
- A brief explanation of each result.
- Cleanup checklist.

Never commit private keys, AWS credentials, passwords, or sensitive network details to a public repository.

---

## 15. Interview questions

**1. What is the difference between a Security Group and a NACL?**  
A Security Group is stateful and associated with network interfaces; a NACL is stateless and applied at the subnet boundary.

**2. Can a Security Group explicitly deny traffic?**  
No. Security Groups define allowed traffic; traffic not allowed by the combined rules is denied.

**3. Can a NACL explicitly deny traffic?**  
Yes. NACLs support numbered allow and deny rules.

**4. What happens when two NACL rules match a packet?**  
Rules are evaluated in ascending numeric order and the first matching rule determines the action.

**5. Why must NACLs allow return traffic?**  
They are stateless, so inbound permission does not automatically permit the outbound response. The reverse-direction rules must allow it.

**6. Why can an EC2 application be unreachable even when the Security Group allows its port?**  
The route, public address, NACL, host firewall, or application listener may be incorrect.

**7. Why is opening TCP 8000 to `0.0.0.0/0` risky?**  
It permits any IPv4 source to attempt connections to that port. The application must be intended for public access and appropriately secured.

**8. What does a timeout indicate?**  
A timeout suggests that the connection did not complete in time, but it does not identify the cause. Investigate the full network path.

**9. Why is a Python simple HTTP server unsuitable for production?**  
It is a basic development/testing server and lacks the hardening, operational features, and production architecture expected of a real service.

**10. How would you reduce administrative exposure?**  
Restrict management sources, use Systems Manager Session Manager where appropriate, protect credentials, and monitor administrative access.

**11. What is the shared responsibility model?**  
AWS secures the underlying cloud infrastructure, while customers secure their workloads and configurations according to the service model.

**12. Should NACLs replace Security Groups?**  
No. They operate at different scopes and have different semantics. Security Groups are usually the primary workload-level control; NACLs can provide additional subnet-level filtering.

---

## 16. Further reading

- [AWS Shared Responsibility Model](https://aws.amazon.com/compliance/shared-responsibility-model/)
- [Amazon EC2 Security Groups](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-security-groups.html)
- [VPC Security Groups](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html)
- [Network ACLs](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html)
- [VPC Flow Logs](https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html)
- [Amazon VPC User Guide](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)
- [Python http.server documentation](https://docs.python.org/3/library/http.server.html)
- [AWS DevOps Zero to Hero repository](https://github.com/iam-veeramalla/aws-devops-zero-to-hero)

---

## Lesson summary

Security Groups and NACLs are complementary AWS network controls. Security Groups provide stateful allow rules at the network-interface/resource level. NACLs provide stateless subnet-level allow and deny rules evaluated in numerical order. Both must permit the required traffic, and routing, public addressing, host firewalls, and the application itself must also be configured correctly.

The Python HTTP lab demonstrates the difference between an application listening on a port and that port being reachable from a client. Make narrow changes in a dedicated test environment, validate each result, and restore the network configuration when the experiment is complete.
