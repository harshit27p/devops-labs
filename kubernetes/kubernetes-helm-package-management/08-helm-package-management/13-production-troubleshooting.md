# 13 — Production Patterns and Troubleshooting

## Chart design
- Keep charts small and focused.
- Use stable labels and helper templates.
- Expose meaningful configuration, not every manifest field.
- Set resource requests/limits and secure Pod defaults.
- Use readiness/liveness/startup probes where appropriate.
- Make optional resources explicit.
- Document values and breaking changes.

## Common failures
**Release name already exists:** inspect `helm list -A` and the release namespace; do not delete release metadata blindly.

**Pending/failed release:** inspect `helm status`, history, rendered manifests, events, and workload readiness.

**Template parse error:** run `helm lint` and `helm template --debug`; check indentation, quoting, scope, and whitespace trimming.

**Resource already exists / ownership conflict:** inspect the live object and its labels/annotations; understand ownership before adopting or deleting it.

**Upgrade timeout:** inspect Pod scheduling, image pulls, probes, PVCs, hooks, and controller events. A Helm timeout does not identify the root cause.

**Rollback did not restore application:** database migrations or external side effects may not be reversible by Helm.

## Production checklist
- [ ] Chart and dependency versions pinned.
- [ ] Values schema and documentation maintained.
- [ ] Rendered manifests reviewed.
- [ ] RBAC and namespace scope least-privileged.
- [ ] Images pinned and scanned.
- [ ] Secrets handled externally or securely.
- [ ] Upgrade, rollback, and migration plan tested.
- [ ] Hooks idempotent and bounded.
- [ ] Observability and alerts configured.
- [ ] Chart artifact provenance recorded.
