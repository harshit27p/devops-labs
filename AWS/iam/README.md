# Day 02 — AWS Identity and Access Management (IAM)

> **Learning series:** AWS DevOps Zero to Hero by Abhishek Veeramalla  
> **Video:** [Day-2 | AWS IAM deep dive with practicals and notes | IAM Project](https://www.youtube.com/watch?v=mCLYcsJ0GXQ)  
> **Reference repository:** [iam-veeramalla/aws-devops-zero-to-hero](https://github.com/iam-veeramalla/aws-devops-zero-to-hero)  
> **Level:** Beginner → Intermediate → Production concepts

## Table of contents

- [1. Learning objectives](#1-learning-objectives)
- [2. What is IAM?](#2-what-is-iam)
- [3. Authentication vs authorization](#3-authentication-vs-authorization)
- [4. IAM building blocks](#4-iam-building-blocks)
- [5. How IAM evaluates a request](#5-how-iam-evaluates-a-request)
- [6. IAM policy structure](#6-iam-policy-structure)
- [7. Managed policies vs inline policies](#7-managed-policies-vs-inline-policies)
- [8. Practical lab: user, S3 access denied, and permissions](#8-practical-lab-user-s3-access-denied-and-permissions)
- [9. Practical lab: use an IAM group](#9-practical-lab-use-an-iam-group)
- [10. AWS CLI validation](#10-aws-cli-validation)
- [11. IAM roles and temporary credentials](#11-iam-roles-and-temporary-credentials)
- [12. Security best practices](#12-security-best-practices)
- [13. Troubleshooting](#13-troubleshooting)
- [14. Common mistakes](#14-common-mistakes)
- [15. Interview questions and answers](#15-interview-questions-and-answers)
- [16. Assignment and validation checklist](#16-assignment-and-validation-checklist)
- [17. Cleanup](#17-cleanup)
- [18. Further reading](#18-further-reading)

## 1. Learning objectives

After completing this lesson, you should be able to:

- Explain IAM and distinguish authentication from authorization.
- Describe IAM users, groups, roles, and policies.
- Understand implicit deny, explicit deny, and least privilege.
- Create a learning IAM user and test the effect of missing permissions.
- Grant S3 permissions through a group rather than duplicating permissions on each user.
- Validate access in the console and with AWS CLI.
- Explain why production workloads should generally use roles and temporary credentials.

## 2. What is IAM?

**AWS Identity and Access Management (IAM)** is the AWS service used to control who can authenticate and which AWS actions they can perform on which resources, subject to applicable policies and conditions.

Think of an organization as a bank:

- **Identity:** the person presenting credentials.
- **Authentication:** the bank verifies the person's identity.
- **Authorization:** the bank checks whether that person may view an account, transfer funds, or close it.
- **Policy:** the rules that specify the permitted actions.
- **Audit trail:** records that help investigate which identity made a request.

The same separation applies in AWS. Successfully signing in does **not** automatically grant permission to use EC2, S3, IAM, or another service.

### Why IAM matters to DevOps

DevOps automation interacts with cloud APIs to deploy infrastructure, publish images, retrieve configuration, and release applications. IAM limits the blast radius if a credential or automation pipeline is misused. A deployment pipeline that only needs to upload artifacts should not receive unrestricted administrator access.

## 3. Authentication vs authorization

| Concept | Question answered | AWS example |
|---|---|---|
| Authentication | Who are you? | Sign in using an approved identity and credentials |
| Authorization | What may you do? | IAM evaluates whether `s3:ListAllMyBuckets` is allowed |
| Auditing | What happened? | CloudTrail records supported API activity |

A request generally succeeds only when the caller is authenticated and the applicable authorization evaluation permits the requested action. A valid password does not override missing permissions.

## 4. IAM building blocks

### 4.1 IAM user

An IAM user is an identity in an AWS account. Depending on how it is configured, it can have a console password and/or programmatic credentials. IAM users can have permissions attached directly or inherit permissions from groups.

**Learning use:** a sandbox user helps demonstrate what happens when no permissions have been granted.

**Production note:** AWS recommends temporary credentials for human users where possible. For workforce access, evaluate IAM Identity Center or federation rather than creating a separate long-term IAM user for every employee.

### 4.2 IAM group

A group is a collection of IAM users. Policies attached to a group grant those permissions to its members. Groups are useful for assigning permissions by job function, such as read-only auditors or developers who can access a specific application bucket.

- Groups contain users, not other groups.
- A group is a permission-management convenience, not a login identity.
- A user can belong to multiple groups; applicable permissions are evaluated together.
- Direct user policies may still apply, so group membership alone does not describe every effective permission.

### 4.3 IAM policy

A policy is a JSON permissions document. It specifies actions, resources, effects, and optionally conditions. Policies can be attached to identities or, for supported services, to resources.

Examples of S3 actions:

- `s3:ListAllMyBuckets` — list bucket names in the account through the relevant API.
- `s3:ListBucket` — list objects within a specified bucket.
- `s3:GetObject` — read an object.
- `s3:PutObject` — upload or replace an object.
- `s3:DeleteObject` — delete an object.

These are different permissions. Permission to list bucket names does not automatically mean permission to read the objects inside those buckets.

### 4.4 IAM role

A role is an identity with a permission policy and a **trust policy** describing who or what may assume it. When a principal assumes a role, AWS provides temporary security credentials for the session.

Typical uses:

- An EC2 application reads from an S3 bucket.
- A Lambda function writes logs or accesses a data store.
- A CI/CD workflow deploys into an AWS account using a trusted federation mechanism.
- A user from one AWS account assumes a role in another account.

A role is not simply an IAM user with a different name. It is designed to be assumed by an authorized principal and normally uses temporary credentials.

### Quick comparison

| Feature | User | Group | Policy | Role |
|---|---|---|---|---|
| Represents | An identity | A set of users | Permission rules | An assumable identity |
| Can sign in directly? | If configured | No | No | No; must be assumed by a trusted principal |
| Holds permission rules? | Can have policies attached | Can have policies attached | Defines permissions | Can have permission policies attached |
| Typical use | Learning or specific legacy cases | Job-function permissions | Describe allowed/denied actions | Workloads, federation, cross-account access |
| Credential pattern | Can have long-term credentials | None | None | Temporary credentials when assumed |

## 5. How IAM evaluates a request

AWS authorization is not a simple rule that “one Allow means access.” Several applicable policy types and account-level controls can affect the final decision.

1. **Implicit deny is the default.** If no applicable policy allows the request, it is denied.
2. **An applicable Allow** can permit the action, provided other applicable controls do not block it.
3. **An explicit Deny overrides an Allow.** An explicit deny in an applicable policy results in denial.
4. **Additional guardrails matter.** Depending on the environment, service control policies (SCPs), resource control policies (RCPs), permissions boundaries, session policies, resource policies, and other controls may affect the result.
5. **Cross-account access requires the appropriate authorization on both sides.** The exact requirements depend on the principal, resource, and policy type.

### Conceptual decision flow

```text
Request to an AWS API
        |
        v
Authenticate the principal
        |
        v
Evaluate applicable policies and guardrails
        |
        +---- Applicable explicit Deny? ---- Yes ---> DENY
        |
        No
        |
        +---- Required Allow and constraints satisfied? -- No --> DENY
        |
       Yes
        |
        v
      ALLOW
```

### Example

An IAM user can sign in to the AWS console but has no policy granting S3 listing. The user opens S3 and receives an access-denied message. This is expected: authentication worked, but authorization did not allow the operation.

## 6. IAM policy structure

A typical identity-based policy contains a version and one or more statements:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowListingBucketNames",
      "Effect": "Allow",
      "Action": "s3:ListAllMyBuckets",
      "Resource": "*"
    }
  ]
}
```

| Element | Meaning |
|---|---|
| `Version` | Policy language version; `2012-10-17` is the standard version used in current examples |
| `Statement` | Array of permission statements |
| `Sid` | Optional statement identifier for readability |
| `Effect` | `Allow` or `Deny` |
| `Action` | API actions covered by the statement |
| `Resource` | Resource ARNs to which the statement applies, or `*` where appropriate |
| `Condition` | Optional constraints such as requested context or source network |

**Important:** `Resource: "*"` is broad in scope. Some list or discovery actions require `*`, but that does not mean all S3 permissions should be granted on all resources. Use the narrowest resource scope supported by each action.

### Policy types to recognize

- **Identity-based policy:** attached to a user, group, or role.
- **Resource-based policy:** attached to a supported resource, such as an S3 bucket policy.
- **AWS-managed policy:** created and maintained by AWS.
- **Customer-managed policy:** created and maintained in your account; reusable across identities.
- **Inline policy:** embedded directly into one identity.
- **Permissions boundary:** sets a maximum permissions boundary for a user or role; it does not grant permissions by itself.
- **Session policy:** can reduce permissions for a role session; it does not grant permissions beyond the role's permissions.
- **SCP/RCP:** organization-level guardrails that set maximum available permissions in applicable contexts; they do not themselves grant permissions.

## 7. Managed policies vs inline policies

| Policy type | Advantages | Considerations |
|---|---|---|
| AWS-managed | Quick to apply; maintained by AWS | May grant more permissions than a particular job needs; review its current definition |
| Customer-managed | Reusable, versioned, and tailored to your requirements | Your team owns maintenance and review |
| Inline | Direct one-to-one relationship with an identity | Harder to reuse and govern at scale |

For a quick learning demonstration, an AWS-managed policy can make the permissions change visible. In real environments, prefer least-privilege policies designed for the task. Avoid attaching `AdministratorAccess` or broad service-full-access policies merely to make an error disappear.

## 8. Practical lab: user, S3 access denied, and permissions

### Lab goal

Create a learning user with no S3 permissions, verify the denial, grant only the permission needed to list bucket names, and test again.

### Safety and prerequisites

- Use an account where you are authorized to administer IAM.
- Keep root credentials secure and do not use root for routine lab work.
- Enable MFA on privileged identities.
- Do not create access keys for the root user.
- This lab does not require creating an S3 bucket. If you create additional resources, check costs and remove them afterwards.
- Console labels can change; follow the equivalent IAM actions if the UI differs.

### Step 1 — Open IAM

1. Sign in using an authorized administrator identity.
2. Open the AWS Management Console and navigate to **IAM**.
3. Confirm you are working in the intended AWS account. IAM is account-scoped, so check the account identity before changing permissions.

### Step 2 — Create a lab user

1. In IAM, open **Users** and choose **Create user**.
2. Enter a clear lab name such as `iam-s3-lab-user`.
3. If the exercise requires console access, configure it according to the console's current workflow and your lab needs.
4. Do **not** attach S3 permissions yet.
5. Complete creation and securely record the lab sign-in method. Never publish passwords or access keys in GitHub notes.

> For production workforce access, prefer IAM Identity Center or federation and temporary credentials. The IAM-user workflow here is an educational exercise to make permission evaluation easy to observe.

### Step 3 — Test without permissions

1. Sign in as the lab user using its assigned sign-in method.
2. Open the S3 console.
3. Try to list buckets.
4. Observe the access-denied response or empty/blocked console view.

The exact console error can vary. The key result is that the identity has no applicable Allow for the requested S3 operation. Do not interpret the denial as a broken S3 service.

### Step 4 — Grant permission to list bucket names

For the narrowest API-level test, create a customer-managed policy with the JSON below and attach it to the lab user. This grants bucket-name listing only; it does **not** grant access to bucket contents.

Save as `s3-list-buckets-policy.json` if you want to keep the policy in your lab repository:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ListBucketNamesForLab",
      "Effect": "Allow",
      "Action": "s3:ListAllMyBuckets",
      "Resource": "*"
    }
  ]
}
```

Console steps:

1. In IAM, open **Policies** and choose **Create policy**.
2. Use the JSON editor and paste the policy.
3. Validate the JSON and give the policy a name such as `LabListS3BucketNames`.
4. Create the policy.
5. Open **Users**, select `iam-s3-lab-user`, and attach the policy under permissions.
6. Sign out and sign in again if needed, then retry the S3 bucket-listing operation.

**Expected result:** the user can request the list of bucket names, subject to other applicable policies and account controls. The user still cannot read, upload, or delete objects just because this policy allows bucket-name listing.

### Step 5 — Optional: allow listing objects in one specific bucket

Only do this if you have an existing bucket you are authorized to use. Replace `YOUR_BUCKET_NAME` with the actual bucket name:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ListObjectsInOneBucket",
      "Effect": "Allow",
      "Action": "s3:ListBucket",
      "Resource": "arn:aws:s3:::YOUR_BUCKET_NAME"
    }
  ]
}
```

This permits listing object keys in the named bucket. It does not grant `s3:GetObject`, `s3:PutObject`, or `s3:DeleteObject`. To use the S3 console smoothly, additional read-only console permissions may be needed; add only the actions required for the intended task.

### Step 6 — Compare with a broad managed policy (demonstration only)

The video demonstrates attaching an AWS-managed S3 full-access policy to show how permissions change. If you reproduce that demonstration, do so only in a disposable learning account, understand that it grants broad S3 permissions, and detach it immediately after observing the result. **Do not use S3 full access as the default solution in production.** The scoped policy above is safer for the listing exercise.

## 9. Practical lab: use an IAM group

### Goal

Grant the same permission to multiple users through a group instead of attaching an identical policy to every user individually.

### Steps

1. In IAM, open **User groups** and choose **Create group**.
2. Name it `S3BucketListingLab`.
3. Attach the customer-managed `LabListS3BucketNames` policy to the group.
4. Add `iam-s3-lab-user` to the group.
5. If you created a direct attachment to the user in the previous lab, remove it to demonstrate group-based permission inheritance. Ensure no other policy is granting the same access during the test.
6. Sign in as the user and list buckets again.
7. Add a second disposable lab user to the same group and verify that the group policy applies to both members.
8. Remove one user from the group and retest. The group-provided permission should no longer apply to that user, unless another applicable policy grants it.

### Why groups help

Without groups, an administrator might attach and maintain the same policy separately on many users. A group lets the administrator manage a permission set centrally by job function. In larger environments, use this idea alongside IAM Identity Center permission sets and federated identity management where appropriate.

## 10. AWS CLI validation

The AWS CLI provides a programmatic way to check identity and S3 access. Use a supported authentication method for the lab identity. Do not place access keys directly in scripts, source code, screenshots, or Git commits.

### Configure a lab profile

If your lab explicitly uses IAM user access keys, create them only for this temporary exercise, store them using the CLI's supported credential configuration, and delete them when finished. For example:

```bash
aws configure --profile iam-lab
```

The CLI prompts for access key ID, secret access key, default region, and output format. These values are secrets. Never paste them into this README or commit local credential files.

Where available, prefer temporary credentials and supported sign-in flows rather than long-lived access keys.

### Confirm the active identity

```bash
aws sts get-caller-identity --profile iam-lab
```

This returns the account and principal ARN associated with the credentials currently in use. It helps detect accidentally testing with an administrator profile.

### Test bucket listing

```bash
aws s3api list-buckets --profile iam-lab
```

- Before permission is granted, expect an `AccessDenied`-style response.
- After attaching the `s3:ListAllMyBuckets` policy, expect a response listing bucket metadata, possibly an empty list if the account has no buckets.
- If access is still denied, check the active profile, attached policies, explicit denies, permissions boundaries, session policies, and organization guardrails.

### Test object listing in a named bucket

```bash
aws s3api list-objects-v2 \
  --bucket YOUR_BUCKET_NAME \
  --profile iam-lab
```

This operation requires `s3:ListBucket` on the bucket ARN. Replace the placeholder with a bucket you own or are authorized to access.

## 11. IAM roles and temporary credentials

### Why roles are central to DevOps

Suppose an EC2-hosted application must download a deployment artifact from S3. A fragile approach is to store a permanent IAM user's access key in a file on the server. If the file leaks, the credential can be reused until it is revoked or rotated.

A better design is:

1. Create an IAM role with a trust policy that allows the intended AWS service or trusted principal to assume it.
2. Attach a least-privilege permissions policy to that role.
3. Associate the role with the compute resource or configure the trusted federation mechanism.
4. Let the workload obtain temporary credentials through the supported AWS credential provider.
5. Audit and refine permissions as the workload evolves.

### Two different policy questions

- **Trust policy:** who is allowed to assume this role?
- **Permissions policy:** what can the role do after it is assumed?

A role needs the correct trust relationship and appropriate permissions. Giving a role S3 permissions does not, by itself, authorize every principal to assume it.

### Common role scenarios

| Scenario | Preferred pattern |
|---|---|
| EC2 application reads one S3 bucket | EC2 instance role with narrowly scoped S3 permissions |
| Lambda function writes logs | Execution role with required logging permissions |
| CI/CD job deploys to AWS | Federated/OIDC role with restricted trust and deployment permissions |
| Engineer accesses multiple AWS accounts | IAM Identity Center or federation, with appropriate role/permission sets |
| External AWS account accesses a resource | Deliberate cross-account role or resource policy design, including trust and permissions |

## 12. Security best practices

1. **Protect the root user.** Enable MFA, use a strong unique password, and avoid routine root sign-in. Do not create root access keys.
2. **Use temporary credentials where possible.** Prefer federation, IAM Identity Center, and roles for workforce users and workloads.
3. **Apply least privilege.** Grant only required actions, resources, and conditions. Avoid broad policies such as `AdministratorAccess` unless the role genuinely requires them and the risk is controlled.
4. **Prefer groups or centrally managed permission sets for job functions.** Avoid inconsistent per-user permission attachments at scale.
5. **Separate duties.** A build job, deploy job, auditor, and administrator rarely need identical permissions.
6. **Enable MFA for privileged access.** Use phishing-resistant MFA, such as security keys or passkeys, where supported.
7. **Protect credentials.** Never commit secrets to GitHub, bake credentials into container images, or place long-term keys in application code.
8. **Review and remove unused access.** Examine last-used information, old access keys, unused identities, and unnecessary policies.
9. **Use conditions thoughtfully.** Conditions can restrict access by attributes such as source identity, tags, network context, or transport security when supported by the service.
10. **Monitor and investigate.** Use CloudTrail and appropriate monitoring to review API activity and investigate unexpected access.
11. **Use organization guardrails carefully.** SCPs and related controls limit permissions; they do not replace identity-level grants.
12. **Test changes safely.** Use policy simulation and a non-production account before applying significant permission changes.

## 13. Troubleshooting

| Symptom | Likely cause | What to check |
|---|---|---|
| User can sign in but S3 is denied | No applicable S3 Allow | Check attached user and group policies |
| Policy appears attached but request fails | Explicit Deny or another limiting control | Inspect all applicable policies, boundaries, session policies, SCPs/RCPs, and bucket policy |
| `list-buckets` fails | Missing `s3:ListAllMyBuckets` or wrong credentials | Run `aws sts get-caller-identity`; check active profile and policy action |
| Bucket names are visible but objects cannot be listed | `s3:ListBucket` is missing | Add scoped `s3:ListBucket` on the bucket ARN if required |
| Object listing works but object download fails | `s3:GetObject` is missing or resource access is blocked | Check object ARN, bucket policy, encryption permissions, and applicable denies |
| Console page displays additional errors | Console makes multiple API calls | Grant only required console-related actions; do not jump straight to full access |
| Group member lacks expected permission | User not in group, policy attached incorrectly, or a deny applies | Verify group membership and effective policies |
| CLI succeeds as admin but fails as lab user | Wrong profile used in one test | Use `--profile iam-lab` and confirm caller identity |
| Access still fails after a policy change | Policy is malformed, wrong action/resource, or another control blocks it | Validate JSON and inspect the complete access-denied message |

For difficult cases, consult the AWS IAM access-denied troubleshooting guide linked below. Avoid removing security guardrails simply to make a lab pass.

## 14. Common mistakes

- Confusing authentication with authorization.
- Assuming a user gets permissions merely because it exists.
- Assuming `s3:ListAllMyBuckets`, `s3:ListBucket`, and `s3:GetObject` are interchangeable.
- Treating `Resource: "*"` as harmless in every policy.
- Granting full administrator or service access to fix a narrowly scoped permission problem.
- Forgetting that explicit Deny overrides Allow.
- Assuming a role's trust policy and permissions policy serve the same purpose.
- Using long-lived access keys for an EC2 instance or CI/CD workload when role-based temporary credentials are available.
- Running tests with the wrong AWS CLI profile.
- Committing policy files containing actual account secrets, credentials, or sensitive infrastructure details.
- Leaving temporary lab users or access keys active after the assignment.

## 15. Interview questions and answers

### Beginner

**1. What is AWS IAM?**  
IAM controls access to AWS resources by managing identities, credentials, and permissions.

**2. What is the difference between authentication and authorization?**  
Authentication establishes who the caller is; authorization determines which actions that caller may perform.

**3. What is an IAM user?**  
An identity in an AWS account that can be configured with credentials and permissions. For workforce access, AWS generally recommends temporary credentials and centralized identity solutions where possible.

**4. Why do we use IAM groups?**  
To assign and maintain common permissions for multiple users by role or responsibility.

**5. What is an IAM policy?**  
A document that specifies allowed or denied actions on resources, optionally subject to conditions.

**6. What is an IAM role?**  
An identity that trusted principals can assume to receive temporary credentials and the role's permissions.

### Intermediate

**7. What is the difference between an IAM role and an IAM user?**  
A user can have long-term credentials; a role is assumed by an authorized principal and normally provides temporary credentials for a session.

**8. What is least privilege?**  
Giving an identity only the permissions needed for its task, scoped to the smallest practical set of resources and conditions.

**9. What is the difference between implicit deny and explicit deny?**  
Implicit deny occurs when no applicable Allow grants the request. Explicit deny is a matching Deny statement and overrides an Allow.

**10. What is the difference between AWS-managed and customer-managed policies?**  
AWS maintains AWS-managed policies. The customer creates and maintains customer-managed policies, allowing tighter tailoring to their needs.

**11. Does `s3:ListAllMyBuckets` let a user download objects?**  
No. It allows listing bucket names; object access needs the appropriate additional permissions and resource authorization.

**12. What is the difference between a role trust policy and a permissions policy?**  
The trust policy determines who can assume the role. The permissions policy determines what the assumed role can do.

### Scenario-based

**13. A developer can sign in but cannot list S3 buckets. How do you debug it?**  
Confirm the identity, inspect user/group policies, verify `s3:ListAllMyBuckets`, check for explicit denies and limiting controls, and retest with the same identity.

**14. Five developers need the same S3 read permissions. Would you attach the policy five times?**  
For an IAM-user learning exercise, a group can centralize those permissions. In an organization, consider IAM Identity Center permission sets or federation as appropriate.

**15. An EC2 application needs to download one file from S3. Would you put access keys on the instance?**  
Prefer an instance role with the minimum S3 permissions required for the relevant bucket/object. This avoids distributing long-lived credentials.

**16. A policy allows `s3:GetObject`, but the request is denied. Why?**  
Possible causes include an explicit deny, wrong object ARN, bucket policy restrictions, a permissions boundary, session policy, organization guardrail, encryption key permissions, or a different active identity.

**17. Why is full S3 access usually a poor fix for an access-denied error?**  
It gives more authority than the specific task may need and increases the impact of credential misuse. Diagnose the required API action and resource instead.

**18. How would you provide AWS permissions to a CI/CD pipeline?**  
Prefer a trusted federation mechanism such as OIDC to assume a role with restricted trust conditions and least-privilege deployment permissions. Avoid storing long-lived access keys in pipeline variables when a temporary-credential option is available.

## 16. Assignment and validation checklist

Complete the following in a lab account where you have permission to administer IAM:

- [ ] Create a lab IAM user without S3 permissions.
- [ ] Sign in as that user and attempt to list S3 buckets.
- [ ] Record the access-denied result without sharing credentials or sensitive account details.
- [ ] Create and attach a policy that allows only `s3:ListAllMyBuckets`.
- [ ] Verify that bucket-name listing now works, subject to other account controls.
- [ ] Verify that bucket listing does not automatically grant object read/write access.
- [ ] Create an IAM group and attach the policy to the group.
- [ ] Add the lab user to the group and verify inherited permissions.
- [ ] Add a second lab user and verify group-based permission management.
- [ ] Remove a user from the group and confirm group-granted access is removed unless another policy grants it.
- [ ] Use `aws sts get-caller-identity` to verify the CLI principal.
- [ ] Explain the difference between an IAM user, group, policy, and role.
- [ ] Explain why workload roles and temporary credentials are preferred over hard-coded keys.
- [ ] Remove temporary credentials and lab resources when finished.

### Suggested evidence for a lab report

Capture screenshots of the policy attachment, group membership, and the before/after access result. Redact account identifiers where appropriate and **never include passwords, secret access keys, session tokens, QR codes, or MFA recovery codes**.

## 17. Cleanup

After recording the results:

1. Remove any broad demonstration policy such as S3 full access.
2. Delete temporary access keys created solely for this exercise.
3. Remove lab users from groups and delete the lab identities/policies if they are no longer needed.
4. Keep only the minimum access required for any continuing coursework.
5. Review the account for other resources created during the exercise and remove them if safe and no longer needed.

Do not delete identities or policies that other applications or learners rely on. Confirm ownership and dependencies before cleanup.

## 18. Further reading

Official AWS documentation is the authority for current behavior and console steps:

- [IAM overview and identity concepts](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html)
- [Compare IAM identities and credentials](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction_identity-management.html)
- [IAM policies and permissions](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html)
- [IAM access management and policy evaluation](https://docs.aws.amazon.com/IAM/latest/UserGuide/access.html)
- [IAM security best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [Root user best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/root-user-best-practices.html)
- [Troubleshoot IAM access-denied errors](https://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_access-denied.html)
- [Amazon S3 identity-based policy examples](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security_iam_id-based-policy-examples.html)
- [AWS IAM Identity Center](https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html)
- [Video: AWS IAM deep dive with practicals](https://www.youtube.com/watch?v=mCLYcsJ0GXQ)
- [Course repository: AWS DevOps Zero to Hero](https://github.com/iam-veeramalla/aws-devops-zero-to-hero)

---

**Scope note:** These notes expand the user-provided summary of the video with additional IAM concepts and current AWS security guidance. They are not a word-for-word transcript. Always check the official AWS documentation before applying permissions in a production account.
