# Lab 01 — Install Helm and Inspect a Chart

Install Helm using the official installation guide for your operating system:
https://helm.sh/docs/intro/install/

Verify:
```bash
helm version
helm env
helm repo list
```

Inspect the sample chart:
```bash
helm show chart charts/platform-web
helm show values charts/platform-web
helm lint charts/platform-web
helm template demo charts/platform-web --namespace demo
```

Review the rendered YAML before installing. Confirm image, ports, Service type, resources, security context, and optional Ingress settings.
