# GitHub-to-Ticket Workflow

1. GitHub sends an `issue_comment` webhook.
2. Receiver validates the signature.
3. Receiver checks event action, repository, issue type and command.
4. Ticket client creates a ticket.
5. Event ID and outcome are persisted.

Use an explicit command such as `/jira`; do not create tickets for every comment. Restrict allowed repositories and, where required, authorized users.

Providers may retry deliveries. Persist a stable delivery ID and make processing idempotent. An in-memory set is insufficient across restarts or multiple instances.

Exercises: write a pure event-filter function, test ignored events and design persistent duplicate prevention.
