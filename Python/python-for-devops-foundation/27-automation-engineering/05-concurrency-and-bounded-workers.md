# Concurrency and Bounded Workers

Concurrency can improve throughput when tasks spend time waiting on I/O. It can also overload dependencies.

## Python options
- `threading` and `ThreadPoolExecutor` for I/O-bound work.
- `multiprocessing` and `ProcessPoolExecutor` for CPU-bound work.
- `asyncio` for many concurrent asynchronous I/O operations.

## Safe design
- Set a maximum worker count.
- Apply per-service rate limits.
- Use connection and request timeouts.
- Bound queues to avoid unbounded memory growth.
- Collect exceptions from every task.
- Avoid sharing mutable state without synchronization.

## Exercise
Use `ThreadPoolExecutor(max_workers=4)` to check a list of local sample files. Record success/failure for each file and ensure one failure does not hide other results.
