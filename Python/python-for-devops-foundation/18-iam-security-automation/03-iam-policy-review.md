# IAM Policy Review Automation

A policy linter should flag suspicious patterns for human review, not automatically rewrite or delete permissions.

Review signals:
- `Action: "*"` or `Resource: "*"` where unnecessary.
- Wildcard permissions for sensitive services.
- Unrestricted role assumption.
- Missing conditions.
- Unexpected principals in resource policies.
- Stale policies or unused access, subject to evidence and owner review.

Example simple detector:
```python
def find_wildcards(policy):
    findings = []
    for statement in policy.get("Statement", []):
        actions = statement.get("Action", [])
        resources = statement.get("Resource", [])
        if isinstance(actions, str):
            actions = [actions]
        if isinstance(resources, str):
            resources = [resources]
        if "*" in actions or "*" in resources:
            findings.append({
                "sid": statement.get("Sid", ""),
                "effect": statement.get("Effect", ""),
                "reason": "wildcard action or resource requires review",
            })
    return findings
```

This is a basic indicator, not a full IAM policy evaluator. Use AWS IAM Access Analyzer and policy validation tools for deeper analysis.

Exercises: parse sample policies, flag wildcards and distinguish findings from confirmed vulnerabilities.
