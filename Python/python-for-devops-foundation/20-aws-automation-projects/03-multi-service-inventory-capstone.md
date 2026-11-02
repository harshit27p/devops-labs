# Capstone — Multi-Service AWS Inventory and Safe Cleanup Toolkit

## Objective
Build a Python CLI that inventories selected AWS resources and proposes safe cleanup candidates without making changes by default.

## Required modules
1. Identity verification using STS.
2. EC2 instance inventory.
3. EBS volume and snapshot inventory.
4. S3 bucket configuration inventory.
5. IAM role/policy metadata review.
6. JSON and CSV reporting.
7. Cleanup policy evaluation.
8. Dry-run and explicit approval execution boundary.

## Suggested outputs
- `account-summary.json`
- `ec2-inventory.csv`
- `ebs-volumes.csv`
- `ebs-snapshots.csv`
- `s3-security-report.csv`
- `cleanup-plan.json`

## Acceptance criteria
- Refuses to run if account or region is not allowlisted.
- Uses paginators for supported collection APIs.
- Handles AccessDenied as unknown/unavailable, not as a secure setting.
- Produces complete reports with timestamps and scan scope.
- Cleanup plan includes reasons and exclusion checks.
- Dry-run never calls stop, terminate, detach or delete APIs.
- Execute mode revalidates each target and requires approval.
- Logs contain resource IDs and outcomes, never credentials.

## Stretch goals
- Store reports in encrypted S3.
- Schedule read-only inventory with Lambda/EventBridge.
- Send summary notifications.
- Add unit tests with mocks/Moto and sandbox integration tests.
