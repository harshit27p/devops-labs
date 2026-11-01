# 07 — Grafana Dashboards and Provisioning

## Grafana role

Grafana visualizes metrics and other telemetry sources. It is not itself a metrics collector or long-term metrics database. A dashboard should answer a small set of operational questions and provide useful drill-downs.

## Dashboard design

A practical service dashboard often includes:

1. Request rate.
2. Error rate and error ratio.
3. Latency percentiles from histogram metrics.
4. Saturation: CPU throttling, memory pressure, queue depth, connection pools.
5. Availability: ready replicas, failed probes, restart trends.
6. Dependency health and recent deployment annotations.

A cluster dashboard may include node readiness, CPU/memory, filesystem capacity, Pod pressure, API server health, and workload availability.

## Dashboard variables

Use variables such as `$namespace`, `$service`, and `$cluster` to make dashboards reusable. Avoid variables that expand to enormous high-cardinality result sets.

## Provisioning

Dashboards and data sources can be provisioned from files or managed through GitOps. Treat dashboards as code, review changes, and keep credentials outside source control.

A minimal data source provisioning example:

```yaml
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus-operated.monitoring.svc:9090
    isDefault: true
    editable: false
```

The URL above is an example; confirm the Service name in your installation.

## Dashboard ConfigMap

`../manifests/grafana-dashboard-configmap.yaml` shows a small dashboard JSON stored in a ConfigMap. Grafana must be configured with a dashboard provider that watches the relevant directory or ConfigMap integration. Merely creating the ConfigMap does not guarantee Grafana imports it.

## Access and security

- Use authentication and least-privilege roles.
- Avoid anonymous admin access.
- Do not store data source passwords in dashboard JSON.
- Restrict network access to Grafana.
- Keep plugins reviewed and updated.
- Avoid public dashboards that reveal internal hostnames, namespaces, or service topology.

## Further reading

- https://grafana.com/docs/grafana/latest/
- https://grafana.com/docs/grafana/latest/administration/provisioning/
