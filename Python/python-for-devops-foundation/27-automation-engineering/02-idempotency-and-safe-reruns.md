# Idempotency and Safe Reruns

An operation is idempotent when repeating it with the same intended input does not create additional unintended effects.

## Examples
- Ensure a directory exists: naturally idempotent.
- Set a configuration value to a desired state: can be idempotent.
- Append the same line on every run: not idempotent unless checked.
- Create a new cloud resource every run: usually not idempotent.

## Patterns
- Use stable resource identifiers.
- Check current state before acting.
- Prefer “ensure desired state” over blind imperative changes.
- Store operation IDs for event-driven workflows.
- Make retries safe and detect duplicate requests.

## Exercise
Write a script that ensures a directory and a marker file exist without duplicating marker content. Test it by running it repeatedly.
