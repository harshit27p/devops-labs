# 09 — Testing, Linting, and Debugging

## Static checks
```bash
helm lint ./charts/platform-web
helm template test ./charts/platform-web --debug
helm show values ./charts/platform-web
```

## API validation
Render then validate against the target cluster:
```bash
helm template test ./charts/platform-web -n demo > rendered.yaml
kubectl apply --dry-run=server -f rendered.yaml
```
Server-side dry-run requires API access and may not fully model controller/runtime behavior.

## Release checks
```bash
helm status <release> -n <namespace>
helm get manifest <release> -n <namespace>
kubectl get events -n <namespace> --sort-by=.lastTimestamp
kubectl describe deployment -n <namespace> <deployment>
```

## Test hooks
Helm chart tests are Pods/Jobs annotated with `helm.sh/hook: test`. Run:
```bash
helm test <release> -n <namespace>
```

## CI recommendations
- Lint charts.
- Render with representative values files.
- Validate schemas and Kubernetes API compatibility.
- Scan images and dependencies.
- Run policy checks.
- Test install/upgrade/rollback in ephemeral clusters.
- Publish only reviewed, versioned artifacts.
