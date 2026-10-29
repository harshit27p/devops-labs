# AWS Zero to Hero — AWS CLI Fundamentals and Automation

> **Video:** [AWS Zero to Hero — AWS Command Line Interface (CLI)](https://www.youtube.com/watch?v=TiDSwf8gydk&list=PLdpzxOOAlwvIc1TjTwopNSjRJkzES2ZXk&index=64)  
> **Suggested repository path:** `09-aws-cli/README.md`  
> **Focus:** AWS CLI v2 installation, authentication, profiles, common commands, EC2 launch anatomy, scripting, troubleshooting, security, and the CLI vs. Infrastructure as Code.

These notes expand the supplied video outline into a practical reference for DevOps learners. Use the official AWS installation guide for your operating system; installation steps and console labels can change.

## 1. What is the AWS CLI?

The AWS Command Line Interface (AWS CLI) is a tool for managing AWS services from a terminal. It sends requests to AWS service APIs using the credentials and configuration available to it.

Typical DevOps uses include:

- Listing and inspecting cloud resources.
- Uploading and downloading files from S3.
- Starting, stopping, and describing EC2 instances.
- Inspecting VPCs, subnets, security groups, and load balancers.
- Running repeatable operational commands.
- Embedding cloud operations in CI/CD workflows and scripts.
- Querying resources and transforming responses with JSON, text, or table output.

### Console vs CLI vs SDK vs IaC

| Tool | Best fit | Important limitation |
|---|---|---|
| AWS Management Console | Learning, visual inspection, occasional manual operations | Manual workflows are difficult to repeat reliably |
| AWS CLI | Ad-hoc operations, scripting, diagnostics, automation glue | Imperative commands alone do not maintain a desired-state model |
| AWS SDK | Application code that calls AWS APIs | Requires application code, error handling, and credential management |
| CloudFormation / AWS CDK / Terraform | Defining and managing infrastructure declaratively | Requires state/stack management, planning, and review |

The CLI is not itself the same as Infrastructure as Code. You can create infrastructure using CLI commands, but for complex long-lived environments, IaC usually provides a clearer reviewable desired state, dependency management, and change history.

## 2. Install AWS CLI v2 safely

Download AWS CLI only from the official AWS documentation. Avoid third-party installers and copied binaries from unknown sources.

Official guide: [Installing or updating the latest version of the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

### macOS

AWS documents a signed `.pkg` installer. Follow the official page for the current installer and architecture, then verify:

```bash
aws --version
which aws
```

### Windows

Use the official AWS CLI v2 MSI installer from the AWS documentation. Then open a **new** PowerShell or Command Prompt window:

```powershell
aws --version
where.exe aws
```

If the command is not found, check whether the installer completed successfully and whether the AWS CLI install directory is on `PATH`. Restart the terminal after installation.

### Linux

Use the installation method documented by AWS for your distribution and CPU architecture. Verify:

```bash
aws --version
command -v aws
```

Do not assume a distribution's package manager always installs the latest CLI v2. Follow the official AWS instructions for the supported method.

### Expected verification

The version output begins with something similar to:

```text
aws-cli/2.x.x Python/3.x ...
```

The exact version and bundled runtime vary. The important check is that the command runs and reports version 2.

## 3. Authentication: choose a safe method

A CLI installation does not automatically grant access to an AWS account. The CLI must obtain credentials and know which Region/output format to use.

### Preferred options

For human access, prefer **AWS IAM Identity Center** or another organization-approved federated access method when available. Temporary credentials are generally preferable to long-lived IAM user keys.

For workloads running on AWS, prefer an **IAM role** attached to the service, such as an EC2 instance profile, rather than embedding access keys.

For local development or a training account, use the authentication method approved for your account. Do not create long-lived IAM user keys merely because a tutorial shows them.

### About `aws configure`

The classic interactive command is:

```bash
aws configure
```

It prompts for AWS Access Key ID, AWS Secret Access Key, default Region, and default output format. This stores credentials/configuration in the local AWS CLI files, commonly `~/.aws/credentials` and `~/.aws/config`. On Windows, the home directory contains the `.aws` folder as well.

**Security warning:** Access keys are secrets. Never paste them into chat, source control, screenshots, issue trackers, shell scripts, or shared machines. If a key is exposed, deactivate or rotate it immediately. Never use root-account access keys.

### Configure a named profile

Named profiles help separate accounts and environments.

```bash
aws configure --profile dev
aws configure --profile staging
aws sts get-caller-identity --profile dev
aws s3 ls --profile dev
```

You can set an environment variable in the current terminal session:

```bash
export AWS_PROFILE="dev"          # macOS/Linux Bash
export AWS_REGION="ap-south-1"
```

PowerShell:

```powershell
$env:AWS_PROFILE = "dev"
$env:AWS_REGION = "ap-south-1"
```

Environment variables can override configuration-file values. If commands unexpectedly use the wrong account or Region, inspect the active profile and environment.

### Configure a profile with IAM Identity Center

For an organization using IAM Identity Center, use the current official setup guide and then sign in with the CLI:

```bash
aws configure sso --profile work
aws sso login --profile work
aws sts get-caller-identity --profile work
```

The exact SSO start URL, account, role, and Region depend on your organization. Do not invent these values.

## 4. Verify identity and Region before doing anything

Always check which account and role your terminal is using before making changes.

```bash
aws sts get-caller-identity
aws configure list
aws configure list-profiles
```

Example identity response fields include `Account`, `Arn`, and `UserId`. Do not publish account IDs or ARNs from a real environment unnecessarily.

Specify the Region explicitly when the resource is regional:

```bash
aws ec2 describe-regions --region us-east-1
aws ec2 describe-instances --region ap-south-1
```

S3 bucket listing is not the same as inspecting regional EC2 resources. Many AWS services are regional; always check the Region in which the resource was created.

## 5. Learn the standard command structure

Most AWS CLI commands follow this structure:

```bash
aws <service> <operation> [options]
```

Examples:

```bash
aws s3 ls
aws ec2 describe-instances --region ap-south-1
aws iam list-roles
aws sts get-caller-identity
```

Use the built-in help:

```bash
aws help
aws s3 help
aws ec2 describe-instances help
```

### Output formats

```bash
aws ec2 describe-instances --output json
aws ec2 describe-instances --output table
aws ec2 describe-instances --output text
```

- `json` is useful for structured data and scripting.
- `table` is convenient for humans.
- `text` is compact but can be less clear for nested structures.

For automation, prefer JSON plus a deliberate `--query` expression over parsing visual table output.

### JMESPath queries with `--query`

List instance IDs and states:

```bash
aws ec2 describe-instances \\
  --query 'Reservations[].Instances[].{ID:InstanceId,State:State.Name,Type:InstanceType}' \\
  --output table
```

List only running instance IDs:

```bash
aws ec2 describe-instances \\
  --filters "Name=instance-state-name,Values=running" \\
  --query 'Reservations[].Instances[].InstanceId' \\
  --output text
```

A filter limits what the service returns when supported; `--query` filters the response on the client side. Use both appropriately.

## 6. Essential AWS CLI commands for DevOps

### Identity and account

```bash
aws sts get-caller-identity
aws configure list
aws configure list-profiles
```

### S3

```bash
aws s3 ls
aws s3 ls s3://YOUR_BUCKET/
aws s3 cp ./build.zip s3://YOUR_BUCKET/artifacts/build.zip
aws s3 cp s3://YOUR_BUCKET/artifacts/build.zip ./build.zip
aws s3 sync ./site/ s3://YOUR_BUCKET/site/
```

Use a real bucket you own. `sync --delete` can remove destination objects absent from the source; inspect both paths before using it.

### EC2

```bash
aws ec2 describe-instances --region ap-south-1
aws ec2 describe-images --owners amazon --region ap-south-1
aws ec2 describe-security-groups --region ap-south-1
aws ec2 describe-subnets --region ap-south-1
aws ec2 describe-vpcs --region ap-south-1
```

### IAM

```bash
aws iam list-roles
aws iam list-users
aws iam list-policies --scope Local
```

IAM is a global service in the common AWS partition endpoint model, so a Region parameter is not used for most IAM operations.

### CloudWatch

```bash
aws cloudwatch list-metrics --namespace AWS/EC2 --region ap-south-1
```

Metrics may not appear until the relevant service emits them. Custom metrics and detailed monitoring have additional considerations and possible charges.

## 7. Practical lab 1 — inspect S3 with the CLI

### Goal

Use the CLI to confirm identity, list buckets, upload a test file, download it, and verify the result.

### Step 1 — verify the active identity

```bash
aws sts get-caller-identity
```

If the identity is unexpected, stop and correct the profile before continuing.

### Step 2 — list buckets

```bash
aws s3 ls
```

This lists buckets the current identity is permitted to enumerate. An access error does not necessarily mean the CLI installation is broken.

### Step 3 — upload and download a test file

```bash
printf 'AWS CLI practice\\n' > cli-test.txt
aws s3 cp cli-test.txt s3://YOUR_BUCKET/lab/cli-test.txt
aws s3 cp s3://YOUR_BUCKET/lab/cli-test.txt ./cli-test-downloaded.txt
```

Replace `YOUR_BUCKET` with a bucket you own. Confirm the local file matches the downloaded copy.

### Step 4 — inspect object metadata

```bash
aws s3api head-object \\
  --bucket YOUR_BUCKET \\
  --key lab/cli-test.txt
```

This returns metadata for the object if the caller has permission. Clean up only the test object after verifying the bucket and key:

```bash
aws s3 rm s3://YOUR_BUCKET/lab/cli-test.txt
```

If versioning is enabled, this may create a delete marker rather than permanently erase historical versions.

## 8. Practical lab 2 — understand an EC2 launch command

Launching EC2 from the CLI requires multiple identifiers and configuration choices. Do not blindly paste a command from a tutorial: AMI IDs are Region-specific, and the subnet, security group, key pair, instance type, and IAM profile must match your environment.

Before launching, identify the AWS account and Region, supported AMI ID, subnet and VPC, security group, instance type/quota, key pair if SSH is needed, IAM instance profile if needed, storage/tags, network settings, and cost/cleanup plan.

Inspect the environment first:

```bash
aws ec2 describe-vpcs --region ap-south-1
aws ec2 describe-subnets --region ap-south-1
aws ec2 describe-security-groups --region ap-south-1
aws ec2 describe-key-pairs --region ap-south-1
```

Find a suitable Amazon-owned image rather than assuming a fixed AMI ID:

```bash
aws ec2 describe-images \\
  --owners amazon \\
  --filters "Name=name,Values=al2023-ami-2023.*-x86_64" \\
            "Name=state,Values=available" \\
  --query 'Images | sort_by(@, &CreationDate)[-5:].[ImageId,Name,CreationDate]' \\
  --output table \\
  --region ap-south-1
```

AMI naming patterns can change. Review results and select a current, supported image compatible with the instance architecture.

### Launch command template

This is a template, not a command to run unchanged. Replace every placeholder and verify network/security settings before launch.

```bash
aws ec2 run-instances \\
  --image-id AMI_ID \\
  --instance-type t3.micro \\
  --count 1 \\
  --subnet-id SUBNET_ID \\
  --security-group-ids SG_ID \\
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=aws-cli-lab},{Key=Project,Value=aws-zero-to-hero}]' \\
  --region ap-south-1
```

This minimal template intentionally does not specify a key pair. Add `--key-name KEY_PAIR_NAME` only if you need SSH and have secured the private key. If the subnet auto-assigns public IPs, review that behavior; do not make an instance public by accident. For production, prefer a Launch Template and Auto Scaling Group instead of repeated ad-hoc launch commands.

### Verify launch status

```bash
aws ec2 describe-instances \\
  --instance-ids INSTANCE_ID \\
  --query 'Reservations[].Instances[].{ID:InstanceId,State:State.Name,Type:InstanceType,PrivateIP:PrivateIpAddress,PublicIP:PublicIpAddress}' \\
  --output table \\
  --region ap-south-1
```

Wait for EC2 status checks if needed:

```bash
aws ec2 wait instance-status-ok \\
  --instance-ids INSTANCE_ID \\
  --region ap-south-1
```

### Clean up the lab instance

After testing, terminate only the instance you created for this lab:

```bash
aws ec2 terminate-instances \\
  --instance-ids INSTANCE_ID \\
  --region ap-south-1
```

Verify termination:

```bash
aws ec2 describe-instances \\
  --instance-ids INSTANCE_ID \\
  --query 'Reservations[].Instances[].{ID:InstanceId,State:State.Name}' \\
  --output table \\
  --region ap-south-1
```

Termination may not remove separately billed resources such as EBS volumes configured to persist, Elastic IPs, snapshots, load balancers, or NAT Gateways. Review those separately.

## 9. Safer automation patterns

### Use variables and strict shell settings

```bash
#!/usr/bin/env bash
set -euo pipefail

AWS_REGION="${AWS_REGION:-ap-south-1}"
AWS_PROFILE="${AWS_PROFILE:-dev}"

aws sts get-caller-identity \\
  --region "$AWS_REGION" \\
  --profile "$AWS_PROFILE"
```

`set -euo pipefail` can help reveal failures and unset variables, but it is not a substitute for explicit error handling and careful testing. Understand how pipelines, conditionals, and expected non-zero return codes behave in your script.

### Use tags

Tags help identify ownership, environment, and cleanup scope. Useful tag keys include `Project`, `Environment`, `Owner`, `CostCenter`, and `ManagedBy`. Tags alone do not enforce permissions or automatically delete resources.

### Prefer idempotent operations

A script is idempotent when repeating it has the same intended outcome rather than creating duplicate or conflicting resources. Many ad-hoc `create-*` commands are not idempotent by themselves. Check whether a resource already exists and use IaC when the desired state is complex.

### Use dry runs when supported

Some operations support `--dry-run`, including certain EC2 API operations. A dry run can validate permissions and parameters, but does not guarantee the real operation will succeed or that all runtime conditions are satisfied.

```bash
aws ec2 run-instances \\
  --image-id AMI_ID \\
  --instance-type t3.micro \\
  --count 1 \\
  --subnet-id SUBNET_ID \\
  --security-group-ids SG_ID \\
  --dry-run \\
  --region ap-south-1
```

Replace placeholders before use. EC2 may return a special `DryRunOperation` response when authorization succeeds; interpret it according to the command documentation.

## 10. Troubleshooting AWS CLI

| Error or symptom | Common cause | Recommended checks |
|---|---|---|
| `aws: command not found` / not recognized | Not installed or PATH not refreshed | Verify installation, restart terminal, inspect PATH |
| `Unable to locate credentials` | No credentials or profile selected | `aws configure list`, `aws configure list-profiles`, sign in using the approved auth method |
| `ExpiredToken` | Temporary credentials expired | Renew SSO/session credentials |
| `AccessDenied` | Missing permission, explicit Deny, wrong role, SCP or boundary | Confirm identity and exact API action/resource; inspect applicable policies |
| `InvalidClientTokenId` | Invalid/expired credentials or wrong credential source | Check active profile and credential source; rotate exposed keys |
| `SignatureDoesNotMatch` | Wrong credentials, system clock issue, or malformed signing context | Confirm profile/secret source, clock synchronization, Region and endpoint |
| `Could not connect to endpoint URL` | Network/DNS/proxy issue or wrong Region/endpoint | Check connectivity, DNS, proxy, Region and service endpoint |
| Resource not found | Wrong Region, ID, account, or resource state | Verify `get-caller-identity`, Region and exact ID |
| JSON parse or query error | Incorrect JMESPath expression or quoting | Start without `--query`, inspect JSON, then add query incrementally |
| Command succeeds but resource is not visible in console | Console is in another account/Region or filters hide resource | Confirm identity, Region, and console filters |

### Debugging sequence

1. Run `aws --version`.
2. Run `aws configure list`.
3. Run `aws sts get-caller-identity`.
4. Confirm profile and Region.
5. Re-run the command with the smallest valid arguments.
6. Read the exact service error message.
7. Check IAM permissions and explicit Deny controls.
8. Add `--debug` only when needed; logs may contain sensitive request metadata. Redact before sharing.
9. Avoid retrying destructive commands until the target resource is confirmed.

## 11. CLI security best practices

- Prefer IAM Identity Center/federation for human users where available.
- Prefer temporary credentials and AWS roles over long-lived access keys.
- Never use root credentials for everyday CLI work.
- Never commit `~/.aws/credentials`, access keys, tokens, or secret configuration.
- Use separate profiles for development, staging, and production.
- Confirm the account and Region before destructive actions.
- Apply least privilege and avoid `AdministratorAccess` as a default.
- Review `--debug` output before sharing.
- Use shell quoting correctly and avoid interpolating untrusted input into commands.
- Use CloudTrail and service logs where appropriate for auditing.
- For CI/CD, use supported OIDC/federated role integration instead of storing long-lived AWS keys whenever possible.

## 12. AWS CLI vs Infrastructure as Code

| Situation | Recommended starting point |
|---|---|
| List buckets or inspect an instance | AWS CLI |
| Upload a build artifact | AWS CLI or SDK |
| One-time diagnostic or operational action | AWS CLI |
| Repeatable VPC, subnets, ALB, ASG, and IAM roles | CloudFormation, CDK, or Terraform |
| Manage desired state across environments | IaC with version control and review |
| Application calls AWS services at runtime | AWS SDK with a role/temporary credentials |
| Emergency investigation | CLI/console as permitted, followed by documented remediation |

CLI commands can be useful inside scripts and pipelines, but a long script full of `create-*` commands may be hard to make safe, repeatable, and maintainable. For multi-resource infrastructure, IaC provides a declarative plan and change review.

## 13. Practice assignments

### Beginner
1. Install AWS CLI v2 and record the version output.
2. Configure an approved profile and verify identity.
3. List S3 buckets and describe EC2 instances in the correct Region.
4. Compare `json`, `table`, and `text` output.
5. Use `--query` to print instance IDs and states.

### Intermediate
1. Upload and download a file to a dedicated S3 lab bucket.
2. Create a named profile for a second approved environment and verify both identities.
3. Write a Bash script that checks the active account before listing resources.
4. Use EC2 `--dry-run` where supported and explain the result.
5. Launch a disposable EC2 instance only after verifying AMI, subnet, security group, and cost; then terminate it.

### Advanced
1. Build a safe inventory script for EC2 instances across two Regions.
2. Add error handling, structured output, tags, and logging.
3. Compare an ad-hoc CLI workflow with an equivalent Terraform or CloudFormation deployment.
4. Configure CI/CD using federated/temporary credentials rather than long-lived keys.
5. Design a guardrail that prevents a destructive script from running in the wrong AWS account.

## 14. Interview questions and concise answers

**1. What is the AWS CLI?** A command-line tool for calling AWS service APIs and managing resources.

**2. Why is the CLI useful for DevOps?** It supports repeatable commands, scripting, diagnostics, and integration into automation pipelines.

**3. Does installing the CLI give AWS permissions?** No. The CLI must obtain credentials, and the identity must be authorized for the requested operation.

**4. What does `aws configure` do?** It interactively configures credentials and default Region/output settings for a profile. Use an approved authentication method and avoid unnecessary long-lived keys.

**5. What is a named profile?** A named set of CLI configuration and credential settings used to separate environments or identities.

**6. How do you verify the active AWS identity?** Run `aws sts get-caller-identity`.

**7. How do you set the Region for a command?** Use `--region REGION`, or configure the profile/environment appropriately.

**8. What is `--query`?** A JMESPath expression that filters/transforms the CLI response on the client side.

**9. Difference between `--filters` and `--query`?** Service-side filters limit what the API returns when supported; `--query` transforms the response locally.

**10. Is the CLI an IaC tool?** It can create resources, but raw imperative commands do not inherently maintain desired state. Use CloudFormation/CDK/Terraform for complex managed infrastructure.

**11. What does `AccessDenied` usually mean?** The active principal lacks a required permission or an applicable policy explicitly denies the action. Confirm identity, resource, action, and policy layers.

**12. How should credentials be managed in CI/CD?** Prefer short-lived federated credentials and roles; avoid long-lived access keys stored in pipeline variables where federation is supported.

**13. Why might an EC2 instance be missing from `describe-instances`?** The command may use the wrong account or Region, wrong filters, or a different resource ID.

**14. Why inspect before terminating resources?** Termination is destructive and can affect workloads or data. Verify account, Region, instance ID, dependencies, and cleanup implications first.

**15. When should you use an SDK instead of CLI?** Use an SDK when an application needs to call AWS services programmatically as part of runtime behavior.

## 15. Official references

- [AWS CLI v2 User Guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html)
- [Install or update AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [Configure the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)
- [Configuration and credential file settings](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)
- [Named profiles](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html)
- [IAM Identity Center configuration for CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sso.html)
- [AWS CLI command reference](https://docs.aws.amazon.com/cli/latest/reference/)
- [AWS CLI filtering and `--query`](https://docs.aws.amazon.com/cli/latest/userguide/cli-usage-filter.html)
- [IAM security best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [EC2 `run-instances` reference](https://docs.aws.amazon.com/cli/latest/reference/ec2/run-instances.html)
- [AWS CloudFormation User Guide](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html)

## Key takeaway

The AWS CLI is a core DevOps tool for inspecting resources, executing operational tasks, and integrating AWS actions into scripts and pipelines. Install it from AWS's official source, use safe authentication, verify identity and Region before changing resources, read errors carefully, and prefer Infrastructure as Code for repeatable multi-resource environments.
