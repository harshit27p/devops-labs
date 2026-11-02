# Coverage and Profiling

Coverage indicates which code paths tests execute; it does not prove correctness or security.

```bash
python -m pip install pytest coverage
coverage run -m pytest
coverage report -m
```

Profile only after identifying a performance question:

```bash
python -m cProfile -s cumulative script.py
```

Prioritize correctness, clear error handling and security controls before micro-optimization. Add tests for failure paths, not just successful execution.
