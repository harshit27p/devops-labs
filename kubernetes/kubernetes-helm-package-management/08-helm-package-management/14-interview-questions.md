# 14 — Helm Interview Questions

1. What problem does Helm solve?
2. Explain Chart, Release, Revision, and Repository.
3. What is the role of Chart.yaml and values.yaml?
4. Difference between chart version and appVersion?
5. How are values merged and overridden?
6. What is values.schema.json?
7. Explain Go template `include`, `define`, `range`, and `with`.
8. Why use `_helpers.tpl`?
9. Explain `helm install` vs `helm upgrade --install`.
10. How does Helm rollback work, and what can it not reverse?
11. What are chart dependencies and Chart.lock?
12. What is a library chart?
13. Explain Helm hooks and hook deletion policies.
14. How do you lint and test a chart?
15. How does Helm support OCI registries?
16. Where is Helm release state stored?
17. Why can secrets in Helm values be exposed?
18. How do Helm and GitOps controllers work together?
19. How would you troubleshoot a failed Helm upgrade?
20. How do you design a reusable chart for multiple environments?

## Scenario prompts
- A chart installs successfully but Pods remain Pending. How do you debug?
- A Helm upgrade times out after a database migration. What recovery plan is needed?
- A resource already exists and Helm refuses ownership. What do you inspect?
- A value override is ignored. How do you inspect the final merged values and rendered output?
- How do you promote exactly the same artifact from staging to production?

Strong answers distinguish Helm release management from Kubernetes runtime reconciliation and call out external side effects.
