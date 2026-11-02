# Interactive Debugging with pdb

`pdb` allows step-by-step inspection of Python execution.

```bash
python -m pdb app.py
```

Useful commands:
- `n` — next line
- `s` — step into a function
- `c` — continue
- `l` — list source
- `p expression` — print an expression
- `where` — show stack
- `q` — quit

Use breakpoints near the failing operation. Avoid printing secrets or production user data while debugging.
