# State, Checkpoints and Recovery

Long-running jobs need a way to resume without repeating completed work or losing track of partial failure.

## Checkpoint design
- Store a stable job/run identifier.
- Record completed units of work.
- Persist only the minimum state needed to resume.
- Make checkpoint updates atomic.
- Version the checkpoint schema.
- Validate checkpoint ownership and integrity before resuming.

## Recovery questions
- Can a job safely restart from the beginning?
- What happens if it crashes after an external action but before saving state?
- Can duplicate processing be detected?
- Is manual recovery documented?

For distributed workflows, use a durable database or workflow engine rather than a fragile local text file.
