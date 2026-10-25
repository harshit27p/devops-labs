# Containerize a Django Web Application with Docker

> **Video:** [Day-25 --- Containerizing a Django Application with Docker
> \| Abhishek Veeramalla](https://www.youtube.com/watch?v=3IAvr_O6vao)\
> **Playlist:** [DevOps Zero to
> Hero](https://www.youtube.com/playlist?list=PLdpzxOOAlwvIc1TjTwopNSjRJkzES2ZXk)\
> **Suggested path:** `03-django-docker/README.md`\
> **Prerequisites:** Basic Python, Django, Linux shell, and the Docker
> fundamentals in
> [`02-docker-fundamentals`](../02-docker-fundamentals/README.md).

This guide turns the video's Django-containerization workflow into a
repeatable lab, adds troubleshooting and deployment safety notes, and
explains which parts are suitable for learning versus production. To
avoid repeating earlier playlist notes, Docker architecture, the general
image lifecycle, and the complete CLI reference are linked rather than
retaught here.

------------------------------------------------------------------------

## Table of contents

-   [1. Learning objectives](#1-learning-objectives)
-   [2. Why containerize Django?](#2-why-containerize-django)
-   [3. Django project structure](#3-django-project-structure)
-   [4. Request flow inside Django](#4-request-flow-inside-django)
-   [5. Dockerizing the application](#5-dockerizing-the-application)
-   [6. Create a minimal Django
    project](#6-create-a-minimal-django-project)
-   [7. Add requirements and a
    Dockerfile](#7-add-requirements-and-a-dockerfile)
-   [8. Understand CMD and ENTRYPOINT](#8-understand-cmd-and-entrypoint)
-   [9. Build and run the image](#9-build-and-run-the-image)
-   [10. Publish the application on an EC2
    instance](#10-publish-the-application-on-an-ec2-instance)
-   [11. Ports, bind addresses, and security
    groups](#11-ports-bind-addresses-and-security-groups)
-   [12. Troubleshooting](#12-troubleshooting)
-   [13. Development versus
    production](#13-development-versus-production)
-   [14. Security and reliability
    checklist](#14-security-and-reliability-checklist)
-   [15. Hands-on exercises](#15-hands-on-exercises)
-   [16. Interview questions and
    answers](#16-interview-questions-and-answers)
-   [17. What belongs in later notes](#17-what-belongs-in-later-notes)
-   [18. References](#18-references)

------------------------------------------------------------------------

## 1. Learning objectives

By completing this lab, you should be able to:

1.  Explain the purpose of Django's `settings.py`, `urls.py`, and
    `views.py`.
2.  Create a minimal Django project that runs locally and inside a
    container.
3.  Write a Dockerfile that installs Python dependencies and starts
    Django.
4.  Explain how `CMD` and `ENTRYPOINT` behave differently.
5.  Build and run a Docker image with host-to-container port mapping.
6.  Explain why Django must listen on `0.0.0.0` inside a container for
    published-port access.
7.  Configure an EC2 security group carefully when testing a web
    application remotely.
8.  Identify why Django's development server and default settings are
    not production deployment choices.

## 2. Why containerize Django?

A Django application depends on more than its Python source. It may
require a specific Python version, Django version, Python packages,
system libraries, environment variables, static files, and access to a
database or other services.

Without a repeatable deployment process, developers can encounter:

-   Different Python or package versions across machines.
-   Missing dependencies on a new server.
-   Differences between local development and cloud deployment.
-   Manual setup that is difficult to reproduce.
-   Risky upgrades that are hard to roll back.

A container image packages the application and selected user-space
dependencies into a repeatable artifact. It does not automatically
package every external dependency: databases, secrets, persistent files,
and cloud configuration still need explicit handling.

### Where this fits in a DevOps workflow

``` text
Django source + requirements
           |
           v
     Automated tests
           |
           v
     Docker image build
           |
           v
    Image validation/scan
           |
           v
   Registry (optional)
           |
           v
  Deployment environment
           |
           v
   Logs, health and metrics
```

For Docker architecture and the difference between images and
containers, refer to
[`02-docker-fundamentals`](../02-docker-fundamentals/README.md).

## 3. Django project structure

A minimal Django project often looks like this:

``` text
django-docker-demo/
├── manage.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
└── config/
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    ├── asgi.py
    └── wsgi.py
```

Depending on the project, Django apps may be added as separate
directories with their own `views.py`, `models.py`, `urls.py`, and
templates.

### `settings.py` --- project configuration

This file controls settings such as installed apps, middleware, database
configuration, allowed hosts, static-file behavior, security options,
and secret-key configuration.

Important examples:

-   `INSTALLED_APPS`: applications enabled in the Django project.
-   `MIDDLEWARE`: request/response middleware stack.
-   `DATABASES`: database connection configuration.
-   `ALLOWED_HOSTS`: hostnames or IP addresses Django accepts in the
    HTTP `Host` header.
-   `DEBUG`: debugging mode; should be disabled in production.
-   `SECRET_KEY`: cryptographic signing key; must be kept secret.
-   `STATIC_URL` and related settings: static-file configuration.

**Container note:** do not hard-code production secrets into
`settings.py` or the image. Use environment variables or an appropriate
secrets-management mechanism.

### `urls.py` --- URL routing

URL configuration maps URL patterns to views. For example, a route for
the home page can call a `home` view.

``` python
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
]
```

The example above assumes a `views.py` module exists alongside
`urls.py`.

### `views.py` --- request handling

A view receives a request and returns a response. A minimal example:

``` python
from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello from Django running in Docker!")
```

In a larger application, views may query models, validate input, render
templates, or call business logic. Keep business logic organized rather
than putting every operation into a single view.

### `manage.py` --- project management

`manage.py` is a command-line entry point for tasks such as running the
development server, creating migrations, applying migrations, and
creating administrative users.

It is useful in development and administration, but a production
container commonly runs a production application server such as Gunicorn
for WSGI or an ASGI server for ASGI applications.

## 4. Request flow inside Django

For a simple request:

``` text
Browser / HTTP client
       |
       v
Host port 8000
       |
       | Docker port publishing
       v
Container port 8000
       |
       v
Django server process
       |
       v
Django middleware
       |
       v
URL resolver (urls.py)
       |
       v
View function (views.py)
       |
       v
HTTP response
```

`settings.py` supplies configuration used by several stages of the
request lifecycle. If the view needs a database, Django uses the
configured database connection.

Port publishing only forwards network traffic; it does not fix Django
configuration, host-header validation, application errors, or firewall
restrictions.

## 5. Dockerizing the application

The basic containerization plan is:

1.  Start with a supported Python base image.
2.  Set a working directory.
3.  Copy dependency declarations.
4.  Install dependencies.
5.  Copy the project code.
6.  Specify how the application starts.
7.  Build the image and run a container.
8.  Test the response and logs.

For better build caching, copy `requirements.txt` before copying the
rest of the source. That way, ordinary source-code edits do not
necessarily invalidate the dependency-installation step.

## 6. Create a minimal Django project

The following commands create a small runnable example. Run them on a
machine with Docker installed.

### Step 1 --- Create the directory

``` bash
mkdir -p django-docker-demo/config
cd django-docker-demo
```

### Step 2 --- Create `requirements.txt`

``` bash
cat <<'EOF' > requirements.txt
Django>=5.2,<5.3
gunicorn>=23,<24
EOF
```

This is a learning example using a bounded Django version range and
Gunicorn. For a reproducible production release, generate and maintain a
tested lock/pinned dependency set and update it intentionally.

### Step 3 --- Create the Django package files

``` bash
touch config/__init__.py
```

Create `config/settings.py`:

``` bash
cat <<'EOF' > config/settings.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "development-only-change-me-before-deployment"
)
DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"

# Local Docker lab defaults. Set this to explicit domains/IPs in deployment.
ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    if host.strip()
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
EOF
```

**Important:** the fallback secret key and `DEBUG=True` are strictly for
the local learning example. Do not deploy those defaults publicly. A
production configuration must use a strong secret from a secure source,
`DEBUG=False`, correct host validation, and suitable HTTPS/security
settings.

Create `config/urls.py`:

``` bash
cat <<'EOF' > config/urls.py
from django.contrib import admin
from django.urls import path
from django.http import JsonResponse

def home(request):
    return JsonResponse({
        "message": "Hello from Django running in Docker!",
        "status": "ok"
    })

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
]
EOF
```

Create `config/wsgi.py`:

``` bash
cat <<'EOF' > config/wsgi.py
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
application = get_wsgi_application()
EOF
```

Create `config/asgi.py`:

``` bash
cat <<'EOF' > config/asgi.py
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
application = get_asgi_application()
EOF
```

Create `manage.py`:

``` bash
cat <<'EOF' > manage.py
#!/usr/bin/env python
import os
import sys
from django.core.management import execute_from_command_line

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    execute_from_command_line(sys.argv)
EOF
```

## 7. Add requirements and a Dockerfile

Create a `.dockerignore` file:

``` bash
cat <<'EOF' > .dockerignore
.git
.venv
__pycache__/
*.py[cod]
.env
db.sqlite3
staticfiles/
EOF
```

This reduces unnecessary build-context files and helps prevent
accidental inclusion of local configuration. If your application
requires a file listed here, adjust the rules intentionally.

Create `Dockerfile`:

``` dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### Dockerfile explanation

  -----------------------------------------------------------------------
  Instruction                         Purpose
  ----------------------------------- -----------------------------------
  `FROM`                              Chooses the base image containing
                                      Python.

  `ENV`                               Configures Python behavior for the
                                      container process.

  `WORKDIR`                           Sets the working directory inside
                                      the image.

  `COPY requirements.txt .`           Copies the dependency file before
                                      the application source to improve
                                      caching.

  `RUN pip install ...`               Installs Python packages while
                                      building the image.

  `COPY . .`                          Copies the remaining build-context
                                      files into `/app`.

  `EXPOSE 8000`                       Documents the port the application
                                      expects to use; it does not publish
                                      the port by itself.

  `CMD`                               Defines the default process and
                                      arguments used to start the app.
  -----------------------------------------------------------------------

### Why use Gunicorn in this example?

Django's `runserver` is designed for development, not production. This
example uses Gunicorn to serve the Django WSGI application. Gunicorn is
a process server; a complete production design may also include a
reverse proxy, TLS termination, static-file handling, a database,
monitoring, and other services.

This Dockerfile is a teaching baseline, not a fully hardened production
image. Later notes can cover non-root execution, dependency pinning,
health checks, static files, multi-stage builds, and build security.

## 8. Understand CMD and ENTRYPOINT

These instructions are related but serve different purposes.

### `CMD`

`CMD` supplies the default command or default arguments for a container.
It is straightforward to override when running the image.

``` dockerfile
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

A user can replace the command:

``` bash
docker run IMAGE python manage.py check
```

### `ENTRYPOINT`

`ENTRYPOINT` configures the executable that the container is primarily
intended to run. With exec-form `ENTRYPOINT`, arguments supplied to
`docker run IMAGE ...` are appended to the entrypoint command.

``` dockerfile
ENTRYPOINT ["gunicorn"]
CMD ["config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

Here, `CMD` supplies default arguments to Gunicorn. A user can replace
those arguments:

``` bash
docker run IMAGE config.wsgi:application --bind 0.0.0.0:9000
```

The executable remains Gunicorn.

### Practical comparison

  -----------------------------------------------------------------------
  Behavior                `CMD`                   `ENTRYPOINT`
  ----------------------- ----------------------- -----------------------
  Typical role            Default command or      Main executable
                          arguments               

  Replaced by command     Usually yes             Usually the supplied
  after image name                                arguments are appended
                                                  to exec-form entrypoint

  Common use              Default server command  Fixed executable or CLI
                                                  tool

  Can be combined         Yes                     Yes; `CMD` can supply
                                                  default arguments
  -----------------------------------------------------------------------

Neither instruction makes an executable literally impossible to
override. The distinction is about the default command-line behavior.
Prefer JSON/exec form for predictable signal handling and argument
processing.

## 9. Build and run the image

From the directory containing `Dockerfile`:

### Step 1 --- Build

``` bash
docker build -t django-demo:1.0 .
```

If your user does not have permission to access Docker, use
`sudo docker ...` or follow the security guidance in the Docker
fundamentals README.

### Step 2 --- Run with port mapping

``` bash
docker run --name django-demo-container \
  -p 8000:8000 \
  -e DJANGO_DEBUG=1 \
  -e DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1 \
  django-demo:1.0
```

The `-p 8000:8000` option maps **host port 8000** to **container port
8000**. The app binds to `0.0.0.0:8000` inside the container, allowing
traffic routed to the container's network interface.

This local command uses development-oriented settings. Do not expose it
publicly as a production deployment.

### Step 3 --- Test from the host

Open:

``` text
http://localhost:8000/
```

Or use:

``` bash
curl http://localhost:8000/
```

Expected response:

``` json
{"message":"Hello from Django running in Docker!","status":"ok"}
```

### Step 4 --- Inspect logs

In another terminal:

``` bash
docker ps
docker logs django-demo-container
docker inspect django-demo-container
```

### Step 5 --- Stop and remove

``` bash
docker stop django-demo-container
docker rm django-demo-container
```

If the container is already stopped, `docker stop` may report that it is
not running; inspect its status before cleanup.

### Alternative: run detached

``` bash
docker run -d --name django-demo-container \
  -p 8000:8000 \
  -e DJANGO_DEBUG=1 \
  -e DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1 \
  django-demo:1.0
```

`-d` runs the container in the background. View logs with
`docker logs -f django-demo-container`.

## 10. Publish the application on an EC2 instance

This section explains how to test the app from outside an Ubuntu EC2
instance. Use a disposable learning environment, not a production host
with development settings.

### Step 1 --- Install Docker and transfer/build the project

Follow the installation steps in
[`02-docker-fundamentals`](../02-docker-fundamentals/README.md). Copy
the project to the instance or clone your repository, then build the
image there:

``` bash
docker build -t django-demo:1.0 .
```

Alternatively, publish the image to a registry and pull it on EC2. Avoid
committing real secrets into the repository or image.

### Step 2 --- Run the container

For a **temporary lab only**, use an explicit public hostname/IP in the
allowed-host list and keep in mind that `DEBUG=True` is not safe for
public exposure. A safer baseline is to set `DEBUG=False` and provide a
secure secret key, even in a lab:

``` bash
docker run -d --name django-demo-container \
  -p 8000:8000 \
  -e DJANGO_DEBUG=0 \
  -e DJANGO_SECRET_KEY='REPLACE_WITH_A_LONG_RANDOM_SECRET' \
  -e DJANGO_ALLOWED_HOSTS='EC2_PUBLIC_DNS,EC2_PUBLIC_IP' \
  django-demo:1.0
```

Replace both host placeholders with the actual EC2 public DNS name and
public IP, without angle brackets. Supply the secret securely; this
command is shown as a learning illustration and may expose it in shell
history or process metadata depending on the environment. For real
deployments, use a suitable secrets-management mechanism.

The sample settings still do not configure every production security
control, TLS, a persistent production database, or static-file serving.
Do not treat the above as a complete production deployment.

### Step 3 --- Check locally on the EC2 host

``` bash
curl -i http://127.0.0.1:8000/
docker ps
docker logs django-demo-container
```

If local access fails, solve the application/container issue before
investigating AWS ingress rules.

### Step 4 --- Configure the EC2 security group

In the AWS console:

1.  Open **EC2 → Instances** and select the instance.
2.  Open the attached security group.
3.  Edit inbound rules.
4.  Add a temporary rule for **Custom TCP**, port **8000**.
5.  Set the source to **your own public IP `/32`** for a personal lab,
    where feasible.
6.  Save and test from your own machine using
    `http://EC2_PUBLIC_DNS:8000/`.

Do not use a source of `0.0.0.0/0` for an application running with
development settings. If IPv6 ingress is configured, review its rules
too.

### Step 5 --- Understand the network path

``` text
Your browser
    |
    | TCP 8000
    v
EC2 security group / network path
    |
    v
EC2 host port 8000
    |
    | Docker port publishing
    v
Container port 8000
    |
    v
Gunicorn -> Django application
```

A successful connection requires every layer to be configured correctly.
The security group cannot make an app listening only on the container's
loopback interface reachable, and Docker port mapping cannot override an
AWS security-group denial.

### Step 6 --- Remove public access when finished

Delete the temporary inbound rule or restrict it to the minimum required
source range. Stop and remove the lab container and shut down or
terminate unused AWS resources according to your lab plan.

## 11. Ports, bind addresses, and security groups

These three settings solve different problems.

### Application bind address

Inside a container:

-   `127.0.0.1:8000` usually listens only on the container's loopback
    interface.
-   `0.0.0.0:8000` listens on all IPv4 interfaces in the container
    network namespace.

For the common Docker bridge-network case, the app should listen on
`0.0.0.0` for published-port traffic to reach it.

### Docker port publishing

``` bash
docker run -p 8000:8000 IMAGE
```

This maps host TCP port 8000 to container TCP port 8000. To publish only
on the host's loopback interface:

``` bash
docker run -p 127.0.0.1:8000:8000 IMAGE
```

The loopback-only version is useful when a reverse proxy on the same
host will be the only intended access path.

### AWS security group

A security group filters traffic to the EC2 network interface. It does
not change the container's bind address or Docker's port mapping. For
remote access, the security group must allow the desired traffic and the
instance must have a working network path.

**Security principle:** expose the fewest ports possible, to the
narrowest source ranges possible.

## 12. Troubleshooting

  --------------------------------------------------------------------------------------
  Symptom                 Likely cause            First checks
  ----------------------- ----------------------- --------------------------------------
  `docker build` fails    Invalid Dockerfile,     Read the first failing build step;
                          missing files,          inspect `pwd`, `ls -la`, and
                          dependency install      `requirements.txt`.
                          failure                 

  Container exits         Server failed to start  `docker ps -a`,
  immediately             or configuration error  `docker logs django-demo-container`.

  Browser gets connection App not running, wrong  Check logs, `docker ps`,
  refused                 port, wrong bind        `docker port django-demo-container`.
                          address, or port not    
                          published               

  `DisallowedHost`        Requested host is       Set `DJANGO_ALLOWED_HOSTS` to the
                          missing from            intended hostname/IP.
                          `ALLOWED_HOSTS`         

  EC2 works locally but   Security group,         `curl` on EC2 first; then verify
  not remotely            routing, host firewall, inbound TCP/8000 and network path.
                          or wrong public address 

  Django static files are Static assets have not  Review `STATIC_ROOT`, `collectstatic`,
  missing                 been collected or       and the production static-file
                          served appropriately    strategy.

  `ModuleNotFoundError`   Dependency missing or   Verify `requirements.txt`, build logs,
                          not included in         and the installed packages in the
                          requirements            image.

  Port already allocated  Another                 `docker ps`, `sudo ss -lntp`; choose a
                          process/container       different host port if appropriate.
                          already uses the host   
                          port                    

  `DisallowedHost` only   Public DNS/IP not       Use the exact public DNS name/IP
  in EC2                  configured in allowed   needed for the lab.
                          hosts                   

  App cannot connect to   Wrong hostname,         Verify service DNS, environment,
  database                credentials, network,   credentials, and connectivity;
                          or database not ready   `localhost` inside a container means
                                                  that container.
  --------------------------------------------------------------------------------------

### Useful commands

``` bash
docker ps -a
docker logs -f django-demo-container
docker inspect django-demo-container
docker port django-demo-container
docker exec -it django-demo-container sh
sudo ss -lntp
curl -i http://127.0.0.1:8000/
```

If the image uses a slim base without diagnostic tools, use host-side
diagnostics or a temporary debug image rather than permanently adding
unnecessary packages to the production image.

## 13. Development versus production

  -----------------------------------------------------------------------
  Concern                 Development lab         Production direction
  ----------------------- ----------------------- -----------------------
  Django server           `runserver` can be used Use a suitable
                          locally                 WSGI/ASGI application
                                                  server

  `DEBUG`                 May be enabled on       Disable
                          localhost               

  Secret key              Temporary local-only    Secure, unique secret
                          value                   supplied outside the
                                                  image

  `ALLOWED_HOSTS`         Local test hosts        Explicit approved
                                                  hostnames

  Database                SQLite may be           Select, secure, back
                          sufficient for a tiny   up, and monitor an
                          demo                    appropriate database

  Static files            Simple development      Collect and serve
                          behavior                static files using an
                                                  intentional strategy

  HTTPS                   Not required for an     Configure TLS, secure
                          isolated localhost demo cookies, proxy headers,
                                                  and relevant Django
                                                  security settings

  Process management      One simple container    Health monitoring,
                                                  graceful shutdown,
                                                  restart/recovery plan

  Dependencies            Demonstration version   Tested, reviewed,
                          ranges                  pinned/locked
                                                  dependencies

  Secrets                 Never commit real       Use managed secrets or
                          secrets                 a secure deployment
                                                  mechanism

  Scaling                 One container           Define replicas, load
                                                  balancing, state
                                                  management and
                                                  observability as needed
  -----------------------------------------------------------------------

A container image makes the application artifact more repeatable; it
does not automatically make Django production-ready.

## 14. Security and reliability checklist

Before any public deployment, review:

-   [ ] `DEBUG=False`.
-   [ ] A strong, unique `DJANGO_SECRET_KEY` is supplied securely.
-   [ ] `ALLOWED_HOSTS` contains only intended hostnames/IPs.
-   [ ] Database credentials and other secrets are not in the image or
    Git.
-   [ ] Dependencies are reviewed and kept up to date.
-   [ ] The app runs as a non-root user where practical.
-   [ ] Only required ports are published.
-   [ ] AWS inbound rules use minimal source ranges.
-   [ ] HTTPS and Django's production security settings are configured.
-   [ ] Database and uploaded media persistence are designed separately
    from the container's writable layer.
-   [ ] Logs, monitoring, health checks, backups, and recovery are
    addressed.
-   [ ] The image and base-image vulnerabilities are assessed.

See the official Django deployment checklist before moving a Django
application to production.

## 15. Hands-on exercises

### Exercise A --- Basic containerization

-   [ ] Create the project files from this guide.
-   [ ] Build `django-demo:1.0`.
-   [ ] Run it with `-p 8000:8000`.
-   [ ] Verify the JSON response with `curl`.
-   [ ] Capture `docker ps`, `docker logs`, and `docker inspect` output.
-   [ ] Explain why `EXPOSE 8000` alone does not publish a port.

### Exercise B --- Host validation

-   [ ] Run with `DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1`.
-   [ ] Test with `curl http://localhost:8000/`.
-   [ ] Change the `Host` header to an unapproved value and observe
    Django's response.
-   [ ] Add only the intended lab hostname and retest.

### Exercise C --- CMD and ENTRYPOINT

Create two tiny images: one using only `CMD`, and another using
exec-form `ENTRYPOINT` plus default `CMD` arguments. Override the
command after the image name and compare the resulting
process/arguments.

### Exercise D --- EC2 network debugging

-   [ ] Test the application with `curl` on EC2.
-   [ ] Confirm the container publishes host port 8000.
-   [ ] Confirm the app binds to `0.0.0.0:8000` inside the container.
-   [ ] Restrict inbound TCP/8000 to your IP.
-   [ ] Test the public DNS address from your own computer.
-   [ ] Remove the temporary security-group rule when finished.

### Exercise E --- Production readiness review

List what would need to change before serving real users: secrets,
`DEBUG`, allowed hosts, TLS, database, static files, non-root execution,
image scanning, logging, monitoring, backups, and recovery.

## 16. Interview questions and answers

**1. What is Django?**\
Django is a Python web framework that provides components for URL
routing, request handling, templates, models, authentication, and other
web-application needs.

**2. What is `settings.py` used for?**\
It holds project configuration such as installed apps, middleware,
database settings, host validation, secret key, debug mode, and
static-file settings.

**3. What is the role of `urls.py`?**\
It maps URL patterns to view functions or class-based views.

**4. What does `views.py` do?**\
It contains request-handling logic that returns responses, renders
templates, or coordinates application work.

**5. Why containerize a Django application?**\
To package the application and its user-space dependencies into a
repeatable image and reduce environment differences across compatible
deployment hosts.

**6. Why should the app listen on `0.0.0.0` inside a container?**\
Binding to `0.0.0.0` allows the server to listen on the container's IPv4
interfaces, so traffic routed through Docker's published port can reach
it.

**7. What does `-p 8000:8000` mean?**\
It publishes host port 8000 and forwards traffic to port 8000 inside the
container.

**8. Does `EXPOSE 8000` publish a port?**\
No. It documents the intended container port. Publishing is configured
at runtime, for example with `-p`.

**9. What is the difference between `CMD` and `ENTRYPOINT`?**\
`CMD` provides a default command or default arguments. `ENTRYPOINT`
defines the main executable; with exec form, extra arguments supplied to
`docker run` are appended to it.

**10. Why is exec form recommended?**\
It avoids an extra shell in common cases and provides more predictable
argument handling and signal delivery.

**11. Why not use Django's `runserver` in production?**\
It is intended for development and is not a production application
server. Use a suitable WSGI/ASGI server and production deployment
configuration.

**12. What does `ALLOWED_HOSTS` protect?**\
It restricts which host header values Django accepts, helping defend
against certain host-header attacks and misconfiguration.

**13. What is the purpose of `.dockerignore`?**\
It prevents unnecessary or sensitive files from entering the build
context.

**14. Why copy `requirements.txt` before application code?**\
It allows Docker to reuse the dependency-installation build step when
application source changes but dependencies do not.

**15. Why might an EC2-hosted container work locally but not from a
browser?**\
The application may bind incorrectly, the port may not be published, the
EC2 security group or network path may block traffic, or Django may
reject the requested host.

**16. Does Docker port mapping configure the AWS security group?**\
No. Docker port mapping and AWS security-group rules are independent
configuration layers.

**17. What happens if the Django container is deleted?**\
The container instance is removed. The image may remain locally, but
data stored only in the container's writable layer can be lost.

**18. Where should a Django secret key be stored?**\
Outside source control and the image, supplied through a secure runtime
configuration or secrets-management mechanism.

**19. Does containerization automatically make the app scalable?**\
No. Containers provide a packaging unit. Scaling requires a deployment
strategy, resource capacity, routing/load balancing, state management,
and monitoring.

**20. What is Gunicorn?**\
Gunicorn is a WSGI HTTP server commonly used to serve Python web
applications such as Django. ASGI applications may require an
ASGI-compatible server.

## 17. What belongs in later notes

Keep these topics separate so the playlist stays useful and avoids
repetition:

  --------------------------------------------------------------------------------------
  Future note                                        New scope
  -------------------------------------------------- -----------------------------------
  `04-dockerfiles-and-multistage-builds/README.md`   Build cache, multi-stage builds,
                                                     smaller runtime images, BuildKit,
                                                     dependency and image optimization

  `05-docker-storage/README.md`                      Volumes, bind mounts, persistent
                                                     database/media data, backup and
                                                     restore

  `06-docker-networking/README.md`                   Bridge networks, port mapping, DNS,
                                                     inter-container connectivity and
                                                     troubleshooting

  `07-docker-compose/README.md`                      Multi-service Django + database
                                                     stacks, service dependencies,
                                                     environment configuration

  `08-django-production-deployment/README.md`        Gunicorn/ASGI, reverse proxy, TLS,
                                                     static files, migrations, database,
                                                     health checks and deployment
                                                     strategies
  --------------------------------------------------------------------------------------

For the next Docker networking video, focus on network behavior and
connectivity. Do not copy this Django application tutorial into that
note; link to it as an example workload instead.

## 18. References

### Video and course

-   [Abhishek Veeramalla --- Containerize a Django Web Application with
    Docker](https://www.youtube.com/watch?v=3IAvr_O6vao)
-   [DevOps Zero to Hero
    playlist](https://www.youtube.com/playlist?list=PLdpzxOOAlwvIc1TjTwopNSjRJkzES2ZXk)
-   [Previous note: Docker
    fundamentals](../02-docker-fundamentals/README.md)

### Official documentation

-   [Django documentation](https://docs.djangoproject.com/en/stable/)
-   [Django deployment
    checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
-   [Django
    settings](https://docs.djangoproject.com/en/stable/topics/settings/)
-   [Django URL
    dispatcher](https://docs.djangoproject.com/en/stable/topics/http/urls/)
-   [Dockerfile
    reference](https://docs.docker.com/reference/dockerfile/)
-   [Docker port
    publishing](https://docs.docker.com/engine/network/port-publishing/)
-   [Docker build best
    practices](https://docs.docker.com/build/building/best-practices/)
-   [Gunicorn documentation](https://docs.gunicorn.org/en/stable/)
-   [AWS EC2 security group
    rules](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/security-group-rules.html)

------------------------------------------------------------------------

## Attribution and update note

These are original study notes based on the video's subject and
supplementary official documentation, not a verbatim transcript.
Framework versions, base images, and deployment recommendations change
over time; consult the official documentation before using this example
for a public or production deployment.

**Suggested commit message:**
`docs: add Django Docker containerization lab`
