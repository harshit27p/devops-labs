# 06 — Injecting Secrets into Containers

## Individual Secret key

```yaml
env:
  - name: DB_PASSWORD
    valueFrom:
      secretKeyRef:
        name: app-credentials
        key: password
```

## Bulk import

```yaml
envFrom:
  - secretRef:
      name: app-credentials
```

Bulk import is convenient but can inject more values than the application needs. Prefer explicit key references for sensitive workloads.

## Mount as files

```yaml
volumes:
  - name: credentials
    secret:
      secretName: app-credentials
      defaultMode: 0400
containers:
  - name: app
    volumeMounts:
      - name: credentials
        mountPath: /var/run/app-secrets
        readOnly: true
```

Applications can read the credential from a file without placing it in the process environment.

## Environment vs volume

| Consideration | Environment variable | Secret volume |
|---|---|---|
| Update existing process | No; restart required | Projected file can update eventually |
| App reload required | Restart Pod | App must reread/reload |
| Accidental exposure | May appear in dumps/diagnostics | File permissions and mount access matter |
| Application compatibility | Many apps support env | Apps must read files |

Neither method protects data from a compromised process that is authorized to access it.

## Optional references

Set `optional: true` only when absence is safe and explicitly handled. Missing required credentials should generally prevent the application from starting successfully.

## Reference

- [Using Secrets](https://kubernetes.io/docs/concepts/configuration/secret/#using-secrets)
