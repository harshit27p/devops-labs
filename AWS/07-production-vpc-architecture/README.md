# AWS Zero to Hero — Production-Style VPC Architecture

> **Video:** [AWS Zero to Hero — Production-grade VPC project](https://www.youtube.com/watch?v=FZPTL_kNvXc&list=PLdpzxOOAlwvIc1TjTwopNSjRJkzES2ZXk&index=61&t=5s)  
> **Suggested repository path:** `07-production-vpc-architecture/README.md`  
> **Focus:** Public/private subnets, two Availability Zones, bastion access, NAT Gateway, Application Load Balancer (ALB), Launch Templates, EC2 Auto Scaling, and a Python web application.

These notes turn the supplied video outline into a repeatable learning lab. Console labels can change, so verify settings against the AWS documentation linked at the end.

## 1. Project overview

Build a small web application reachable through a public Application Load Balancer while its EC2 application instances stay in private subnets without public IPv4 addresses.

### Learning objectives

- Design a VPC spanning two Availability Zones.
- Separate internet-facing resources from private application compute.
- Explain route tables, Internet Gateway (IGW), and NAT Gateway.
- Use a bastion host as a controlled SSH jump point.
- Create a Launch Template with user data and an instance profile.
- Attach an Auto Scaling Group (ASG) to an ALB target group.
- Configure health checks and diagnose unhealthy targets.
- Validate connectivity without assigning public IP addresses to application instances.
- Estimate costs and remove resources safely after testing.

### Architecture

```text
                            Internet users
                                  |
                            HTTP / HTTPS
                                  |
                     +------------------------+
                     | Internet Gateway (IGW) |
                     +------------------------+
                                  |
             +--------------------+--------------------+
             |                                         |
      Public subnet AZ-a                        Public subnet AZ-b
      +--------------------+                    +--------------------+
      | ALB node           |                    | ALB node           |
      | Bastion (optional) |                    | NAT Gateway (HA)   |
      | NAT Gateway (HA)   |                    |                    |
      +--------------------+                    +--------------------+
             |                                         |
             +--------------------+--------------------+
                                  |
                    ALB target group / HTTP :8000
                                  |
             +--------------------+--------------------+
             |                                         |
     Private app subnet AZ-a                  Private app subnet AZ-b
     +--------------------+                    +--------------------+
     | EC2 app instance   |                    | EC2 app instance   |
     | Managed by ASG     |                    | Managed by ASG     |
     +--------------------+                    +--------------------+
             |                                         |
             +--------------------+--------------------+
                                  |
                   Outbound updates via NAT Gateway
```

The ALB spans public subnets in at least two AZs. The ASG places application instances in private subnets across the two AZs. For production resilience, use a NAT Gateway in each AZ and route each private subnet to its same-AZ NAT Gateway. A one-NAT lab design is cheaper but creates an AZ dependency and may incur cross-AZ data charges.

> **Important:** “Production-style” does not automatically mean production-ready. Real deployments should also consider HTTPS and certificates, WAF where appropriate, centralized logs, patching, secrets management, monitoring/alarms, deployment automation, backups, and tested recovery procedures.

## 2. Traffic flows to understand

### Inbound application request

1. A user resolves the ALB DNS name.
2. The request reaches the internet-facing ALB through the IGW.
3. The ALB listener forwards it to a healthy target in the target group.
4. The private EC2 instance accepts traffic only from the ALB security group.
5. The application responds through the ALB to the user.

The client does **not** connect directly to the private EC2 instance.

### Administrator SSH access

1. An administrator connects to the bastion host's public address from an explicitly allowed source IP.
2. The administrator uses a secure, approved method to connect from the bastion to the private instance.
3. The private instance's security group permits SSH only from the bastion security group.

Prefer **AWS Systems Manager Session Manager** where possible and remove inbound SSH access entirely. If using a bastion, restrict port 22 to your current public IP `/32`; never open SSH to `0.0.0.0/0`.

### Outbound updates

Private instances send outbound traffic to the NAT Gateway, which is in a public subnet and has a route to the IGW. NAT allows initiated outbound connections and their responses; it does not provide unsolicited inbound internet access to private instances.

## 3. Address plan

Choose a CIDR that does not overlap with your home, office, VPN, or peered networks. The following is an example only.

| Resource | Example CIDR | Route intent |
|---|---|---|
| VPC | `10.20.0.0/16` | VPC-local route |
| Public subnet AZ-a | `10.20.1.0/24` | Default IPv4 route to IGW |
| Public subnet AZ-b | `10.20.2.0/24` | Default IPv4 route to IGW |
| Private app subnet AZ-a | `10.20.11.0/24` | Default IPv4 route to NAT-A |
| Private app subnet AZ-b | `10.20.12.0/24` | Default IPv4 route to NAT-B |

Use one AWS Region and select two different AZs in that Region. AZ names can map differently across accounts, so don't assume a name such as `us-east-1a` identifies the same physical AZ for every account.

A subnet is effectively public when its route table provides a route to an Internet Gateway and its resources have appropriate public addressing and security rules. A private subnet does not route directly to the IGW. It may route outbound IPv4 traffic through a NAT Gateway, or have no general internet route. **A subnet name alone does not make it public or private.**

## 4. Security group design

Create separate security groups so the intended traffic path is explicit.

| Security group | Inbound rules | Outbound intent |
|---|---|---|
| `sg-alb` | TCP 80 from `0.0.0.0/0` for a temporary HTTP lab; TCP 443 for HTTPS when configured | App port to `sg-app` |
| `sg-app` | TCP 8000 **from `sg-alb` only**; TCP 22 from `sg-bastion` only if SSH is used | Required outbound traffic, including NAT-routed updates |
| `sg-bastion` | TCP 22 from **your public IP `/32` only** | SSH to `sg-app`; other egress only as needed |

Security groups are stateful. Responses to allowed connections are automatically permitted. Network ACLs are stateless and can also affect traffic, but avoid changing NACLs unnecessarily during the initial lab.

Security checks:

- Do not assign a public IPv4 address to application instances.
- Do not add a public-subnet route to the private application subnets.
- Do not allow the whole internet to reach port 8000 on application instances.
- Never store SSH private keys in user data, AMIs, source control, or shell history.
- Attach an IAM role to EC2 if the app needs AWS APIs; don't store long-lived access keys on instances.
- For production, prefer Session Manager and restrict or remove inbound SSH.

## 5. Build the VPC and networking

### Step 1 — Create the VPC

1. Open the **VPC** console and select the intended Region.
2. Create a VPC named `zero-to-hero-vpc` with IPv4 CIDR `10.20.0.0/16`.
3. Enable DNS resolution and DNS hostnames if required by the workload.
4. Create four subnets:
   - `public-a` — `10.20.1.0/24`, AZ-a
   - `public-b` — `10.20.2.0/24`, AZ-b
   - `private-app-a` — `10.20.11.0/24`, AZ-a
   - `private-app-b` — `10.20.12.0/24`, AZ-b
5. Add tags such as `Project=aws-zero-to-hero` and `Environment=lab`.

### Step 2 — Create and attach an Internet Gateway

1. Create `zero-to-hero-igw`.
2. Attach it to `zero-to-hero-vpc`.
3. Create a route table named `public-rt`.
4. Add `0.0.0.0/0 → Internet Gateway`.
5. Associate `public-rt` with both public subnets.

The IGW route alone does not give a private EC2 instance internet access. Public IPv4 addressing and security controls also matter.

### Step 3 — Create NAT Gateway(s)

For the recommended resilient design:

1. Allocate an Elastic IP address for each NAT Gateway.
2. Create `nat-a` in `public-a` and `nat-b` in `public-b`.
3. Wait until each NAT Gateway becomes available.
4. Create separate route tables for the private subnets.
5. Add `0.0.0.0/0 → nat-a` to the route table associated with `private-app-a`.
6. Add `0.0.0.0/0 → nat-b` to the route table associated with `private-app-b`.

**Budget warning:** NAT Gateways have hourly and data-processing charges. For a short practice lab, a single NAT Gateway is cheaper, but it is not equally resilient. Delete NAT Gateways and release unused Elastic IPs after the lab.

### Step 4 — Confirm route-table associations

Expected route intent:

- Public subnets: `VPC CIDR → local`, `0.0.0.0/0 → IGW`
- Private app subnet AZ-a: `VPC CIDR → local`, `0.0.0.0/0 → NAT-A`
- Private app subnet AZ-b: `VPC CIDR → local`, `0.0.0.0/0 → NAT-B`

A common mistake is creating the correct route but leaving a subnet associated with the main or wrong route table.

## 6. Create the Application Load Balancer

Create the ALB before attaching it to the Auto Scaling Group.

1. Open **EC2 → Load Balancers → Create load balancer**.
2. Choose **Application Load Balancer**.
3. Name it `zero-to-hero-alb`.
4. Choose **Internet-facing** and IPv4 for this simple lab.
5. Select the VPC and both public subnets, one in each AZ.
6. Attach `sg-alb`.
7. Create a target group:
   - Name: `zero-to-hero-tg`
   - Target type: **Instances**
   - Protocol: HTTP
   - Port: `8000`
   - Health check protocol: HTTP
   - Health check path: `/health`
8. Create a listener on HTTP port 80 that forwards to the target group.
9. Later inspect **Targets / Registered targets** to check health.

For production, configure HTTPS with an AWS Certificate Manager certificate and redirect HTTP to HTTPS. Do not send passwords or sensitive data over plain HTTP. HTTP is used here only to simplify the learning lab.

The target group's health check must use a path that returns a successful status code when the app is ready. A running EC2 instance is not necessarily a healthy application target.

## 7. Create a Launch Template

The Launch Template defines how ASG instances are created. Use a current, supported Linux AMI in your Region. The user-data example below is intended for Amazon Linux 2023.

1. Open **EC2 → Launch Templates → Create launch template**.
2. Name it `zero-to-hero-app-template`.
3. Choose an Amazon Linux 2023 AMI or another supported Linux image.
4. Choose a small instance type suitable for the lab and account quota.
5. Select `sg-app`.
6. Do not assign a public IP to instances in private subnets. Also ensure the ASG subnet setting does not enable public IP assignment.
7. Create/select an instance profile with no permissions unless the workload requires AWS API access. Add only required permissions.
8. Under **Advanced details → User data**, paste the script below.
9. Create the Launch Template.

### User data: install and start a tiny Python app

This deliberately simple app returns a health-check endpoint and the EC2 instance ID so you can observe load distribution. The instance ID is read using IMDSv2.

```bash
#!/bin/bash
set -euxo pipefail

dnf -y update
dnf -y install python3

install -d -m 0755 /opt/zero-to-hero-app

cat > /opt/zero-to-hero-app/app.py <<'PY'
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import urllib.request

def get_instance_id():
    try:
        token_request = urllib.request.Request(
            "http://169.254.169.254/latest/api/token",
            method="PUT",
            headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"},
        )
        with urllib.request.urlopen(token_request, timeout=2) as response:
            token = response.read().decode()
        request = urllib.request.Request(
            "http://169.254.169.254/latest/meta-data/instance-id",
            headers={"X-aws-ec2-metadata-token": token},
        )
        with urllib.request.urlopen(request, timeout=2) as response:
            return response.read().decode()
    except Exception:
        return "unknown"

INSTANCE_ID = get_instance_id()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            body, status = {"status": "ok"}, 200
        elif self.path == "/":
            body = {
                "message": "AWS Zero to Hero private application",
                "instance_id": INSTANCE_ID,
                "hostname": os.uname().nodename,
            }
            status = 200
        else:
            body, status = {"error": "not found"}, 404
        payload = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, fmt, *args):
        print("%s - %s" % (self.address_string(), fmt % args))

HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
PY

cat > /etc/systemd/system/zero-to-hero-app.service <<'UNIT'
[Unit]
Description=Zero to Hero sample Python web application
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=nobody
Group=nobody
WorkingDirectory=/opt/zero-to-hero-app
ExecStart=/usr/bin/python3 /opt/zero-to-hero-app/app.py
Restart=on-failure
RestartSec=3
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=full
ProtectHome=true

[Install]
WantedBy=multi-user.target
UNIT

chmod 0755 /opt/zero-to-hero-app
chmod 0644 /opt/zero-to-hero-app/app.py
systemctl daemon-reload
systemctl enable --now zero-to-hero-app
```

**User-data notes:**

- User data normally runs during initial launch, typically as root. Check cloud-init logs if it fails.
- `dnf update` can lengthen boot time; for production, prefer a tested AMI/image pipeline over blindly updating packages at every launch.
- This tiny HTTP server is for learning only, not production hosting. A real app needs a maintained application server and deployment/monitoring process.
- Require IMDSv2 in the Launch Template; do not weaken metadata protections to make the example work.
- If the instance has no outbound access, package installation may fail. Check NAT routing, DNS, NACLs, and security-group egress.

## 8. Create the Auto Scaling Group

1. Open **EC2 → Auto Scaling Groups → Create Auto Scaling group**.
2. Name it `zero-to-hero-app-asg`.
3. Select `zero-to-hero-app-template` and a specific template version.
4. Choose the VPC and both **private application subnets**.
5. Attach the existing target group `zero-to-hero-tg`.
6. Enable Elastic Load Balancing health checks if available.
7. For the learning lab, set minimum `2`, desired `2`, maximum `4`.
8. Add tags such as `Project=aws-zero-to-hero`.
9. Create the group and wait for instances to launch.
10. Open the target group and wait for targets to become **healthy**.

Do not place app instances in public subnets simply to make SSH or package installation easier. Use a bastion/Session Manager for administration and NAT or VPC endpoints for required outbound services.

### Optional target-tracking scaling policy

1. Open the ASG and select **Automatic scaling**.
2. Add a target-tracking policy based on average CPU utilization, for example a target around 50%.
3. Choose a suitable warm-up period.
4. Generate modest test traffic and observe scaling activities.
5. Return desired capacity to 2 before cleanup.

CPU is only an example. Production scaling should use metrics correlated with demand, such as request count per target, latency, queue depth, or application-specific signals.

## 9. Create the bastion host (optional)

A bastion is included to teach the jump-host pattern, but Session Manager is often preferable.

1. Launch a small supported Linux EC2 instance in `public-a`.
2. Assign a public IPv4 address or Elastic IP only if necessary.
3. Attach `sg-bastion`, allowing TCP 22 only from your current public IP `/32`.
4. Use a dedicated key pair and protect the private key.
5. Keep app instances in private subnets with no public IP.
6. Configure `sg-app` to allow TCP 22 only from `sg-bastion` if SSH is required.
7. Connect to the bastion, then connect to the private instance's private IP using an approved secure key-delivery/access method.

Example from an administrator workstation:

```bash
chmod 400 bastion-key.pem
ssh -i bastion-key.pem ec2-user@BASTION_PUBLIC_IP
```

Do not casually copy private keys onto shared bastion hosts. For stronger controls, use SSH ProxyJump or Systems Manager Session Manager and document the chosen access pattern.

### Preferred alternative: Systems Manager Session Manager

With the correct instance profile, SSM Agent, network connectivity, and IAM permissions, Session Manager can provide shell access without inbound SSH rules or a public IP. Private instances need access to Systems Manager endpoints, typically through NAT or appropriate VPC interface endpoints. Verify the exact endpoint and IAM requirements for your Region.

## 10. Test the application

### Test 1 — ALB DNS name

1. Open **EC2 → Load Balancers** and copy the ALB DNS name.
2. Visit `http://ALB-DNS-NAME/` in a browser, or run:

```bash
curl -i http://ALB-DNS-NAME/
curl -i http://ALB-DNS-NAME/health
```

Replace `ALB-DNS-NAME` with the actual DNS name. Expected: `/` returns JSON with a message and instance ID; `/health` returns HTTP `200` and `{"status": "ok"}`; an unknown path returns HTTP `404`.

### Test 2 — Observe load distribution

```bash
for i in $(seq 1 10); do
  curl -s http://ALB-DNS-NAME/ | python3 -m json.tool
done
```

You may see different instance IDs. Do not expect every request to alternate perfectly: connection reuse, target health, and load distribution behavior affect the result.

### Test 3 — Confirm private placement

In the EC2 console, verify each app instance:

- Is in `private-app-a` or `private-app-b`.
- Has no public IPv4 address.
- Has a private IPv4 address.
- Is registered and healthy in the target group.
- Uses the expected security group.

Trying to reach a private instance's private IP from your workstation should not work unless you have a private network path such as VPN, Direct Connect, or an authorized jump host. That is expected; the ALB is the public entry point.

## 11. Troubleshooting guide

| Symptom | Likely causes | Checks / fixes |
|---|---|---|
| ALB returns `503` | No healthy or registered targets | Check target health, listener forward action, ASG attachment, app process |
| Targets are `unhealthy` | Wrong health path/port, SG block, app failed to start | Confirm port `8000`, `/health`, `sg-app` inbound from `sg-alb`, cloud-init and systemd logs |
| ALB DNS does not open | Wrong listener, ALB SG, subnet/IGW route, DNS typo | Check listener port 80, ALB SG inbound, both public subnet associations and public route table |
| App instance has no internet for package install | Wrong private route, NAT unavailable, missing egress, DNS issue | Check route to NAT, NAT's public-subnet route to IGW, NAT state, DNS and outbound rules |
| SSH to bastion times out | Source IP changed, SG/NACL/route issue, wrong address | Update `/32` to current public IP; check public address and IGW route |
| SSH from bastion to app fails | App SG blocks SSH, wrong private IP/key/user | Check SG reference, local route, OS username and key access |
| Instances launch in public subnets | ASG subnet selection is wrong | Edit ASG to use only private app subnets |
| User data failed | Package repo unreachable, shell error, cloud-init incomplete | Check `/var/log/cloud-init-output.log`, `cloud-init status --long`, `journalctl -u zero-to-hero-app` |
| One AZ has no healthy targets | Subnet/route/capacity/AZ issue | Check subnet selection, free IPs, capacity, route and target health |
| Scale-out does not happen | No scaling policy, metric below threshold, cooldown/warmup | Check ASG activities, policy, CloudWatch metrics, min/max limits |

Useful commands on an app instance:

```bash
sudo cloud-init status --long
sudo tail -n 200 /var/log/cloud-init-output.log
sudo systemctl status zero-to-hero-app --no-pager
sudo journalctl -u zero-to-hero-app -n 100 --no-pager
sudo ss -lntp | grep ':8000'
curl -i http://127.0.0.1:8000/health
```

Troubleshoot in this order: (1) process running; (2) listening on expected address/port; (3) local health endpoint works; (4) app SG allows ALB SG; (5) target group port/path/protocol match; (6) NACLs/routes permit traffic; (7) targets are registered and in the expected AZs.

## 12. AWS CLI verification commands

Install AWS CLI v2 and configure an approved profile. Use IAM Identity Center or another approved credential method; avoid root credentials and never commit credentials to Git.

```bash
export AWS_REGION="ap-south-1"
export AWS_PROFILE="your-lab-profile"
aws sts get-caller-identity
```

Change the Region/profile to match your setup.

### Inspect VPC and subnets

```bash
aws ec2 describe-vpcs \
  --filters "Name=tag:Name,Values=zero-to-hero-vpc" \
  --query 'Vpcs[].{VpcId:VpcId,Cidr:CidrBlock,State:State}'

aws ec2 describe-subnets \
  --filters "Name=vpc-id,Values=VPC_ID" \
  --query 'Subnets[].{SubnetId:SubnetId,Cidr:CidrBlock,AZ:AvailabilityZone,PublicIp:MapPublicIpOnLaunch}'
```

### Inspect route tables

```bash
aws ec2 describe-route-tables \
  --filters "Name=vpc-id,Values=VPC_ID" \
  --query 'RouteTables[].{RouteTableId:RouteTableId,Routes:Routes,Associations:Associations}'
```

### Inspect ALB and target health

```bash
aws elbv2 describe-load-balancers --names zero-to-hero-alb
aws elbv2 describe-target-groups --names zero-to-hero-tg
aws elbv2 describe-target-health --target-group-arn TARGET_GROUP_ARN
```

### Inspect Auto Scaling

```bash
aws autoscaling describe-auto-scaling-groups \
  --auto-scaling-group-names zero-to-hero-app-asg

aws autoscaling describe-scaling-activities \
  --auto-scaling-group-name zero-to-hero-app-asg \
  --max-items 20
```

Replace placeholders such as `VPC_ID` and `TARGET_GROUP_ARN` with actual values. These commands inspect resources; they do not create the architecture.

## 13. Cost and cleanup checklist

This lab can incur charges. NAT Gateways, ALBs, EC2 instances, public IPv4 addresses, Elastic IPs, and data transfer may be billable. Check current pricing for your Region before starting.

After capturing screenshots and test results, remove resources in dependency order:

1. Delete the Auto Scaling Group or set desired/min/max to zero and wait for instances to terminate.
2. Delete the ALB and its listeners if required by the console workflow.
3. Delete the target group after it is no longer in use.
4. Terminate the bastion host.
5. Delete NAT Gateways and wait until deletion completes.
6. Release Elastic IPs no longer associated with resources.
7. Delete custom route tables after disassociating subnets (the main route table cannot be deleted).
8. Detach and delete the Internet Gateway.
9. Delete the subnets.
10. Delete the VPC.
11. Remove unused launch templates, lab-only IAM roles/profiles, security groups, and key pairs if no longer needed.
12. Review Billing and Cost Management for lingering resources.

Do not delete shared IAM roles, key pairs, or network resources used by other workloads. Use resource tags to identify lab resources before deleting them.

## 14. Production improvements

- **HTTPS:** Use ACM certificates on the ALB and redirect HTTP to HTTPS.
- **No SSH ingress:** Use Systems Manager Session Manager with least-privilege IAM.
- **Repeatable deployment:** Use a golden AMI, EC2 Image Builder, or deployment pipeline rather than installing mutable dependencies at boot.
- **Infrastructure as Code:** Rebuild the VPC, ALB, target group, ASG, IAM, and security groups with Terraform, AWS CDK, or CloudFormation.
- **Observability:** Enable ALB access logs, CloudWatch metrics/alarms, application logs, and sensible retention.
- **Resilience:** Use at least two AZs, an appropriate ASG health-check strategy, and a NAT Gateway per AZ when requirements justify the cost.
- **Secrets:** Use Secrets Manager or Systems Manager Parameter Store; never place secrets in user data or AMIs.
- **Outbound access:** Consider VPC endpoints for supported AWS services.
- **Security posture:** Use least-privilege IAM, IMDSv2, patching, vulnerability management, and appropriate AWS security services.
- **Capacity:** Ensure ALB subnets have enough free IP addresses and ASG subnets can support scale-out.
- **Data durability:** Keep persistent data outside replaceable app instances, such as in a suitable managed database or object store.
- **Recovery:** Define RTO/RPO and test AZ failure and application recovery scenarios.

## 15. Lab deliverables

Capture evidence for your notes or portfolio (hide account IDs, public IPs, and other sensitive details):

- [ ] VPC and four-subnet overview.
- [ ] Public and private route-table entries.
- [ ] Security-group rules showing ALB-to-app and bastion-to-app restrictions.
- [ ] ALB listener and target group configuration.
- [ ] Two healthy targets in separate AZs.
- [ ] ASG settings and private-subnet instance placement.
- [ ] Browser/curl output from the ALB DNS name.
- [ ] Repeated requests showing instance IDs.
- [ ] Cleanup confirmation / billing review.

Suggested GitHub project description:

> Designed a multi-AZ AWS web application architecture using a VPC with public and private subnets, an internet-facing Application Load Balancer, private EC2 instances managed by an Auto Scaling Group, NAT Gateway egress, and restricted administrative access. Validated target health, routing, and security-group boundaries.

Only claim components you actually implemented and tested.

## 16. Practice assignments

### Beginner

1. Draw the architecture and label each subnet, route table, gateway, security group, and traffic direction.
2. Explain why an ALB belongs in public subnets while application instances can remain private.
3. Demonstrate that the app responds through the ALB but is not directly internet-accessible.
4. Explain the difference between an IGW and a NAT Gateway.

### Intermediate

1. Add HTTPS to the ALB using a certificate in AWS Certificate Manager.
2. Configure a target-tracking scaling policy and document how the ASG reacts.
3. Break the target group's health-check path intentionally, record the symptom, then fix it.
4. Replace bastion SSH with Session Manager.
5. Compare one NAT Gateway versus one per AZ, including availability and cost trade-offs.

### Advanced

1. Implement the stack with Terraform or CloudFormation.
2. Add CloudWatch alarms for unhealthy hosts, ALB 5xx errors, and ASG capacity.
3. Store application logs centrally and enable ALB access logging.
4. Build a repeatable AMI/image pipeline and use ASG instance refresh for updates.
5. Design a private-only architecture using VPC endpoints for required AWS services and no general internet egress.
6. Write a failure runbook for an AZ outage, unhealthy targets, and failed user data.

## 17. Interview questions and concise answers

**1. Why use public and private subnets?**  
To expose only the required ingress layer while keeping application compute off direct public internet paths.

**2. What makes a subnet public?**  
Its route table has a route to an Internet Gateway. A resource also needs appropriate addressing and security rules to communicate with the internet.

**3. Does a NAT Gateway allow inbound connections to private instances?**  
No. It supports outbound connections initiated from private resources and their return traffic; it is not a public inbound entry point.

**4. Why deploy across two Availability Zones?**  
To reduce dependence on a single AZ and maintain service during an AZ disruption, assuming the application and its dependencies are also resilient.

**5. What does an ALB target group do?**  
It defines targets and protocol/port/health-check behavior for listener rules.

**6. Why can an ALB return 503?**  
Often there are no healthy registered targets or no usable targets for the request. Check target health, listener rules, app port/path, and security groups.

**7. Difference between an ASG and a Launch Template?**  
The Launch Template describes how to launch an instance. The ASG maintains and scales a fleet using that configuration.

**8. Why attach the target group to the ASG?**  
Instances launched by the group can be registered automatically, and terminating instances can be deregistered during their lifecycle.

**9. What is a bastion host?**  
A controlled administrative jump point into private networks. It must be tightly restricted and patched; Session Manager can often reduce the need for one.

**10. Why allow the app port only from the ALB security group?**  
It prevents clients from bypassing the intended public entry point and limits app ingress to the load balancer.

**11. Difference between EC2 status checks and ALB health checks?**  
EC2 status checks assess instance/system health. ALB health checks test whether the target responds as expected on a configured protocol, port, and path.

**12. Is this fully production-ready?**  
No. It is a learning foundation. Production readiness also requires TLS, operational monitoring, secure deployment/patching, secrets management, capacity planning, data durability, and recovery testing.

**13. Why can user data fail on a later launch?**  
Package repositories, dependency versions, network access, script errors, or boot timing may change. Production workflows should use tested images and deployment automation.

**14. How would you reduce NAT Gateway costs?**  
Review data transfer and traffic patterns, use VPC endpoints for supported AWS services, avoid unnecessary cross-AZ routing, and right-size the architecture without sacrificing required resilience.

**15. Where should persistent application data live?**  
Outside replaceable Auto Scaling instances—often in a managed database or object storage selected for access patterns, durability, and recovery requirements.

## 18. Official references

- [AWS VPC example: servers in private subnets with NAT](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-example-private-subnets-nat.html)
- [Create an Auto Scaling Group using a Launch Template](https://docs.aws.amazon.com/autoscaling/ec2/userguide/create-asg-launch-template.html)
- [Tutorial: Set up a scaled and load-balanced application](https://docs.aws.amazon.com/autoscaling/ec2/userguide/tutorial-ec2-auto-scaling-load-balancer.html)
- [Attach a load balancer to an Auto Scaling Group](https://docs.aws.amazon.com/autoscaling/ec2/userguide/attach-load-balancer-asg.html)
- [Auto Scaling networking and subnet considerations](https://docs.aws.amazon.com/autoscaling/ec2/userguide/asg-in-vpc.html)
- [AWS Networking Best Practices — Subnets](https://aws.github.io/aws-networking-best-practices/foundation/subnets/)
- [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)
- [AWS Systems Manager Session Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html)
- [EC2 user data and cloud-init](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html)

## Key takeaway

Make the **ALB the public application entry point**, keep application EC2 instances in **private subnets**, use **security-group references** to constrain traffic, and use **Auto Scaling across multiple AZs** for elasticity and resilience. NAT Gateway provides controlled outbound connectivity; it is not a substitute for inbound security. Verify the architecture with health checks and real requests, then clean up all billable resources.
