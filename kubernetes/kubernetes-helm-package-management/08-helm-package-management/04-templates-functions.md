# 04 — Go Templates and Functions

Helm templates use Go's text/template engine plus Sprig and Helm-specific functions.

## Common expressions
- `{{ .Values.replicaCount }}` — read a value.
- `{{ .Release.Name }}` — release name.
- `{{ .Release.Namespace }}` — target namespace.
- `{{ .Chart.Name }}` — chart name.
- `{{ include "name" . }}` — render a named template.
- `{{ required "message" .Values.foo }}` — require a value.
- `{{ default "value" .Values.foo }}` — use a default.
- `{{ quote .Values.foo }}` — quote a string.

## Whitespace
`{{-` and `-}}` trim whitespace. Incorrect trimming can merge YAML lines or create invalid manifests. Prefer readable templates and validate rendered output.

## Example
```yaml
replicas: {{ .Values.replicaCount }}
image: {{ printf "%s:%s" .Values.image.repository .Values.image.tag | quote }}
```

## Debug
```bash
helm template demo ./charts/platform-web --debug
helm lint ./charts/platform-web
```

Templates generate YAML; they do not guarantee that the Kubernetes API accepts it. Always render and validate against the target cluster's API versions.
