# Add this foundation to devops-labs

1. Download and extract this ZIP.
2. Copy the included `python/` directory into the root of your existing `devops-labs` clone.
3. Review the links in `python/01-course-roadmap/video-resources.md`.
4. Commit and push the new folder.

Example from the root of your local repository:

```bash
# After extracting the ZIP somewhere accessible:
cp -r /path/to/extracted/python ./python

git add python/
git commit -m "Add Python for DevOps documentation foundation"
git push
```

On Windows PowerShell, use `Copy-Item -Recurse` instead of `cp` if preferred.
