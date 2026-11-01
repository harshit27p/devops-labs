# Lab 03 — Backup and Restore an Application Namespace

## Objective

Practice a recovery workflow using a backup tool supported by your environment.

## Prerequisites

A disposable cluster, a test namespace, a supported backup tool (for example Velero), configured object storage, and a backup method for persistent data. Installation and provider plugin setup are environment-specific.

## Create test workload

```bash
kubectl create namespace recovery-lab
kubectl create deployment web --image=nginx:1.27 -n recovery-lab
kubectl expose deployment web --port=80 -n recovery-lab
kubectl get all,pvc -n recovery-lab
```

For real data recovery practice, add a test PVC and a test application that writes known data. Ensure your backup configuration captures PV data; namespace objects alone do not prove volume recovery.

## Backup and inspect

```bash
velero backup create recovery-lab-backup   --include-namespaces recovery-lab --wait
velero backup describe recovery-lab-backup
velero backup logs recovery-lab-backup
```

## Restore

Use a separate test namespace or isolated cluster and follow the backup tool's supported namespace mapping procedure. Validate object restoration, volume data, application startup, and a known test record.

## Record

Measure actual recovery time, identify missing dependencies, and compare observed data loss with the intended RPO. Clean up only after evidence has been captured.
