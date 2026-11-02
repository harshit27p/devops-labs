# Safe Resource Cleanup Framework

## Separate plan from execution
A cleanup system should produce a reviewable plan before it performs changes.

Each candidate record should contain:
- Resource type and ID.
- Account and region.
- Owner and environment tags.
- Age and observed state.
- Policy rule evaluated.
- Exclusion/retention checks.
- Proposed action and reason.
- Approval identity and timestamp.

## Two-phase pattern
1. `plan`: read-only discovery, candidate scoring and JSON/CSV output.
2. `execute`: reload the plan, re-fetch resources, revalidate every guard and perform only approved actions.

Do not trust a stale plan without rechecking the live resource. Protect against time-of-check/time-of-use changes.

## Required guardrails
- Dry-run default.
- Account/region allowlist.
- Explicit resource IDs or narrow tag selection.
- Protected tags and exclusion lists.
- Retention and backup checks.
- Maximum action count.
- Explicit approval and audit log.
- Stop on unexpected API responses.

Exercises: implement a plan-only mode and prove through tests that delete APIs are never called in dry-run.
