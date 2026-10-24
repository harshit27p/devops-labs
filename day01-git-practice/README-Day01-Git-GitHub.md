# Day 01 — DevOps Principles, Git & GitHub

**Course:** PGCP-ITISS — DevOps  
**Environment:** Windows 10/11, Git for Windows, Git Bash  
**Level:** Beginner to Intermediate  
**Lab duration in the supplied guide:** 4 hours

This README consolidates the supplied Day 01 Lab Guide, Session 1, Session 2, and GitFlow branching reference. It covers DevOps fundamentals, Git architecture, Windows setup, SSH authentication, repository lifecycle, `.gitignore`, branching and merges, conflict resolution, GitHub remotes, the capstone scaffold, and the GitFlow release strategy.

> **Important:** Run the lab commands in **Git Bash** unless explicitly stated otherwise. Replace example names, emails, and GitHub usernames with your own values. Never commit private SSH keys, tokens, passwords, or real `.env` credentials.

---

## Table of Contents

1. [Learning Objectives](#learning-objectives)
2. [DevOps Fundamentals](#devops-fundamentals)
3. [Git and Version Control Concepts](#git-and-version-control-concepts)
4. [Install and Configure Git on Windows](#install-and-configure-git-on-windows)
5. [Set Up SSH Authentication with GitHub](#set-up-ssh-authentication-with-github)
6. [Lab 1 — Create a Local Repository](#lab-1--create-a-local-repository)
7. [Lab 2 — Stage, Commit, Diff, and Inspect History](#lab-2--stage-commit-diff-and-inspect-history)
8. [Lab 3 — Create a Windows-Friendly `.gitignore`](#lab-3--create-a-windows-friendly-gitignore)
9. [Lab 4 — Branching and Fast-Forward Merge](#lab-4--branching-and-fast-forward-merge)
10. [Lab 5 — Create and Resolve a Merge Conflict](#lab-5--create-and-resolve-a-merge-conflict)
11. [Lab 6 — Publish the Repository to GitHub](#lab-6--publish-the-repository-to-github)
12. [Lab 7 — Scaffold the DevOps Capstone Project](#lab-7--scaffold-the-devops-capstone-project)
13. [GitHub Collaboration and Remote Workflows](#github-collaboration-and-remote-workflows)
14. [GitFlow Branching Strategy](#gitflow-branching-strategy)
15. [Essential Git Command Cheat Sheet](#essential-git-command-cheat-sheet)
16. [Windows Troubleshooting](#windows-troubleshooting)
17. [Security and Good Practices](#security-and-good-practices)
18. [Self-Assessment Checklist](#self-assessment-checklist)
19. [Review Questions](#review-questions)

---

## Learning Objectives

By the end of Day 01, you should be able to:

- Explain the DevOps culture, lifecycle, and CI/CD concepts.
- Distinguish Git from GitHub and centralized from distributed version control.
- Describe Git's working directory, staging area, and local repository.
- Configure Git on Windows and understand line-ending conversion.
- Generate an ED25519 SSH key pair and authenticate to GitHub.
- Initialize a repository, stage files, commit changes, inspect diffs, and read history.
- Exclude Windows system files, logs, build artifacts, and sensitive files with `.gitignore`.
- Create branches, merge feature work, and resolve merge conflicts.
- Connect a local repository to GitHub and push/pull changes.
- Scaffold the baseline application for later Docker and DevOps modules.
- Explain GitFlow's `main`, `develop`, `feature/*`, `release/*`, and `hotfix/*` branches.

---

## DevOps Fundamentals

### The “Wall of Confusion”

The supplied Session 1 describes a traditional separation between:

- **Development (Dev):** Focuses on features, rapid innovation, and frequent code releases.
- **Operations (Ops):** Focuses on stability, uptime, and production reliability.

This can create a “Wall of Confusion”: code works on a developer's machine but fails in production because of differences in environments, dependencies, or configuration. Manual handoffs and blame make releases slow and risky.

**DevOps** combines cultural practices and tools to improve collaboration and deliver applications and services more reliably and frequently.

### Three pillars described in the session

1. **Culture:** Shared responsibility, transparency, and blameless collaboration.
2. **Practices:** Small and frequent releases, infrastructure as code, automated testing, and feedback loops.
3. **Tools:** Toolchains such as Git, Docker, Jenkins, Kubernetes, Ansible, Terraform, and Prometheus.

### DevOps lifecycle

The session presents a continuous lifecycle:

| Phase | Purpose | Example tools named in the session |
|---|---|---|
| Plan | Define requirements and work | Jira, GitHub Projects, Trello |
| Code | Author and version source code | Git, GitHub, GitLab |
| Build | Compile/package code and images | Maven, Gradle, Docker |
| Test | Run automated tests and scans | JUnit, SonarQube, Selenium |
| Release | Validate and prepare releases | Jenkins, GitHub Actions |
| Deploy | Provision and deploy | Terraform, Kubernetes, AWS |
| Operate | Maintain, scale, and patch systems | Ansible, Linux, Docker Swarm |
| Monitor | Observe health, metrics, logs, alerts | Prometheus, Grafana, ELK |

### CI, Continuous Delivery, and Continuous Deployment

- **Continuous Integration (CI):** Developers integrate changes frequently; commits trigger automated build and test workflows.
- **Continuous Delivery:** The pipeline builds, tests, and prepares a release; production deployment may require manual approval.
- **Continuous Deployment:** Every change that passes the pipeline is automatically released to production.

---

## Git and Version Control Concepts

### Why version control?

A Version Control System (VCS) tracks file changes over time so that teams can inspect who changed what, understand why, identify when a bug appeared, and return to a known version.

### Centralized vs. distributed VCS

| Centralized VCS | Distributed VCS (Git) |
|---|---|
| A central server holds the version history. | Each clone contains repository history. |
| Server availability is critical for many operations. | Many operations, including commits and history inspection, work locally. |
| Examples named in the session: SVN, CVS, Perforce. | Examples named in the session: Git, Mercurial. |

**Git is not GitHub:** Git is the version-control tool. GitHub hosts Git repositories and provides a web interface, pull requests, issues, code review, and CI/CD features.

### The three areas of Git

1. **Working directory:** The files you currently edit.
2. **Staging area (index):** The selected changes prepared for the next commit.
3. **Local repository (`.git`):** Stored commit history, objects, branch pointers, tags, and metadata.

Typical flow:

```text
Working Directory  --git add-->  Staging Area  --git commit-->  Local Repository
```

### Git object model

The supplied Session 1 describes Git as storing snapshots:

- **Blob:** File content.
- **Tree:** Directory structure and references to blobs/subtrees.
- **Commit:** Points to a top-level tree and records author/committer metadata, message, timestamp, and parent commit(s).
- **Hash:** Identifies an object by a content-derived checksum.

A commit records the staged snapshot, not every untracked or unstaged change in the working directory.

---

## Install and Configure Git on Windows

### Install Git for Windows

1. Download Git for Windows from [git-scm.com/download/win](https://git-scm.com/download/win).
2. Run the installer.
3. The lab guide recommends:
   - Default branch name: `main`.
   - PATH option: Git from the command line and also from third-party software.
   - Line endings: checkout Windows-style and commit Unix-style line endings.
   - Terminal: MinTTY, the default Git Bash terminal.
4. Open **Git Bash** from the Windows Start menu.

### Verify installation

```bash
git --version
pwd
```

Git Bash maps the Windows user profile to `~`. For example, `C:\Users\Student` is commonly represented as `/c/Users/Student`.

### Configure your identity

Replace the example values with your own name and the email associated with your GitHub account:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Configure Windows line endings

```bash
git config --global core.autocrlf true
```

Windows commonly uses CRLF (`\r\n`), while Linux and many Git repository files use LF (`\n`). This setting converts line endings during checkout and commit to reduce unnecessary line-ending diffs.

### Set the default branch and editor

```bash
git config --global init.defaultBranch main
git config --global core.editor "notepad"
```

If you use VS Code and the `code` command is available, you may instead set:

```bash
git config --global core.editor "code --wait"
```

### Verify configuration

```bash
git config --list --show-origin
```

Check that `user.name`, `user.email`, `core.autocrlf`, and `init.defaultBranch` have the intended values.

### Configuration scopes

| Scope | Command | Applies to |
|---|---|---|
| System | `git config --system` | All users on the machine |
| Global | `git config --global` | Your operating-system user |
| Local | `git config --local` | The current repository |

Local repository settings can override global settings.

---

## Set Up SSH Authentication with GitHub

The lab uses an ED25519 SSH key pair. GitHub CLI operations over HTTPS do not accept the account password; use SSH authentication or a Personal Access Token (PAT) as appropriate.

### 1. Check for existing SSH keys

```bash
ls -la ~/.ssh
```

If `id_ed25519` and `id_ed25519.pub` already exist, you may be able to reuse them. Do not overwrite an existing private key without understanding which services use it.

### 2. Generate a key pair if needed

```bash
ssh-keygen -t ed25519 -C "your.email@example.com"
```

Press Enter to accept the default path, and optionally set a passphrase. The private key is `~/.ssh/id_ed25519`; the public key is `~/.ssh/id_ed25519.pub`.

### 3. Start the SSH agent and add the private key

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

### 4. Display the public key

```bash
cat ~/.ssh/id_ed25519.pub
```

Copy the complete public key output. **Never share or upload `~/.ssh/id_ed25519`**, which is the private key.

### 5. Add the key to GitHub

1. Sign in to GitHub.
2. Open **Settings → SSH and GPG keys**.
3. Select **New SSH key**.
4. Give it a recognizable title, such as `Windows Lab PC`.
5. Keep the key type as an authentication key.
6. Paste the public key and save it.

### 6. Test SSH authentication

```bash
ssh -T git@github.com
```

On the first connection, verify the host fingerprint prompt before accepting it. Successful authentication produces a message similar to:

```text
Hi YOUR_USERNAME! You've successfully authenticated, but GitHub does not provide shell access.
```

---

## Lab 1 — Create a Local Repository

### 1. Create the lab directory

```bash
mkdir -p ~/devops-labs/day01-git-practice
cd ~/devops-labs/day01-git-practice
```

### 2. Initialize Git

```bash
git init
git branch --show-current
ls -la .git
```

The `.git` directory stores repository metadata and history. Deleting it removes the local Git history for that repository.

### 3. Create the initial HTML page

```bash
cat << 'EOF' > index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>DevOps Portal</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, sans-serif;
            margin: 40px;
            background: #eef2f5;
        }
        .card {
            background: white;
            padding: 25px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #0066cc;
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>DevOps Continuous Delivery Portal</h1>
        <p>Environment: Windows Workstation</p>
        <p>Release Version: 1.0.0</p>
    </div>
</body>
</html>
EOF
```

### 4. Inspect the repository status

```bash
git status
```

Because the file is new and has not been staged, it appears as untracked.

---

## Lab 2 — Stage, Commit, Diff, and Inspect History

### 1. Stage the initial page

```bash
git add index.html
git status
```

The file should now appear under changes to be committed.

### 2. Commit it

```bash
git commit -m "feat: add baseline DevOps portal"
```

### 3. Add a footer

```bash
cat << 'EOF' >> index.html
<footer>
    <p>Maintained on Windows PC - CDAC DevOps Module</p>
</footer>
EOF
```

### 4. Inspect unstaged and staged changes

```bash
# Working directory compared with staging area
git diff

# Stage the footer change
git add index.html

# Staging area compared with the latest commit
git diff --staged
```

### 5. Commit the footer

```bash
git commit -m "docs: add portal footer"
```

### 6. Review commit history

```bash
# Full history
git log

# Compact history
git log --oneline

# History with branch graph and decorations
git log --oneline --graph --decorate --all

# Show patches for the last two commits
git log -p -2
```

**Remember:** `git add` selects changes for the next commit. `git commit` records the staged snapshot in local history.

---

## Lab 3 — Create a Windows-Friendly `.gitignore`

### Objective

Prevent OS metadata, logs, build artifacts, temporary files, and sensitive configuration from being tracked.

### 1. Create sample files

```bash
touch app.log
touch secrets.env
touch Thumbs.db
```

Inspect the status:

```bash
git status
```

### 2. Create `.gitignore`

```bash
cat << 'EOF' > .gitignore
# Windows operating-system files
Thumbs.db
ehthumbs.db
Desktop.ini
$RECYCLE.BIN/

# macOS metadata
.DS_Store

# Logs and temporary files
*.log
*.tmp

# Sensitive environment configuration
.env
*.env
*.pem
credentials.json

# Build artifacts and dependencies
*.exe
*.o
bin/
obj/
node_modules/
EOF
```

### 3. Verify ignored files

```bash
git status
git check-ignore -v app.log secrets.env Thumbs.db
```

Stage and commit the ignore rules:

```bash
git add .gitignore
git commit -m "chore: add gitignore rules"
```

**Important:** `.gitignore` does not untrack a file that Git already tracks. If a sensitive file was committed previously, remove it from tracking and handle any exposed secret appropriately. For example, `git rm --cached FILE` removes it from the index but leaves the local file. Rotating a leaked credential may still be necessary.

---

## Lab 4 — Branching and Fast-Forward Merge

A branch is a lightweight, movable pointer to a commit. `HEAD` indicates the currently checked-out branch or commit.

### 1. Create a feature branch

```bash
git branch
git switch -c feature/status-indicator
git branch
```

The `-c` option creates the branch and switches to it.

### 2. Update the page on the feature branch

```bash
cat << 'EOF' > index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>DevOps Portal</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, sans-serif;
            margin: 40px;
            background: #eef2f5;
        }
        .card {
            background: white;
            padding: 25px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .status-badge {
            display: inline-block;
            padding: 5px 12px;
            background: #28a745;
            color: white;
            border-radius: 20px;
            font-weight: bold;
        }
        h1 {
            color: #0066cc;
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>DevOps Continuous Delivery Portal</h1>
        <span class="status-badge">System Status: OPERATIONAL</span>
        <p>Environment: Windows Workstation</p>
        <p>Release Version: 1.1.0-feature</p>
    </div>
    <footer>
        <p>Maintained on Windows PC - CDAC DevOps Module</p>
    </footer>
</body>
</html>
EOF
```

Stage and commit:

```bash
git add index.html
git commit -m "feat: add operational status indicator"
```

### 3. Merge the feature branch into `main`

```bash
git switch main
git merge feature/status-indicator
```

Because `main` has no competing commits since the feature branch was created, Git can perform a fast-forward merge: it moves the `main` pointer forward without creating a separate merge commit.

### 4. Delete the merged branch

```bash
git branch -d feature/status-indicator
git log --oneline --graph --decorate --all
```

---

## Lab 5 — Create and Resolve a Merge Conflict

A merge conflict can occur when branches make incompatible edits to the same lines, or when one branch edits a file that the other branch deletes. Git pauses and requires a human to choose the final content.

### 1. Create the maintenance branch

```bash
git switch -c feature/maintenance-alert
```

Replace the page with the maintenance version:

```bash
cat << 'EOF' > index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>DevOps Portal</title>
</head>
<body>
    <div style="background: #ffeb3b; padding: 15px; font-weight: bold; text-align: center;">
        WARNING: Database Maintenance Scheduled for 10:00 PM Tonight
    </div>
    <div class="card">
        <h1>DevOps Portal (Maintenance Branch)</h1>
    </div>
</body>
</html>
EOF

git add index.html
git commit -m "feat: add maintenance alert banner"
```

### 2. Make a competing edit on `main`

```bash
git switch main
```

```bash
cat << 'EOF' > index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>DevOps Portal</title>
</head>
<body>
    <div style="background: #007acc; color: white; padding: 15px; font-weight: bold; text-align: center;">
        ANNOUNCEMENT: Cloud Infrastructure Upgrade Completed
    </div>
    <div class="card">
        <h1>DevOps Portal (Production)</h1>
    </div>
</body>
</html>
EOF

git add index.html
git commit -m "docs: announce cloud infrastructure upgrade"
```

### 3. Attempt the merge

```bash
git merge feature/maintenance-alert
```

Git should report a conflict if the branch histories and edits match the lab scenario.

Check which files are conflicted:

```bash
git status
```

### 4. Understand conflict markers

Git may insert content like:

```text
<<<<<<< HEAD
ANNOUNCEMENT: Cloud Infrastructure Upgrade Completed
=======
WARNING: Database Maintenance Scheduled for 10:00 PM Tonight
>>>>>>> feature/maintenance-alert
```

- `<<<<<<< HEAD`: start of the current branch's version.
- `=======`: separator between the competing versions.
- `>>>>>>> feature/maintenance-alert`: end of the incoming branch's version.

### 5. Resolve the conflict

Open `index.html` in an editor and decide what the final page should contain. You can retain one version or combine the announcement and maintenance alert. Remove **all** conflict marker lines.

For example, use this combined page:

```bash
cat << 'EOF' > index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>DevOps Portal</title>
</head>
<body>
    <div style="background: #007acc; color: white; padding: 15px; font-weight: bold; text-align: center;">
        ANNOUNCEMENT: Cloud Infrastructure Upgrade Completed
    </div>
    <div style="background: #ffeb3b; padding: 15px; font-weight: bold; text-align: center;">
        WARNING: Database Maintenance Scheduled for 10:00 PM Tonight
    </div>
    <div class="card">
        <h1>DevOps Portal</h1>
    </div>
</body>
</html>
EOF
```

Stage the resolution and complete the merge:

```bash
git add index.html
git commit -m "fix: resolve merge conflict in index.html"
git status
git log --oneline --graph --decorate --all
```

Delete the feature branch after the merge is complete:

```bash
git branch -d feature/maintenance-alert
```

If the merge needs to be abandoned before resolution, use `git merge --abort` while the merge is in progress.

---

## Lab 6 — Publish the Repository to GitHub

### 1. Create a repository on GitHub

1. Visit [github.com/new](https://github.com/new).
2. Name it `devops-day01-practice`.
3. Choose Public or Private.
4. For this lab's existing local repository, do **not** initialize the remote with an additional README, `.gitignore`, or license.
5. Create the repository and copy its SSH URL.

### 2. Add the remote

Replace `YOUR_GITHUB_USERNAME` with your username:

```bash
git remote add origin git@github.com:YOUR_GITHUB_USERNAME/devops-day01-practice.git
git remote -v
```

If `origin` already exists, inspect it with `git remote -v` and update it using `git remote set-url origin ...` rather than adding a duplicate.

### 3. Push the `main` branch

```bash
git push -u origin main
```

The `-u` flag sets upstream tracking, so later pushes and pulls can use the configured upstream branch.

### 4. Verify and pull

Refresh the repository page on GitHub and confirm the files and commit history appear.

```bash
git pull origin main
git status
```

If Git reports `Already up to date`, there are no incoming changes to integrate.

### 5. Remote workflow cheat sheet

```bash
# Show remote names and URLs
git remote -v

# Download remote commits and references without merging into the current branch
git fetch origin

# Fetch and integrate remote main into the current branch
git pull origin main

# Push local main to remote origin
git push origin main

# Clone an existing repository
git clone git@github.com:YOUR_GITHUB_USERNAME/devops-day01-practice.git
```

---

## Lab 7 — Scaffold the DevOps Capstone Project

The lab guide prepares a repository structure for the later Docker and DevOps modules.

### 1. Create the directories

Run from `~/devops-labs/day01-git-practice`:

```bash
mkdir -p src k8s scripts
```

### 2. Create the starter Python application

```bash
cat << 'EOF' > src/app.py
import http.server
import socketserver

PORT = 8080


class SimpleHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        html = """
        <!DOCTYPE html>
        <html>
        <head><title>DevOps Capstone Application</title></head>
        <body style="font-family: Arial, sans-serif; text-align: center; margin-top: 50px;">
            <h1>DevOps Microservice Portal</h1>
            <p>Running on Python 3 Standard HTTP Server</p>
            <p>Ready for Docker Containerization (Day 02)</p>
        </body>
        </html>
        """
        self.wfile.write(html.encode("utf-8"))


if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), SimpleHandler) as httpd:
        print(f"DevOps Application listening on port {PORT}...")
        httpd.serve_forever()
EOF
```

Run it locally if Python 3 is installed:

```bash
python src/app.py
```

Open `http://localhost:8080` in a browser. Stop the server with `Ctrl+C`. The supplied sample uses Python's standard HTTP server for a simple lab demonstration; it is not a production-grade application server.

### 3. Create a project README

```bash
cat << 'EOF' > README.md
# DevOps Capstone Project

## Description
This repository contains the baseline code for the CDAC PGCP-ITISS DevOps curriculum.

## Module Milestones
- Day 01: Git & GitHub version control
- Day 02: Docker containerization and Dockerfile packaging
- Day 03: Multi-container stacks with Compose and Swarm
- Day 04: Kubernetes deployment manifests and monitoring
- Day 05: Jenkins automated CI/CD pipelines
- Day 06–10: Infrastructure automation and related DevOps tools
EOF
```

### 4. Inspect, commit, and push

```bash
git status
git add src/ k8s/ scripts/ README.md
git commit -m "chore: scaffold DevOps capstone project"
git push origin main
git log --oneline -n 5
```

### Suggested repository layout

```text
devops-day01-practice/
├── .gitignore
├── README.md
├── index.html
├── src/
│   └── app.py
├── scripts/
└── k8s/
```

Later modules may add a `Dockerfile`, `docker-compose.yml`, and Kubernetes manifests under `k8s/`.

---

## GitHub Collaboration and Remote Workflows

The supplied Session 2 explains a feature-branch and pull-request workflow for team collaboration.

### Typical pull-request workflow

1. Update `main`.
2. Create a feature branch.
3. Make changes and commit them.
4. Push the feature branch.
5. Open a pull request (PR) targeting `main`.
6. A reviewer checks the changes; automated CI tests may run.
7. After approval, merge the PR.
8. Switch back to `main` and pull the latest changes.

Example commands:

```bash
git switch main
git pull origin main
git switch -c feat/api-endpoint

# Make and test changes, then stage and commit
git add .
git commit -m "feat: add API endpoint"

git push -u origin feat/api-endpoint
```

Open the pull request on GitHub. The individual Day 01 lab focuses on a personal repository, while Session 2 introduces this collaborative workflow conceptually.

---

## GitFlow Branching Strategy

The supplied `Git-Branching-Strategy.pdf` describes GitFlow as a structured model for parallel feature work, scheduled releases, and urgent production patches. It defines five branch types.

### The five core branches

| Branch | Created from | Merged back to | Purpose |
|---|---|---|---|
| `main` (called `master` in older examples) | Existing production history | N/A | Production-ready code; release tags are created here. Direct commits are discouraged. |
| `develop` | `main` | `main` via release; release changes return to `develop` | Integration branch for completed features and testing. |
| `feature/*` | `develop` | `develop` | Isolated feature development. |
| `release/*` | `develop` | `main` and `develop` | Release stabilization, minor fixes, documentation, and metadata; no new features. |
| `hotfix/*` | Production branch (`main`) | `main` and `develop` | Emergency production fixes. |

The reference uses both `master` and `main` in its table and examples. This README uses `main` for the commands, matching the Day 01 lab's default branch.

### Scenario A — Normal feature development

```bash
git switch develop
git switch -c feature/user-profile

# Make changes, test them, then commit
git add .
git commit -m "feat: add user profile"

git switch develop
git merge --no-ff feature/user-profile
git branch -d feature/user-profile
```

`--no-ff` forces a merge commit even when Git could fast-forward. The reference recommends it to preserve the history of a feature integration.

### Scenario B — Prepare release `1.1.0`

Create a release branch after the planned features have been integrated into `develop`:

```bash
git switch develop
git switch -c release-1.1.0
```

Perform regression testing and make only stabilization fixes. The reference stresses that fixes on a release branch must be synchronized back into `develop`.

When the release is verified:

```bash
git switch main
git merge --no-ff release-1.1.0
git tag -a 1.1.0 -m "Release version 1.1.0"

git switch develop
git merge --no-ff release-1.1.0
git branch -d release-1.1.0
```

### Scenario C — Emergency hotfix `1.0.1`

Start from the production branch, fix and test the defect, merge it into production, and tag the patch release:

```bash
git switch main
git switch -c hotfix-1.0.1

# Fix and test the production defect, then commit
git add .
git commit -m "fix: resolve critical production defect"

git switch main
git merge --no-ff hotfix-1.0.1
git tag -a 1.0.1 -m "Hotfix version 1.0.1"

git switch develop
git merge --no-ff hotfix-1.0.1
git branch -d hotfix-1.0.1
```

The key rule is the **two-way merge**: the hotfix goes into both `main` and `develop`, preventing future development from reintroducing the production defect.

### GitFlow best practices from the reference

- Keep the production branch stable and tested.
- Prefer `--no-ff` for integration merges when preserving branch history is required.
- Back-merge release and hotfix changes into `develop`.
- Tag every production release so a CI/CD pipeline can refer to a specific release milestone.
- Do not create a release branch until the planned features are integrated and ready for stabilization.

> **Scope note:** GitFlow is included because a separate supplied PDF covers it. The Day 01 hands-on lab itself mainly practices local feature branches, merges, conflict resolution, and GitHub publishing.

---

## Essential Git Command Cheat Sheet

| Task | Command |
|---|---|
| Check version | `git --version` |
| Initialize repository | `git init` |
| Check status | `git status` |
| Stage one file | `git add index.html` |
| Stage all changes | `git add .` |
| Commit staged changes | `git commit -m "message"` |
| Show unstaged diff | `git diff` |
| Show staged diff | `git diff --staged` |
| Show history | `git log --oneline` |
| Show branch graph | `git log --oneline --graph --decorate --all` |
| List branches | `git branch` |
| Create and switch branch | `git switch -c feature/name` |
| Switch branch | `git switch main` |
| Merge branch | `git merge feature/name` |
| Force merge commit | `git merge --no-ff feature/name` |
| Delete merged branch | `git branch -d feature/name` |
| Abort an in-progress merge | `git merge --abort` |
| Add remote | `git remote add origin SSH_URL` |
| Show remotes | `git remote -v` |
| Fetch remote updates | `git fetch origin` |
| Pull remote main | `git pull origin main` |
| Push main | `git push -u origin main` |
| Show ignored-file rule | `git check-ignore -v FILE` |
| Discard unstaged changes in a file | `git restore FILE` |
| Unstage a file | `git restore --staged FILE` |
| Amend last commit message | `git commit --amend -m "new message"` |
| List tags | `git tag` |
| Create annotated tag | `git tag -a 1.0.0 -m "Release version 1.0.0"` |

**Caution:** `git restore FILE` discards unstaged edits to that file. `git branch -D` force-deletes a branch and may discard unmerged work. Use destructive commands only when you understand what will be lost.

---

## Windows Troubleshooting

### `warning: LF will be replaced by CRLF`

With `core.autocrlf=true`, Git may report line-ending normalization. This is often expected. Check the repository's line-ending policy if the warning is frequent or produces noisy diffs.

### `Permission denied (publickey)` during push

Check that the public key is in your GitHub account and the private key is loaded:

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
ssh -T git@github.com
git remote -v
```

Make sure the remote URL uses the intended GitHub username and repository.

### Accidentally modified a file

To discard unstaged changes in `index.html`:

```bash
git restore index.html
```

This cannot recover edits that were never saved elsewhere.

### Accidentally staged a file

To unstage a file without deleting the local changes:

```bash
git restore --staged secret.txt
```

If the file contains credentials, do not commit it. Add an appropriate ignore rule and verify status.

### Fix a typo in the latest commit message

```bash
git commit --amend -m "fix: corrected commit message"
```

Amending rewrites the commit. Avoid amending a commit that has already been shared unless you understand the consequences for collaborators.

### `origin` already exists

Inspect the configured URL:

```bash
git remote -v
```

If it is wrong, update it rather than adding another remote:

```bash
git remote set-url origin git@github.com:YOUR_GITHUB_USERNAME/devops-day01-practice.git
```

### Push rejected

Fetch and inspect the remote history before integrating it:

```bash
git fetch origin
git status
git log --oneline --graph --decorate --all
```

If the remote was initialized with commits that are not in your local history, the histories may need to be reconciled. Do not use force push as a first response.

---

## Security and Good Practices

- Never commit a private SSH key, access token, password, `.env` file, or real credentials.
- Use `.gitignore` for files that should not be tracked, but remember it does not remove secrets already committed.
- Use clear, short commit messages; the sessions recommend imperative wording and show Conventional Commit prefixes such as `feat:`, `fix:`, `docs:`, and `chore:`.
- Check `git status` before staging and committing.
- Inspect changes with `git diff` and `git diff --staged`.
- Use branches to isolate work and merge only after testing.
- Resolve all merge markers before completing a merge.
- Push to GitHub regularly and verify the remote URL.
- Tag production releases in the GitFlow workflow and synchronize hotfixes/release fixes back into `develop`.

---

## Self-Assessment Checklist

- [ ] Git for Windows is installed and `git --version` works.
- [ ] `user.name`, `user.email`, `core.autocrlf`, and the default branch are configured.
- [ ] SSH authentication to GitHub succeeds.
- [ ] A local repository has been initialized and `.git` inspected.
- [ ] Changes have been staged, committed, diffed, and reviewed in the log.
- [ ] `.gitignore` excludes Windows metadata, logs, build artifacts, and sensitive configuration.
- [ ] A feature branch has been created and merged into `main`.
- [ ] A merge conflict has been produced, manually resolved, and committed.
- [ ] The repository is connected to GitHub via `origin`.
- [ ] `main` has been pushed and a pull has been tested.
- [ ] The `src/`, `k8s/`, and `scripts/` project scaffold exists.
- [ ] `src/app.py` runs on port 8080.
- [ ] The GitFlow branch purposes and release/hotfix back-merges are understood.

---

## Review Questions

1. What is the “Wall of Confusion,” and how does DevOps address it?
2. How do Continuous Integration, Continuous Delivery, and Continuous Deployment differ?
3. What is the difference between Git and GitHub?
4. How does a distributed VCS differ from a centralized VCS?
5. What are the working directory, staging area, and local repository?
6. What do Git blobs, trees, and commits represent?
7. Why is `core.autocrlf` relevant on Windows?
8. What is the difference between `git diff` and `git diff --staged`?
9. Why is `.gitignore` important, and what does it not do?
10. What is a fast-forward merge? How does it differ from a merge commit?
11. What do `<<<<<<<`, `=======`, and `>>>>>>>` mean in a conflict?
12. What is the difference between `git fetch` and `git pull`?
13. Why should SSH private keys and `.env` files never be committed?
14. What are the roles of `main`, `develop`, `feature/*`, `release/*`, and `hotfix/*` in GitFlow?
15. Why must release and hotfix changes be merged back into `develop`?
16. Why are annotated tags useful for production releases?

---

## Source PDFs

This README is based on the supplied Day 01 materials:

- **`Lab-Guide(2).pdf`** — 21-page Windows Git & GitHub individual developer lab: configuration, SSH, local repository lifecycle, `.gitignore`, branching, merge conflicts, GitHub publishing, capstone scaffold, troubleshooting, and checklist.
- **`Session-1(2).pdf`** — 8-page session on DevOps principles, lifecycle, CI/CD, VCS, Git architecture, configuration, and core commands.
- **`Session-2(2).pdf`** — 6-page session on branching, merging, conflicts, GitHub remote workflows, pull requests, and project structure.
- **`Git-Branching-Strategy.pdf`** — 4-page GitFlow reference covering branch roles, normal feature work, release preparation, hotfixes, tags, and back-merges.

The README preserves the source labs' Windows/Git Bash orientation and uses the supplied command patterns. GitFlow is presented as a related branching-strategy reference rather than as a replacement for the simpler individual workflow used in the lab exercises.
