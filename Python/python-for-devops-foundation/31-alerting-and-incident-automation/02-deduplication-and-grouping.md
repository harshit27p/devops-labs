# Deduplication and Grouping

A single incident can generate many similar events. Deduplication reduces noise while preserving evidence.

## Grouping keys
Use stable fields such as service, environment, alert rule and affected dependency. Avoid grouping unrelated incidents solely because they share a broad message.

## Event lifecycle
- New
- Acknowledged
- Firing
- Resolved
- Reopened

Retain occurrence counts and first/last-seen timestamps. Do not discard repeat events; attach them to the incident group.
