# 12 — Storage Troubleshooting

## First response
```bash
kubectl get pvc -A
kubectl get pv
kubectl get pods -A -o wide
kubectl get events -A --sort-by=.lastTimestamp
kubectl describe pvc -n <namespace> <claim>
kubectl describe pod -n <namespace> <pod>
```

## PVC Pending
Check missing/default StorageClass, incorrect/unavailable provisioner, unsupported size or access mode, quota/backend capacity, `WaitForFirstConsumer`, and topology constraints.

## Pod stuck in ContainerCreating
Look for FailedMount/FailedAttachVolume and permission, filesystem, or node-plugin errors. Inspect:
```bash
kubectl get volumeattachment
kubectl get csidrivers
kubectl describe pod <pod>
```

## Multi-Attach
A single-node-attached volume may still be attached to another node. Confirm old Pod termination, node health, VolumeAttachment state, and driver behavior. Do not force-detach without provider/driver guidance; data corruption is possible.

## Permission denied
Check UID/GID, ownership, fsGroup/CSI support, mount flags, and filesystem permissions. Avoid blindly applying recursive chmod.

## CSI logs
```bash
kubectl get pods -A | grep -i csi
kubectl logs -n <driver-namespace> <driver-pod> -c <container> --since=30m
```
Capture timestamps, PVC/PV, StorageClass, events, VolumeAttachment, driver logs, node, backend volume ID, and recent changes. Redact secrets before sharing.
