# AWS Zero to Hero --- Amazon S3 Fundamentals and Practical Labs

> **Video:** [AWS Zero to Hero --- Amazon
> S3](https://www.youtube.com/watch?v=DiWWPo2Qoso&list=PLdpzxOOAlwvIc1TjTwopNSjRJkzES2ZXk&index=63)\
> **Suggested repository path:** `08-amazon-s3/README.md`\
> **Focus:** S3 fundamentals, buckets and objects, access control,
> static website hosting, versioning, lifecycle policies, cost
> optimization, AWS CLI, troubleshooting, and interview preparation.

These notes provide a practical companion to the video description. AWS
console labels and pricing can change, so consult the official
documentation linked at the end before using these steps in production.

## 1. What is Amazon S3?

Amazon Simple Storage Service (S3) is a managed object-storage service
for storing and retrieving data at scale. Common use cases include
application logs, backups, static website assets, media files, build
artifacts, reports, and data lakes.

S3 is not a traditional block device or shared network filesystem.
Applications interact with objects through APIs, SDKs, the AWS CLI, and
supported integrations.

### Core terminology

  -----------------------------------------------------------------------
  Term                                Meaning
  ----------------------------------- -----------------------------------
  Bucket                              Container for objects; names are
                                      unique within an AWS partition.

  Object                              Stored data plus metadata.

  Key                                 Object name,
                                      e.g. `images/logo.png`.

  Prefix                              Leading part of a key,
                                      e.g. `logs/2026/10/`; folder-like
                                      organization rather than a
                                      traditional directory.

  Region                              Region where the bucket is created.

  Version ID                          Identifies a version when
                                      versioning is enabled.

  Storage class                       Storage and retrieval
                                      characteristics with different
                                      costs.

  Lifecycle rule                      Policy to transition or expire
                                      eligible objects or versions.
  -----------------------------------------------------------------------

### Object vs block vs file storage

-   **Object storage --- S3:** API-based storage for backups, logs,
    datasets, and static assets.
-   **Block storage --- EBS:** Disk volumes attached to compute
    instances.
-   **File storage --- EFS/FSx:** Shared filesystem access and directory
    semantics.

S3 keys can contain `/` characters, but the underlying namespace is
key-based.

## 2. Durability, availability, and scalability

S3 Standard is designed for **99.999999999% (11 nines) annual
durability**. Durability means data is designed to be retained reliably;
availability describes how often it can be accessed. Neither guarantees
recovery from accidental deletion, malicious changes, compromised
credentials, or application-level corruption.

Good design habits:

-   Choose the Region based on latency, compliance, and cost.
-   Keep Block Public Access enabled by default.
-   Enable versioning for important data where it fits the recovery and
    cost model.
-   Use least-privilege IAM and bucket policies.
-   Encrypt data at rest and use HTTPS in transit.
-   Monitor access and configuration changes.
-   Define retention and restore requirements before setting expiration
    rules.

## 3. Create a practice bucket

Use a unique name such as `your-s3-lab-<unique-suffix>`; bucket names
are globally unique within the AWS partition.

1.  Open the S3 console and select **Create bucket**.
2.  Choose a Region and unique name.
3.  Keep **Block all public access** enabled.
4.  Keep ACLs disabled / **Bucket owner enforced** Object Ownership
    unless a specific legacy requirement exists.
5.  Enable default encryption. SSE-S3 is a simple default; use SSE-KMS
    when its key controls and audit features are needed and its
    permissions/costs are understood.
6.  Enable versioning for the versioning exercise.
7.  Add tags such as `Project=aws-zero-to-hero` and `Environment=lab`.

Do not use a production bucket for practice. Never upload passwords,
private keys, tokens, or confidential data.

## 4. Upload and retrieve an object

Create `hello.txt`:

``` text
Hello from Amazon S3.
This object is part of my AWS Zero to Hero practice lab.
```

Upload it through the console, then download it and compare the
contents. Example object layout:

``` text
uploads/hello.txt
logs/app/2026/10/app.log
backups/database/backup.sql.gz
website/index.html
website/assets/style.css
```

These are object-key prefixes, not real filesystem directories.

## 5. Storage classes

Storage classes trade off storage price, access latency, availability
design, minimum storage duration, retrieval fees, and restore time.
Verify current regional pricing before choosing.

  -----------------------------------------------------------------------
  Storage class                       Typical use
  ----------------------------------- -----------------------------------
  S3 Standard                         Frequently accessed data needing
                                      low-latency access

  S3 Intelligent-Tiering              Access patterns that are uncertain
                                      or change over time;
                                      monitoring/optional archive tiers
                                      have considerations

  S3 Standard-IA                      Infrequent access with rapid
                                      retrieval; minimum duration and
                                      retrieval charges apply

  S3 One Zone-IA                      Infrequent access where single-AZ
                                      storage is acceptable and data is
                                      recreatable

  S3 Glacier Instant Retrieval        Archive data needing millisecond
                                      retrieval

  S3 Glacier Flexible Retrieval       Archive data where retrieval may
                                      take minutes to hours

  S3 Glacier Deep Archive             Long-term archive where retrieval
                                      can take many hours
  -----------------------------------------------------------------------

Before selecting a class, ask: How often is data accessed? How fast must
it be retrieved? How long is it retained? Is single-AZ storage
acceptable? Are minimum durations, minimum billable object sizes,
transition, request, or retrieval costs relevant?

**Common mistake:** Choosing the lowest storage price without
calculating retrieval charges, restore time, minimum duration, and
transition costs.

## 6. IAM policies and bucket policies

S3 authorization may involve identity policies, bucket policies, access
point policies, organization controls, and KMS key policies. A request
must satisfy all applicable controls.

-   **IAM identity policy:** Attached to a user, group, or role; grants
    actions on resources.
-   **Bucket policy:** Resource-based policy attached to a bucket; can
    grant or deny access and enforce conditions.
-   **Explicit Deny:** An applicable explicit `Deny` overrides an
    `Allow`. However, merely omitting a principal from a bucket policy
    does not automatically deny permissions granted by another
    applicable policy.

### Example: deny requests without TLS

Replace `YOUR_BUCKET` with your actual bucket name and merge this
statement into the existing bucket policy as needed.

``` json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyInsecureTransport",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::YOUR_BUCKET",
        "arn:aws:s3:::YOUR_BUCKET/*"
      ],
      "Condition": {
        "Bool": {
          "aws:SecureTransport": "false"
        }
      }
    }
  ]
}
```

This does not make the bucket public. Preserve other statements required
by your workload and test policy changes in a lab first.

### Example: allow a specific role to read objects

Replace the placeholders. Listing objects is a separate permission
(`s3:ListBucket`) on the bucket ARN and should only be granted when
required.

``` json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowSpecificRoleReadObjects",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::ACCOUNT_ID:role/ROLE_NAME"
      },
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::YOUR_BUCKET/*"
    }
  ]
}
```

### Safe permission-testing workflow

1.  Create a dedicated test role or user with minimal permissions.
2.  Upload a non-sensitive object.
3.  Test the allowed action and one disallowed action.
4.  Check the exact error and CloudTrail event if enabled.
5.  Remove the test identity and lab objects afterward.

Avoid granting `s3:*` on `*` just to make an error disappear.

## 7. Block Public Access

S3 Block Public Access provides account-, bucket-, and
access-point-level controls to help prevent public exposure. Keep it
enabled unless public access is an explicit, reviewed requirement.

For public static content, a common production design is **private S3
bucket + CloudFront + Origin Access Control (OAC)** rather than making
the bucket public. Review the data in the bucket, policies, ACL/object
ownership settings, access points, and organization controls before
changing public-access settings.

## 8. Static website hosting --- learning lab

S3 website hosting serves static files such as HTML, CSS, JavaScript,
and images. It does not run server-side Python, PHP, Node.js, or other
application code.

**HTTPS caveat:** The direct S3 website endpoint does not support HTTPS
directly. For a secure public site, prefer CloudFront with a certificate
and a private S3 origin protected by OAC. A direct public S3 website is
only appropriate for a deliberate, non-sensitive lab.

### Step 1 --- Create website files

`index.html`:

``` html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AWS S3 Lab</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <main>
    <h1>Hello from Amazon S3</h1>
    <p>This is a static website deployed for my AWS learning lab.</p>
  </main>
</body>
</html>
```

`style.css`:

``` css
body {
  font-family: system-ui, sans-serif;
  max-width: 760px;
  margin: 4rem auto;
  padding: 0 1rem;
  line-height: 1.6;
}
```

### Step 2 --- Enable website hosting

1.  Create a dedicated, unique bucket for the website experiment.
2.  Upload `index.html` and `style.css` to the bucket root.
3.  Open **Properties → Static website hosting**.
4.  Enable website hosting and set the index document to `index.html`.
5.  Save and copy the **Bucket website endpoint**.

### Step 3 --- Public-read policy for a disposable lab only

To access a direct S3 website endpoint publicly, objects need
public-read access and the relevant Block Public Access settings must
permit it. This deliberately weakens the secure default. Do not use it
for sensitive content or disable account-wide protections merely to
complete a lab.

``` json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadWebsiteObjectsOnly",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::YOUR_WEBSITE_BUCKET/*"
    }
  ]
}
```

Replace `YOUR_WEBSITE_BUCKET`. This grants anonymous read access to
every matching object in that bucket. Never store secrets or private
files there.

### Step 4 --- Test

Open the website endpoint shown in the bucket properties. If it fails,
check the endpoint, index document, object keys, bucket policy, Block
Public Access, and Region. The website endpoint and the S3 REST API
endpoint are different.

### Preferred production pattern

-   Keep the S3 bucket private.
-   Use CloudFront with Origin Access Control.
-   Attach an ACM certificate for HTTPS.
-   Point your DNS hostname to CloudFront.
-   Plan logging, caching, and invalidation.

## 9. Versioning

S3 Versioning retains multiple versions of an object under the same key
and can help recover from accidental overwrites or deletes.

### Exercise

1.  Open the bucket's **Properties → Bucket Versioning**.
2.  Enable versioning.
3.  Upload `hello.txt`.
4.  Change its contents and upload it again using the same key.
5.  View the object's versions and compare them.
6.  Delete the current object in the lab and inspect whether a delete
    marker appears.

Important behavior:

-   Overwriting a key creates a new version.
-   A normal delete usually adds a delete marker rather than permanently
    removing every version.
-   Older versions consume storage and may continue to incur charges.
-   Permanently deleting a specific version requires its version ID and
    permission.
-   Suspending versioning does not remove versions already stored.

Versioning is useful for build artifacts and configuration files, but is
not a complete backup strategy by itself. Combine it with appropriate
retention, access separation, copies/replication where needed, and
tested restores.

## 10. Lifecycle rules and cost optimization

Lifecycle policies can transition objects to other storage classes or
expire eligible objects/versions. Design rules around retention
requirements, not just a desire to reduce the storage price.

  -------------------------------------------------------------------------
  Data type               Example strategy        Caution
  ----------------------- ----------------------- -------------------------
  Temporary uploads       Expire after a defined  Confirm the application
                          short period            no longer needs them

  Application logs        Transition or expire    Preserve
                          according to retention  audit/incident-response
                          policy                  records

  Old build artifacts     Archive after release   Confirm restore-time
                          retention               requirements

  Noncurrent versions     Expire after a defined  This removes recovery
                          retention period        points

  Incomplete multipart    Abort after a suitable  Ensure uploads are not
  uploads                 period                  still active
  -------------------------------------------------------------------------

### Create a rule

1.  Open **Management → Lifecycle rules**.
2.  Create a clearly named rule.
3.  Scope it to a dedicated prefix or tag, such as `tmp/`.
4.  Select transition and/or expiration actions.
5.  Review effects on current objects, noncurrent versions, and delete
    markers.
6.  Save and monitor results.

Lifecycle actions may not happen immediately; check documented timing
and eligibility rules.

Cost checklist: - Select storage classes based on access and restore
needs. - Delete abandoned objects and incomplete multipart uploads. -
Review old versions and delete markers. - Scope lifecycle policies
carefully. - Monitor request, retrieval, transfer, and storage costs. -
Consider Intelligent-Tiering only when the access pattern and economics
justify it. - Check current pricing for your Region. - Never expire
backups or logs before confirming retention requirements.

## 11. AWS CLI hands-on practice

Use AWS CLI v2 with an approved profile. Avoid root credentials,
hard-coded access keys, and secrets in shell history or Git.

``` bash
export AWS_REGION="ap-south-1"
export AWS_PROFILE="your-lab-profile"
export BUCKET="YOUR_UNIQUE_BUCKET_NAME"

aws sts get-caller-identity
```

Change the Region, profile, and bucket name to match your setup.

### List, upload, download, and copy

``` bash
aws s3 ls
aws s3 ls "s3://${BUCKET}/" --recursive

printf 'Hello from the AWS CLI\n' > hello.txt
aws s3 cp hello.txt "s3://${BUCKET}/uploads/hello.txt"
aws s3 cp "s3://${BUCKET}/uploads/hello.txt" downloaded-hello.txt
aws s3 cp "s3://${BUCKET}/uploads/hello.txt" "s3://${BUCKET}/archive/hello.txt"
```

### Sync a static site directory

``` bash
aws s3 sync ./website/ "s3://${BUCKET}/website/"
```

`sync` does not configure website hosting, bucket policy, or CloudFront.
Be cautious with `--delete`: it can remove destination objects that are
not present locally.

### Inspect settings and versions

``` bash
aws s3api get-bucket-versioning --bucket "$BUCKET"
aws s3api get-bucket-encryption --bucket "$BUCKET"
aws s3api get-public-access-block --bucket "$BUCKET"
aws s3api list-object-versions --bucket "$BUCKET" --prefix "uploads/hello.txt"
aws s3api get-bucket-lifecycle-configuration --bucket "$BUCKET"
```

Some commands may fail if a setting has not been configured or your
identity lacks permission. Interpret the error rather than broadening
permissions immediately.

### Remove only a disposable lab prefix

Inspect first:

``` bash
aws s3 ls "s3://${BUCKET}/uploads/" --recursive
```

After confirming the path, remove only the lab objects:

``` bash
aws s3 rm "s3://${BUCKET}/uploads/" --recursive
```

This does not necessarily permanently delete all historical versions in
a versioned bucket. Review versions separately before permanent
deletion.

## 12. Troubleshooting

  -------------------------------------------------------------------------------
  Symptom                 Likely cause            Checks
  ----------------------- ----------------------- -------------------------------
  `AccessDenied` on       Missing `s3:PutObject`, Identity and bucket policies,
  upload                  explicit Deny, wrong    permissions boundary, SCP, KMS
                          ARN, or KMS permissions key policy

  List fails but object   `s3:ListBucket` missing Check action and bucket ARN;
  download works                                  this can be intentional

  Website returns `403`   Public access blocked,  Website endpoint, Block Public
                          missing public-read     Access, bucket policy
                          policy, wrong object    
                          key                     

  Website returns `404`   Index document/key      Confirm `index.html` exists at
                          incorrect               the configured key

  Website works over HTTP Direct S3 website       Use CloudFront and a
  but not HTTPS           endpoint does not serve certificate
                          HTTPS                   

  Version history not     Versioning disabled or  Check versioning and object
  visible                 wrong object key        versions

  Public policy has no    Block Public Access or  Prefer CloudFront/OAC rather
  effect                  organization controls   than weakening broad controls

  CLI uses wrong account  Wrong profile or        Run
                          environment credentials `aws sts get-caller-identity`

  Lifecycle action has    Rule scope, object age, Inspect filters, version
  not occurred            or eligibility mismatch status, and documented timing
  -------------------------------------------------------------------------------

### `AccessDenied` debugging order

1.  Confirm identity: `aws sts get-caller-identity`.
2.  Verify bucket, Region, key, and resource ARN.
3.  Identify the exact failed API action.
4.  Review identity policy and bucket policy.
5.  Check explicit Deny, permissions boundaries, session policies, and
    SCPs.
6.  If SSE-KMS is used, review KMS permissions and key policy.
7.  Review CloudTrail for the failed API event if logging is enabled.
8.  Add only the permission required for the intended operation.

## 13. Security best practices

-   Keep Block Public Access enabled by default.
-   Prefer bucket owner enforced Object Ownership; avoid ACLs unless
    required.
-   Apply least-privilege IAM and bucket policies.
-   Deny insecure transport where appropriate.
-   Enable versioning for important objects if it supports the recovery
    model.
-   Consider S3 Object Lock for WORM-style retention, but understand
    governance/compliance modes before enabling it.
-   Use encryption at rest and HTTPS in transit.
-   Use SSE-KMS when customer-managed key control or audit needs justify
    it; plan for permissions and cost.
-   Enable CloudTrail data events when object-level API visibility is
    required; these may incur charges.
-   Separate environments/data classifications with buckets or accounts.
-   Never expose backups, logs, deployment artifacts, or configuration
    files through a public policy.
-   Do not store credentials in objects unless using an approved secrets
    design.

## 14. Lab assignments

### Beginner

1.  Create a private bucket with encryption enabled.
2.  Upload, download, copy, and list a test object using console and
    CLI.
3.  Explain bucket, key, and prefix.
4.  Compare S3 with EBS.
5.  Inspect public-access-block and encryption settings.

### Intermediate

1.  Enable versioning and recover from an overwrite.
2.  Write a least-privilege policy allowing a role to read only
    `reports/*`.
3.  Create a lifecycle rule scoped to a disposable `tmp/` prefix.
4.  Host a static website in a dedicated lab bucket, document the risks,
    then remove public access.
5.  Explain why CloudFront/OAC is preferred for HTTPS production
    hosting.

### Advanced

1.  Deploy a static site using a private bucket and CloudFront OAC.
2.  Add a secure-transport Deny and validate it.
3.  Design lifecycle rules for current and noncurrent versions under a
    retention policy.
4.  Enable suitable audit visibility and explain data-event costs.
5.  Design a backup strategy with versioning, separate-account copies or
    replication where justified, and restore tests.
6.  Write a threat model for accidental public exposure and compromised
    credentials.

## 15. Interview questions

**1. What is Amazon S3?**\
A managed object-storage service for storing and retrieving data through
APIs at scale.

**2. What is an S3 bucket?**\
A container for objects, with a name unique within the AWS partition.

**3. What is an object key?**\
The name identifying an object within a bucket. Prefixes such as
`logs/2026/` help organize keys.

**4. What does 11 nines durability mean?**\
S3 Standard is designed for 99.999999999% annual durability. It is not
the same as availability or protection from application-level deletion.

**5. Difference between durability and availability?**\
Durability concerns retaining data; availability concerns being able to
access it.

**6. Difference between IAM and bucket policies?**\
IAM policies are identity-based; bucket policies are resource-based.

**7. Does a bucket policy Deny always override an Allow?**\
An applicable explicit Deny takes precedence. Omitting an Allow from a
bucket policy does not automatically deny permissions granted by other
applicable policies.

**8. What is Block Public Access?**\
Controls at account, bucket, and access-point levels that help prevent
public exposure.

**9. What is S3 Versioning?**\
It preserves multiple versions of an object key and can help recover
from overwrites or deletes.

**10. Is versioning a complete backup?**\
No. Pair it with retention, access separation, copies/replication when
required, and restore testing.

**11. What is a lifecycle policy?**\
A rule that transitions or expires eligible objects or versions
according to age and filters.

**12. Can S3 host a dynamic backend?**\
No. S3 serves static objects; dynamic application code needs compute or
application services.

**13. Can a direct S3 website endpoint serve HTTPS?**\
No. Use CloudFront with a certificate for HTTPS.

**14. How can a public website use a private S3 bucket?**\
Use CloudFront with Origin Access Control to grant CloudFront access to
the origin.

**15. Why can `GetObject` work while `ListBucket` fails?**\
They are different permissions on different resource ARNs.

**16. How can S3 costs be reduced?**\
Choose suitable classes, use carefully scoped lifecycle rules, manage
old versions and incomplete multipart uploads, and monitor request,
retrieval, transfer, and storage charges.

## 16. Official references

-   [Amazon S3 User
    Guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html)
-   [S3 security best
    practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html)
-   [Block Public
    Access](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html)
-   [Bucket
    policies](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-policies.html)
-   [Using HTTPS with
    S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingHTTPS.html)
-   [Hosting a static website on
    S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteHosting.html)
-   [CloudFront with an S3
    origin](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/GettingStarted.SimpleDistribution.html)
-   [S3
    Versioning](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html)
-   [S3 lifecycle
    management](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html)
-   [S3 storage classes](https://aws.amazon.com/s3/storage-classes/)
-   [Amazon S3 pricing](https://aws.amazon.com/s3/pricing/)

## Key takeaway

S3 is more than file storage. DevOps engineers need to choose
appropriate storage classes, apply least-privilege access, understand
explicit Deny and Block Public Access, recover objects with versioning,
automate retention with lifecycle rules, and account for cost and
security consequences. For public static websites, prefer a private S3
bucket behind CloudFront with HTTPS instead of exposing the bucket
directly.
