# Day 03 — Amazon EC2: Launch a Cloud Server and Deploy Jenkins

> **Series:** AWS DevOps Zero to Hero  
> **Instructor:** Abhishek Veeramalla  
> **Video:** [Watch the EC2 session](https://www.youtube.com/watch?v=Dc0t4LDOySY&list=PLdpzxOOAlwvIc1TjTwopNSjRJkzES2ZXk&index=57)  
> **Curriculum reference:** [aws-devops-zero-to-hero](https://github.com/iam-veeramalla/aws-devops-zero-to-hero)  
> **Focus:** EC2 fundamentals, instance selection, SSH access, security groups, and deploying Jenkins on Ubuntu.

This guide follows the topics in the supplied video summary and expands them into a practical, reusable lab. AWS Console labels and available instance types can change, so verify the current options in your chosen Region before launching resources.

---

## Contents

- [1. Learning objectives](#1-learning-objectives)
- [2. What is Amazon EC2?](#2-what-is-amazon-ec2)
- [3. Where EC2 fits in AWS](#3-where-ec2-fits-in-aws)
- [4. EC2 instance types](#4-ec2-instance-types)
- [5. Regions and Availability Zones](#5-regions-and-availability-zones)
- [6. Important EC2 components](#6-important-ec2-components)
- [7. Security groups and network access](#7-security-groups-and-network-access)
- [8. Hands-on lab: launch Ubuntu EC2](#8-hands-on-lab-launch-ubuntu-ec2)
- [9. Connect to EC2 using SSH](#9-connect-to-ec2-using-ssh)
- [10. Install Java and Jenkins](#10-install-java-and-jenkins)
- [11. Open Jenkins safely](#11-open-jenkins-safely)
- [12. Validate the deployment](#12-validate-the-deployment)
- [13. Troubleshooting guide](#13-troubleshooting-guide)
- [14. Security and production considerations](#14-security-and-production-considerations)
- [15. Cost awareness and cleanup](#15-cost-awareness-and-cleanup)
- [16. EC2 CLI quick reference](#16-ec2-cli-quick-reference)
- [17. Assignment](#17-assignment)
- [18. Interview questions](#18-interview-questions)
- [19. Further reading](#19-further-reading)

---

## 1. Learning objectives

By the end of this lesson, you should be able to:

1. Explain the purpose of Amazon EC2 and when to use virtual machines.
2. Select an instance family based on workload requirements.
3. Explain AWS Regions and Availability Zones.
4. Describe AMIs, instance types, EBS volumes, key pairs, and security groups.
5. Launch an Ubuntu instance from the AWS Console.
6. Connect to Linux using SSH and a private key.
7. Install Java and Jenkins on Ubuntu.
8. diagnose common SSH, package installation, service, and browser connectivity issues.
9. Apply basic security and cost controls to a lab instance.

### Prerequisites

- An AWS account with permission to launch EC2 resources.
- A Region selected in the AWS Console.
- A local terminal: Linux/macOS Terminal, Windows PowerShell, or Windows Terminal with OpenSSH.
- Basic Linux commands and SSH familiarity.
- Awareness that EC2, EBS storage, public IPv4 addresses, data transfer, and related resources may incur charges.

---

## 2. What is Amazon EC2?

**Amazon Elastic Compute Cloud (Amazon EC2)** provides resizable compute capacity in the AWS Cloud. An EC2 instance is a virtual server that you can configure for applications, web servers, automation tools, databases, build agents, and other workloads.

With a traditional physical server, an organization may need to purchase hardware, install it in a data center, provision power and cooling, and maintain the physical infrastructure. With EC2, AWS operates the underlying cloud infrastructure while the customer chooses and manages the guest operating system and software according to the selected service model.

### Traditional server vs. EC2

| Area | Traditional on-premises server | Amazon EC2 |
|---|---|---|
| Initial provisioning | Hardware procurement and setup | Provision an instance through console, API, CLI, or IaC |
| Capacity changes | May require purchasing hardware | Resize or replace instances as workload needs change |
| Physical facility | Organization manages or contracts it | AWS manages the physical AWS infrastructure |
| OS and application | Customer-managed | Generally customer-managed for EC2 |
| Billing | Capital and operational expenses | Usage-based billing, depending on purchasing option |
| Availability | Designed by the organization | Can use multiple AZs and managed AWS services |
| Responsibility | Depends on owned/hosted environment | Shared between AWS and customer |

EC2 reduces the need to own physical compute hardware, but it does **not** remove the need to patch operating systems, secure applications, configure access, monitor utilization, or control costs.

### Typical EC2 use cases

- Hosting a web application or API.
- Running Jenkins or another CI/CD tool.
- Build agents and automation runners.
- Development, testing, and staging environments.
- Self-managed software that needs OS-level control.
- Batch processing and data workloads.
- Lift-and-shift migration of existing applications.

### EC2 lifecycle, conceptually

```text
Choose Region and AZ
        |
        v
Choose AMI + instance type
        |
        v
Configure network, IAM role, storage, security group
        |
        v
Launch instance
        |
        v
Connect, configure OS and install application
        |
        v
Monitor, patch, back up, scale, and maintain
        |
        v
Stop or terminate when no longer needed
```

---

## 3. Where EC2 fits in AWS

EC2 is a compute service. A real application usually relies on multiple services working together.

```text
Developer / Administrator
          |
          | HTTPS / SSH
          v
Internet or corporate network
          |
          v
VPC (virtual network)
  |
  +-- Subnet in an Availability Zone
  |       |
  |       +-- Security Group
  |               |
  |               +-- EC2 instance
  |                       |
  |                       +-- Ubuntu Linux
  |                               |
  |                               +-- Java runtime
  |                               +-- Jenkins
  |
  +-- Route table / Internet Gateway / other network components
```

The diagram is conceptual. The exact routing components depend on whether the instance is public or private and how it is accessed.

### Related AWS services

- **Amazon VPC:** Isolated logical network for AWS resources.
- **Amazon EBS:** Persistent block storage commonly attached to EC2.
- **IAM:** Controls who or what can call AWS APIs.
- **Security Groups:** Stateful virtual firewalls attached to network interfaces.
- **Elastic IP:** Static public IPv4 address resource, subject to AWS pricing rules.
- **Elastic Load Balancing:** Distributes traffic among registered targets.
- **Auto Scaling:** Adjusts the number of instances according to desired capacity and policies.
- **CloudWatch:** Collects metrics, logs, and alarms.
- **Systems Manager:** Supports managed operations such as Session Manager, when prerequisites are configured.

These services will receive deeper treatment in later lessons; this page introduces only their relationship to EC2.

---

## 4. EC2 instance types

An **instance type** defines a combination of compute, memory, storage, and networking capabilities. Choose one according to measured workload needs rather than selecting the largest available machine.

| Family | Optimized for | Example workloads |
|---|---|---|
| General purpose | Balanced CPU, memory, and networking | Small applications, development environments, web servers |
| Compute optimized | High CPU performance | CPU-heavy services, batch processing, scientific workloads |
| Memory optimized | Large memory capacity | In-memory databases, analytics, caching |
| Storage optimized | High local storage throughput or I/O | Distributed storage, data processing, high-I/O workloads |
| Accelerated computing | GPUs or specialized accelerators | ML inference/training, graphics, video processing |
| High-performance computing | Tightly coupled compute workloads | Engineering simulation and HPC workloads |

### Instance type naming

An instance type name often contains a family, generation, and optional capabilities or size. For example, `t3.micro` belongs to the T3 burstable general-purpose family and uses the `micro` size.

Instance families and their availability change over time and vary by Region. Check the current AWS instance type list before choosing a type.

### Burstable instances

T-family instances are designed for workloads that usually need low-to-moderate CPU with occasional bursts. They use CPU credits under the applicable model. Sustained high CPU can behave differently depending on the instance's credit mode and configuration.

A small burstable instance can be suitable for a short learning lab, but it may be underpowered for a production Jenkins controller with multiple concurrent builds.

### How to choose an instance

Consider:

1. **CPU:** Number and performance of vCPUs; sustained vs. bursty usage.
2. **Memory:** Jenkins, Java, builds, and plugins can use substantial RAM.
3. **Storage:** Root volume size, throughput, persistence, and backup requirements.
4. **Network:** Expected traffic and required bandwidth.
5. **Architecture:** x86-64 vs. Arm; ensure OS packages and application dependencies support it.
6. **Cost:** On-Demand, Spot, Savings Plans, Reserved Instances, and other applicable options have different trade-offs.
7. **Region availability:** Not every instance family is offered in every AZ.

> **Important:** Do not assume `t2.micro` is always available or free. Instance availability, eligibility, quotas, and Free Tier offers depend on current AWS terms, account status, Region, and selected configuration. Check the pricing and account console before launching.

---

## 5. Regions and Availability Zones

### AWS Region

A **Region** is a separate geographic area where AWS operates infrastructure. Region selection can affect latency, data residency, service availability, resilience design, and cost.

Examples include Mumbai (`ap-south-1`) and Hyderabad (`ap-south-2`). Confirm the current Region names and service availability in AWS documentation.

### Availability Zone (AZ)

An **Availability Zone** is an isolated location within a Region, consisting of one or more data centers with independent infrastructure. Multiple AZs help design applications that tolerate failure in one location.

An EC2 instance is launched in a specific AZ. The instance and its attached resources have Region/AZ constraints; for example, an EBS volume is normally tied to one AZ.

### Region vs. AZ

| Region | Availability Zone |
|---|---|
| Geographic area | Isolated location within a Region |
| Contains multiple AZs | Belongs to one Region |
| Useful for geographic placement and disaster recovery | Useful for fault isolation and high availability |
| Region selection affects service availability and data location | AZ placement affects instance and volume placement |

### Single-AZ vs. multi-AZ design

A single EC2 instance is a single point of failure for the application running on it. For production availability, a common design uses instances across multiple AZs behind a load balancer, with appropriate health checks, scaling, data replication, and deployment practices.

Adding a second AZ alone does not make an application highly available: the application, data layer, network, and operations must also be designed for failure.

---

## 6. Important EC2 components

### 6.1 Amazon Machine Image (AMI)

An **AMI** is a template used to launch instances. It includes information needed to launch an instance, such as the OS image and block-device mappings.

Examples: Ubuntu Server AMI, Amazon Linux AMI, and Windows Server AMI.

Choose an AMI from a trusted publisher and keep the OS patched.

### 6.2 Key pair

An EC2 key pair supports SSH authentication for Linux instances when using the key-based login path. AWS provides or registers the public key; the private key must be protected by the user.

- The `.pem` file is a **private credential**. Do not commit it to GitHub, email it, or share it.
- AWS cannot simply re-download the original private key if you lose it.
- Restrict file permissions on Unix-like systems.
- For supported configurations, consider Session Manager or EC2 Instance Connect to reduce dependence on long-lived SSH key distribution.

### 6.3 EBS volume

Amazon Elastic Block Store provides block storage for EC2. The root EBS volume typically holds the operating system and application files.

Consider:
- Volume size and type.
- Encryption.
- Snapshots and backup retention.
- Whether the root volume is deleted when the instance is terminated.
- Separate data volumes when persistence and recovery need to be independent from the instance lifecycle.

### 6.4 Security group

A security group is a **stateful virtual firewall** associated with an instance's network interface. Rules specify permitted inbound and outbound traffic.

For this lab, the main ports are:

| Port | Protocol | Purpose | Suggested source |
|---|---|---|---|
| 22 | TCP | SSH administration | Your current public IP `/32`, not the entire internet |
| 8080 | TCP | Jenkins web interface in the basic demo | Your current public IP `/32` for a short lab, or a private network/VPN |
| 443 | TCP | HTTPS, if properly configured | Intended client ranges or public internet for a public production endpoint |

Do not open every port to `0.0.0.0/0`. Publicly exposing Jenkins on port 8080 is not a production security design. See the security section below.

### 6.5 Public and private IPv4 addresses

- A **private IPv4 address** is used for communication within connected private networks.
- A **public IPv4 address** can provide internet reachability when routing and security rules permit.
- A public IP alone does not guarantee connectivity. The subnet route table, internet gateway, security group, network ACL, and host service must all allow the traffic.

### 6.6 IAM instance profile

An EC2 instance profile allows applications on the instance to obtain credentials for an attached IAM role. Prefer a role with narrowly scoped permissions over storing long-lived AWS access keys on the server.

---

## 7. Security groups and network access

A browser request to Jenkins succeeds only if the entire path works:

```text
Browser
  |
  | TCP 8080
  v
Public IP / routing
  |
  v
VPC route + Internet Gateway (if public access is intended)
  |
  v
Security Group inbound rule
  |
  v
EC2 network interface
  |
  v
Ubuntu host firewall (if enabled)
  |
  v
Jenkins listening on port 8080
```

If any required part is missing, the browser may time out or fail to connect.

### Inbound rules for the learning lab

1. Allow TCP 22 only from your current public IP address.
2. Allow TCP 8080 only from your current public IP for a temporary demonstration, if you must access Jenkins directly.
3. Remove the port 8080 rule when the lab is complete.
4. Never expose SSH to all IPv4 addresses unless there is a well-justified, tightly controlled temporary need.

Your public IP can change. If SSH stops working, verify your current public IP and update the source CIDR rather than opening SSH to everyone.

---

## 8. Hands-on lab: launch Ubuntu EC2

### Lab objective

Launch an Ubuntu Linux instance, connect to it securely, install Java and Jenkins, and validate the Jenkins service.

### Step 1 — Open EC2

1. Sign in to the AWS Management Console.
2. Open **EC2**.
3. Select the intended Region in the Region selector.
4. Open **Instances** and choose **Launch instances**.

### Step 2 — Configure the instance

Use these as a learning baseline; review the current console options and estimated costs.

- **Name:** `jenkins-learning-lab`
- **AMI:** A current supported Ubuntu Server LTS AMI from Canonical.
- **Instance type:** A small instance suitable for the account and workload. The video may demonstrate `t2.micro`, but it is not universally available or appropriate for every account or current Free Tier offer.
- **Key pair:** Create or select a key pair and download the private key once.
- **Network:** Select a VPC and subnet with the intended access design.
- **Public IP:** Enable only if direct internet access is required for this lab and the subnet supports it.
- **Security group:** Create a dedicated group with SSH restricted to your IP. Add port 8080 only when needed for the demonstration.
- **Storage:** Select an adequate encrypted EBS root volume. Jenkins package installation and build work need disk space; a very small volume can fill quickly.
- **IAM role:** Leave absent if the lab needs no AWS API access, or attach a least-privilege role if a justified requirement exists.

Review the configuration, then choose **Launch instance**.

### Step 3 — Wait for instance checks

In the Instances view, wait until the instance is running and its status checks pass. Record:

- Instance ID.
- Public IPv4 address or DNS name, if assigned.
- Private IPv4 address.
- Availability Zone.
- Security group name.
- AMI and instance type.

Do not publish sensitive account identifiers or private key material in public notes.

### Step 4 — Verify network prerequisites

Before connecting, confirm:

- Instance state is `running`.
- Status checks have passed.
- The key pair matches the instance launch configuration.
- Security group permits SSH from your current IP.
- If connecting over the public internet, the instance has a public IP and its subnet route table has a route to an Internet Gateway.
- Local or corporate network rules do not block outbound TCP 22.

---

## 9. Connect to EC2 using SSH

The default SSH username depends on the AMI. For the official Ubuntu Server AMI, the usual username is `ubuntu`.

### Linux or macOS

Move the private key to a safe location, then restrict permissions:

```bash
chmod 400 ~/Downloads/jenkins-lab.pem
```

Connect using the public IPv4 address:

```bash
ssh -i ~/Downloads/jenkins-lab.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

Replace `YOUR_EC2_PUBLIC_IP` with the instance's actual public IPv4 address. Do not type the placeholder literally.

### Windows PowerShell

Open PowerShell and run:

```powershell
ssh -i "$HOME\Downloads\jenkins-lab.pem" ubuntu@YOUR_EC2_PUBLIC_IP
```

If OpenSSH rejects the key because of file permissions, restrict access to the private key using Windows file permissions or use a supported SSH client configured with that key. Do not upload the key to a third-party website.

### Expected result

You should reach a shell prompt on the remote Ubuntu server. Verify the system:

```bash
whoami
hostname
cat /etc/os-release
ip address
df -h
free -h
```

### SSH connection checklist

- `Permission denied (publickey)`: verify the username and key pair.
- `Connection timed out`: check public IP, route, security group TCP 22 source, network ACL, and local network restrictions.
- `Connection refused`: the host may be reachable but SSH may not be listening or may be blocked locally.
- `Host key verification failed`: verify that the instance endpoint is correct before carefully updating a stale known-host entry.

For a supported alternative, consider AWS Systems Manager Session Manager. It requires the right IAM permissions, instance configuration/agent, and network connectivity to Systems Manager endpoints.

---

## 10. Install Java and Jenkins

> **Version note:** Jenkins runtime requirements change. The Jenkins documentation currently lists Java 21 and Java 25 as supported runtime versions for current releases. The steps below use OpenJDK 21 on Ubuntu. Check Jenkins' official Java support policy and installation instructions before repeating this lab later.

### Step 1 — Update Ubuntu packages

```bash
sudo apt update
sudo apt upgrade -y
```

For a disposable lab, a package upgrade may require a reboot if core packages or the kernel are updated. Schedule reboots appropriately.

### Step 2 — Install Java 21

```bash
sudo apt install -y fontconfig openjdk-21-jre
java -version
```

Expected output should report an OpenJDK 21 runtime. Exact vendor and build strings vary.

### Step 3 — Add the official Jenkins repository

Follow the current Jenkins Linux installation page if its repository or signing-key instructions change. The following is the documented Debian/Ubuntu repository pattern for current Jenkins LTS packages:

```bash
sudo install -m 0755 -d /etc/apt/keyrings
sudo wget -O /etc/apt/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key

echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" \
  | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
```

Refresh the package index and install Jenkins:

```bash
sudo apt update
sudo apt install -y jenkins
```

### Step 4 — Start and enable Jenkins

```bash
sudo systemctl enable --now jenkins
```

Check its service state:

```bash
sudo systemctl status jenkins --no-pager
```

Check the listening port:

```bash
sudo ss -lntp | grep ':8080'
```

Check recent logs if startup fails:

```bash
sudo journalctl -u jenkins -n 100 --no-pager
```

### Step 5 — Retrieve the initial setup password

For a standard package installation:

```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

Treat this password as a secret. Do not commit it to GitHub or paste it into public chat, screenshots, or issue trackers.

### Step 6 — Complete Jenkins setup

1. From a browser on an allowed client, open `http://YOUR_EC2_PUBLIC_IP:8080` for this temporary HTTP-only lab.
2. Enter the initial administrator password.
3. Install the suggested plugins or select the plugin set required for your lab.
4. Create an administrator account.
5. Complete the setup wizard.

**This HTTP URL is for a temporary learning lab only.** Do not use it to send credentials over an untrusted network. For real use, configure HTTPS through a suitable reverse proxy or load balancer, restrict network access, and apply Jenkins security guidance.

---

## 11. Open Jenkins safely

The video demonstration opens port 8080 in the EC2 security group so the Jenkins UI can be reached externally. For a short lab, limit the inbound source to your current public IP (`x.x.x.x/32`).

### Console workflow

1. Open EC2 → **Instances**.
2. Select the Jenkins instance.
3. Open the **Security** tab.
4. Select its security group.
5. Choose **Edit inbound rules**.
6. Add:
   - Type: Custom TCP
   - Port: `8080`
   - Source: My IP (or your carefully defined CIDR)
7. Save the rule.
8. Test the Jenkins URL from the allowed client.

Remove this rule when you no longer need browser access.

### Production pattern

A safer production architecture usually avoids exposing the Jenkins controller directly to the entire internet. Consider:

- Private subnet placement and access through VPN, a bastion design, or Systems Manager.
- HTTPS termination through a correctly configured reverse proxy or load balancer.
- Security groups that permit traffic only from the proxy or trusted administration network.
- Strong authentication, controlled plugin installation, patching, backups, and restricted administrative access.
- Separate build agents and carefully scoped credentials for jobs.
- Network egress controls and secret-management practices.

Do not treat a security group as a substitute for Jenkins authentication or application-level hardening.

---

## 12. Validate the deployment

Run these commands on the EC2 instance:

```bash
# Confirm OS
cat /etc/os-release

# Confirm Java runtime
java -version

# Confirm service state
sudo systemctl is-active jenkins

# Confirm Jenkins is listening
sudo ss -lntp | grep ':8080'

# Inspect recent logs
sudo journalctl -u jenkins -n 50 --no-pager

# Check available filesystem space
df -h
```

From your local workstation, verify that the target host is reachable. On systems with `curl`:

```bash
curl -I http://YOUR_EC2_PUBLIC_IP:8080
```

An HTTP response indicates that a web service answered, but the Jenkins setup wizard may redirect or return a different status depending on setup state.

### Success criteria

- EC2 instance is running and status checks pass.
- SSH connection works from the permitted source.
- Java runtime is installed and supported by the installed Jenkins release.
- Jenkins service is active.
- Jenkins listens on port 8080.
- The browser can reach Jenkins from the allowed client.
- The initial setup wizard completes successfully.
- You have a cleanup plan for the resources.

---

## 13. Troubleshooting guide

| Symptom | Likely cause | What to check |
|---|---|---|
| SSH times out | Route or firewall path is blocked | Public IP, route table, Internet Gateway, SG TCP 22, network ACL, client network |
| SSH says `Permission denied (publickey)` | Wrong key or username | AMI username, selected key pair, local private-key file |
| Browser times out on 8080 | Network path blocked | Public IP, route, SG TCP 8080 source, NACL, local firewall |
| Browser says connection refused | Service not listening | `systemctl status jenkins`, `ss -lntp`, Jenkins logs |
| Jenkins fails to start | Java incompatibility, memory pressure, config/package issue | `java -version`, `journalctl -u jenkins`, `free -h`, disk space |
| `apt update` fails | DNS, routing, repository, or outbound access issue | Default route, DNS resolution, outbound rules, repository status |
| Disk space is exhausted | Logs, packages, workspaces, or builds grew | `df -h`, `sudo du -xhd1 /var/lib/jenkins` |
| Public IP changed after stop/start | Dynamic public IPv4 changed | Re-check instance details and update the endpoint; consider alternatives if a stable IP is required |
| Jenkins loads but setup fails | Application startup or browser/session issue | Jenkins logs, browser dev tools, Java compatibility, disk and memory |

### Useful diagnostics

```bash
# Network addresses and routes
ip address
ip route

# DNS resolution
getent hosts pkg.jenkins.io

# Check service status and logs
sudo systemctl status jenkins --no-pager
sudo journalctl -u jenkins -n 100 --no-pager

# Check ports and resources
sudo ss -lntp
free -h
df -h
```

Avoid disabling firewalls or opening every port as a first troubleshooting step. Change one control at a time and keep access restricted.

---

## 14. Security and production considerations

The demo is a learning exercise, not a complete production architecture.

### Identity and access

- Protect the AWS root user with MFA; do not use it for routine administration.
- Use IAM Identity Center or appropriate federated access for workforce users where available.
- Apply least privilege to AWS permissions.
- Attach an IAM role to EC2 only when the workload needs AWS API access.
- Never store long-lived AWS access keys in source code, user data, AMIs, or Jenkins jobs.

### Network security

- Restrict SSH to known administration IPs or use Session Manager when suitable.
- Avoid direct public exposure of Jenkins when possible.
- Use HTTPS for authenticated web interfaces.
- Review both security groups and network ACLs.
- Minimize inbound and outbound access to what the workload requires.

### Operating system and Jenkins

- Apply security updates and reboot when necessary.
- Use supported Java and Jenkins releases.
- Install only required plugins from trusted sources.
- Back up Jenkins home and test restoration.
- Restrict who can configure jobs and credentials.
- Avoid running untrusted builds on a privileged controller.
- Monitor disk, memory, CPU, service health, and logs.

### Availability and recovery

A single EC2 instance can fail. Production design may require multiple AZs, automated replacement, backups, a documented recovery procedure, and a suitable strategy for Jenkins controller state. High availability requires deliberate design; simply enabling instance recovery or creating a snapshot does not guarantee seamless service continuity.

---

## 15. Cost awareness and cleanup

EC2 can incur charges even when the application is not being used. Potential cost items include:

- Instance runtime.
- EBS volumes and snapshots.
- Public IPv4 address usage under current AWS pricing.
- Data transfer.
- Elastic IPs, load balancers, NAT Gateways, and other supporting resources.

Free Tier eligibility and promotional credits depend on current account terms and resource configuration. Always check the AWS billing console and pricing pages rather than assuming a particular instance or resource is free.

### Lab cleanup checklist

When finished:

1. Save any notes or configuration you need.
2. Stop Jenkins if you only need to pause the lab, remembering that EBS and some other charges may continue.
3. Terminate the EC2 instance if you no longer need it.
4. Check whether the root EBS volume is configured for deletion on termination.
5. Delete unattached EBS volumes and snapshots you no longer need.
6. Release any allocated Elastic IP that is not needed.
7. Remove temporary security-group rules and other resources created for the lab.
8. Review billing and cost-explorer data after usage is recorded.

> Termination is destructive. Confirm that you have saved required files and that no persistent data needs to be retained before terminating.

---

## 16. EC2 CLI quick reference

These commands require AWS CLI to be installed and configured with appropriate permissions. They operate in the Region configured in the CLI unless a Region is supplied.

```bash
# Check which identity the CLI is using
aws sts get-caller-identity

# List EC2 instances in the configured Region
aws ec2 describe-instances \
  --query 'Reservations[].Instances[].[InstanceId,State.Name,InstanceType,PublicIpAddress,Placement.AvailabilityZone]' \
  --output table

# Describe one instance
aws ec2 describe-instances \
  --instance-ids i-REPLACE_WITH_INSTANCE_ID

# Start an existing stopped instance
aws ec2 start-instances \
  --instance-ids i-REPLACE_WITH_INSTANCE_ID

# Stop an instance
aws ec2 stop-instances \
  --instance-ids i-REPLACE_WITH_INSTANCE_ID

# Terminate an instance (destructive)
aws ec2 terminate-instances \
  --instance-ids i-REPLACE_WITH_INSTANCE_ID
```

Replace all example IDs with actual values. Confirm the active AWS account and Region before making changes. Do not run the termination command unless you intend to delete that instance.

---

## 17. Assignment

### Task A — EC2 launch

1. Launch an Ubuntu EC2 instance.
2. Record its AMI, instance type, Region, AZ, subnet, and security group.
3. Explain why you chose the instance type and storage size.
4. Connect using SSH and record the successful validation commands.

### Task B — Jenkins installation

1. Install a supported Java runtime.
2. Install Jenkins from the official repository.
3. Enable and start the service.
4. Verify Jenkins status and port 8080.
5. Complete the initial setup wizard.

### Task C — Security

1. Restrict SSH to your IP.
2. Restrict port 8080 to your IP for the temporary demo.
3. Explain why `0.0.0.0/0` is risky for SSH and an administrative web UI.
4. Describe how Session Manager or a private network could reduce public exposure.
5. Remove temporary access rules when finished.

### Task D — Troubleshooting

Explain how you would diagnose each situation:

- SSH connection timeout.
- SSH public-key authentication failure.
- Jenkins service inactive.
- Jenkins port open locally but inaccessible from the browser.
- Low disk space after builds.

### Task E — Cost and cleanup

List every resource created and document how you verified that unnecessary resources were removed.

### Evidence to include in your GitHub submission

- Screenshot of EC2 instance details (redact account IDs or other sensitive details).
- Terminal output for `java -version` and `systemctl is-active jenkins`.
- Screenshot of Jenkins setup page without exposing passwords or credentials.
- Security-group inbound rules showing restricted source ranges.
- Cleanup checklist.

Never commit private keys, initial Jenkins passwords, AWS credentials, or other secrets to the repository.

---

## 18. Interview questions

### Fundamentals

**1. What is Amazon EC2?**  
A service providing resizable compute capacity in AWS. Users select an AMI, instance type, storage, network, and security settings to launch virtual servers.

**2. What is an AMI?**  
A launch template containing the image and configuration information used to create instances.

**3. What is an instance type?**  
A specification of compute, memory, storage, and networking capabilities.

**4. What is the difference between a Region and an Availability Zone?**  
A Region is a geographic area; an AZ is an isolated location within that Region.

**5. What is an EC2 key pair?**  
A public/private key mechanism used by supported connection methods to authenticate users to an instance.

### Networking and security

**6. Why does SSH fail even when an instance is running?**  
The instance may lack a valid route or public address, port 22 may be blocked, the client IP may not match the security group rule, the username/key may be wrong, or SSH may not be running.

**7. What is a security group?**  
A stateful virtual firewall associated with a network interface that controls permitted inbound and outbound traffic.

**8. Why should port 22 not normally be open to the entire internet?**  
It exposes the SSH service to connection attempts from any IPv4 source, increasing the attack surface.

**9. Does assigning a public IP automatically make an instance reachable?**  
No. Routing, Internet Gateway connectivity, security groups, network ACLs, host firewalls, and the application service must also allow the traffic.

**10. What is an IAM instance role?**  
A role whose temporary credentials can be made available to applications on an EC2 instance so they can call authorized AWS APIs without storing long-lived access keys.

### Operations and DevOps

**11. What is the difference between stopping and terminating an instance?**  
Stopping shuts down a supported instance while generally retaining attached EBS volumes; terminating deletes the instance and may delete volumes configured for deletion on termination. Other resources may persist and require separate cleanup.

**12. How would you make a web application highly available?**  
Use instances across multiple AZs, a load balancer, health checks, scaling, resilient data services, monitoring, and tested recovery procedures.

**13. Why might Jenkins fail to start after a Java update?**  
The installed Jenkins version may not support the selected Java runtime, or the service may encounter configuration, memory, disk, or permission problems. Check the official support matrix and service logs.

**14. Why might Jenkins be reachable through SSH but not through a browser?**  
SSH and HTTP use different ports and rules. Check TCP 8080, public routing, the host firewall, and whether Jenkins is listening on the expected interface and port.

**15. How would you reduce the cost of a learning environment?**  
Use appropriately sized resources, start them only when needed, terminate disposable instances, remove unused storage and addresses, and monitor billing.

---

## 19. Further reading

Use official documentation as the source of truth when console steps, instance types, package instructions, or prices change.

- [Amazon EC2 User Guide](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html)
- [EC2 instance types by Region](https://docs.aws.amazon.com/ec2/latest/instancetypes/ec2-instance-regions.html)
- [Connect to your EC2 instance](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/connect.html)
- [EC2 security groups](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-security-groups.html)
- [AWS global infrastructure](https://aws.amazon.com/about-aws/global-infrastructure/)
- [AWS EC2 pricing](https://aws.amazon.com/ec2/pricing/)
- [Jenkins Java support policy](https://www.jenkins.io/doc/book/platform-information/support-policy-java/)
- [Jenkins installation on Linux](https://www.jenkins.io/doc/book/installing/linux/)
- [AWS DevOps Zero to Hero repository](https://github.com/iam-veeramalla/aws-devops-zero-to-hero)

---

## Lesson summary

Amazon EC2 provides virtual compute capacity in AWS. To deploy an application successfully, you need more than a running instance: you must select an appropriate AMI and instance type, configure storage and networking, secure access with key pairs and security groups, install compatible software, validate the service, monitor the system, and clean up resources when finished.

This lab demonstrates a basic Jenkins deployment on Ubuntu. Treat direct public access on port 8080 as temporary learning-only access, and use stronger network isolation and HTTPS for real environments.
