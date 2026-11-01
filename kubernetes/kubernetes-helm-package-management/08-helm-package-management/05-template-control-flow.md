# 05 — Template Control Flow and Named Templates

## Control structures
- `if` / `else`: conditional resource sections.
- `with`: change the current context.
- `range`: iterate over lists/maps.
- `define`: declare a named template.
- `include`: render a named template and allow piping/formatting.

## Named helper
```gotemplate
{{- define "platform-web.fullname" -}}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
```

Use:
```yaml
metadata:
  name: {{ include "platform-web.fullname" . }}
```

## Context and scope
Inside `range` and `with`, dot (`.`) changes. Use `$` to access the root context. Pass context explicitly to helpers to avoid hidden assumptions.

## YAML safety
Use `toYaml` and `nindent` for nested structures:
```gotemplate
resources:
  {{- toYaml .Values.resources | nindent 2 }}
```
Validate indentation and types using `helm template` and a YAML/Kubernetes schema validator.

## Avoid
- Complex business logic in templates.
- Unbounded dynamic resource generation.
- Generating secrets in templates without a secure design.
- Unstable names that cause needless replacement.
