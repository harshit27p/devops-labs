# Plugin Trust and Permissions

A plugin running in the same Python process generally has the same operating-system privileges as the host. An interface or abstract base class does not sandbox it.

## Controls
- Install only reviewed and pinned plugins.
- Separate plugin execution into a restricted process/container when stronger isolation is required.
- Apply OS-level least privilege and filesystem/network restrictions.
- Set CPU, memory and execution-time limits.
- Sign or otherwise verify release artifacts where appropriate.
- Audit plugin actions and dependencies.
- Provide disable/rollback controls.

Do not describe Python imports, virtual environments or interfaces as security sandboxes.
