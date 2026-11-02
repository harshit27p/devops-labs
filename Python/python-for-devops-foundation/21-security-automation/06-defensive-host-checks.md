# Defensive Host Checks

A host-check script should collect the minimum information needed for an approved purpose and avoid making changes.

## Example checks
- OS and Python runtime version
- Selected configuration file ownership and mode
- Disk capacity and filesystem usage
- Package inventory from the platform package manager
- Service state through approved system interfaces

## Design rules
1. Document exactly what is collected.
2. Avoid reading credential stores, browser profiles or private user files.
3. Handle permission errors without escalating privileges automatically.
4. Mark unsupported checks as `not_supported`, not `passed`.
5. Write machine-readable JSON and a human-readable summary.
6. Include collection timestamp and tool version.

## Exercise
Implement three read-only checks and emit a JSON object with `check`, `status`, `evidence` and `timestamp` fields.
