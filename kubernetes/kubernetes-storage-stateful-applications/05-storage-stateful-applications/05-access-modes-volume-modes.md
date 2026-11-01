# 05 — Access Modes and Volume Modes

| Access mode | Meaning |
|---|---|
| RWO | Read-write mount from a single node; multiple Pods on that node may use it |
| ROX | Read-only mount from many nodes |
| RWX | Read-write mount from many nodes |
| RWOP | Read-write mount by one Pod; CSI and version support required |

RWO does **not** mean one Pod. It means read-write attachment to one node. Access modes do not provide application-level locking or safe concurrent-write semantics; backend and driver capabilities matter.

## Volume modes
- `Filesystem` (default): volume is formatted/mounted as a filesystem.
- `Block`: raw block device is exposed; the application must handle block I/O and data layout.

Choose RWX only when the backend supports it and the application is safe for shared filesystem access. RWOP can enforce single-Pod mounting where supported. Validate driver capabilities before designing around a mode.
