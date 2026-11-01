# 02 — Chart Structure and Metadata

A chart is a directory with a `Chart.yaml` file and optional templates, values, dependencies, and supporting files.

```text
platform-web/
├── Chart.yaml
├── values.yaml
├── values.schema.json
├── templates/
│   ├── _helpers.tpl
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   ├── serviceaccount.yaml
│   └── NOTES.txt
└── charts/
```

## Chart.yaml
Important fields include `apiVersion`, `name`, `description`, `type`, `version`, `appVersion`, `kubeVersion`, and maintainers/sources. `version` is the chart package version; `appVersion` describes the application version and is informational unless templates use it.

## Chart types
- `application`: deployable chart (default).
- `library`: reusable named templates; not installed as a standalone application.

## Package
```bash
helm lint charts/platform-web
helm package charts/platform-web --destination dist/
helm show chart dist/platform-web-0.1.0.tgz
helm show values dist/platform-web-0.1.0.tgz
```

## Naming and labels
Use stable names and standard labels such as `app.kubernetes.io/name`, `app.kubernetes.io/instance`, `app.kubernetes.io/version`, `app.kubernetes.io/managed-by`, and `helm.sh/chart`. Helpers centralize naming and labels.
