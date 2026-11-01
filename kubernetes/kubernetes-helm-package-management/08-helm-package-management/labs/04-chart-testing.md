# Lab 04 — Test and Validate a Chart

```bash
helm lint charts/platform-web
helm template test charts/platform-web -n helm-lab --debug > rendered.yaml
kubectl apply --dry-run=server -f rendered.yaml
```

If the API server reports an unsupported API version or invalid field, update the chart for the target cluster version. Server-side dry-run requires API access.

Package:
```bash
helm package charts/platform-web --destination dist/
```

Optional: configure a chart test Job annotated with `helm.sh/hook: test`, install the chart, and run `helm test <release> -n <namespace>`.
