# Credential and Access Hygiene

- Prefer temporary credentials and role assumption.
- Rotate or revoke exposed credentials immediately.
- Remove unused access only after confirming ownership and dependency.
- Review last-used information as one signal, not absolute proof.
- Enable MFA for human access where appropriate.
- Audit access key age and usage.
- Avoid logging tokens or secret values.
- Use CloudTrail and relevant security services for audit evidence.

Do not build scripts that silently disable users or delete keys. Generate review reports and require an owner-approved remediation workflow.

Exercises: produce a credential-age report and write a remediation checklist with rollback considerations.
