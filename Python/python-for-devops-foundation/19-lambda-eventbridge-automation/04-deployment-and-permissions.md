# Lambda Deployment and Permissions

## Deployment checklist
- Correct runtime and architecture.
- Dependency packaging or supported deployment artifact.
- Environment configuration.
- Execution role with minimum permissions.
- Timeout and memory settings.
- VPC access only when required.
- CloudWatch logging permissions.
- Deployment version and rollback strategy.

## IAM separation
The Lambda execution role is not the same as the permission allowing EventBridge to invoke the function. Configure both sides according to the chosen integration.

## Safe rollout
Deploy to a test alias or environment first, run a test event, verify logs/metrics, then shift production traffic. Keep the previous version available for rollback.

Exercises: create a deployment checklist and document the minimum permissions for a read-only inventory Lambda.
