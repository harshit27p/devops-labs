# 02 — Scheduler Architecture and Scheduling Cycle

The kube-scheduler watches for Pods that have no assigned node, evaluates feasible nodes, scores candidates, and binds the Pod to a selected node.

## Scheduling cycle
1. **Queueing:** Pod enters scheduler queues.
2. **PreFilter:** plugins prepare state and may reject the Pod.
3. **Filter:** eliminate nodes that cannot run it.
4. **PostFilter:** may attempt preemption if no node is feasible.
5. **PreScore/Score:** rank feasible nodes.
6. **Reserve/Permit:** plugins may reserve resources or delay binding.
7. **PreBind/Bind/PostBind:** prepare and bind the Pod.

The exact plugin sequence depends on Kubernetes version and scheduler profile.

## Filter vs score
- Filter is a feasibility decision: can this Pod run on the node?
- Score is a preference: which feasible node is better?

## Scheduler profiles
A cluster can configure profiles and plugin weights. Custom scheduler names can be selected through `spec.schedulerName`, but the named scheduler must exist and be configured.

## Observe
```bash
kubectl get events -A --sort-by=.lastTimestamp
kubectl describe pod <pod>
kubectl get pods -n kube-system | grep scheduler
```
Managed control planes may not expose scheduler Pods or logs. Use provider diagnostics where appropriate.
