# Multi-Stage Docker Builds & Distroless Images

> **Video:** [Day-26 --- Multi-Stage Docker Builds and Distroless Images
> \| Abhishek Veeramalla](https://www.youtube.com/watch?v=yyJrZgoNal0)\
> **Playlist:** [DevOps Zero to
> Hero](https://www.youtube.com/playlist?list=PLdpzxOOAlwvIc1TjTwopNSjRJkzES2ZXk)\
> **Suggested path:** `04-multistage-distroless/README.md`\
> **Prerequisites:** Basic Go syntax and the Docker fundamentals in
> [`02-docker-fundamentals`](../02-docker-fundamentals/README.md).

These notes expand the video's Go calculator demonstration with
reproducible examples, size comparison commands, security trade-offs,
troubleshooting, and links to official documentation. The aim is to
learn how to separate the build environment from the runtime image
without repeating the full Docker introduction.

> **Important terminology:** `scratch` is Docker's special empty base
> image, not a general-purpose Linux distribution. Distroless images are
> separately maintained minimal runtime images (for example, Google's
> distroless images) that include selected runtime dependencies but omit
> shells and package managers. Both approaches can produce minimal
> images, but they are not the same thing.

------------------------------------------------------------------------

## Table of contents

-   [1. Learning objectives](#1-learning-objectives)
-   [2. Why optimize container
    images?](#2-why-optimize-container-images)
-   [3. What is a multi-stage build?](#3-what-is-a-multi-stage-build)
-   [4. What are distroless images?](#4-what-are-distroless-images)
-   [5. Go calculator project](#5-go-calculator-project)
-   [6. Baseline: single-stage
    Dockerfile](#6-baseline-single-stage-dockerfile)
-   [7. Optimized: multi-stage build using
    scratch](#7-optimized-multi-stage-build-using-scratch)
-   [8. Alternative: use a distroless runtime
    image](#8-alternative-use-a-distroless-runtime-image)
-   [9. Build and compare image sizes](#9-build-and-compare-image-sizes)
-   [10. Static vs dynamic linking and CA
    certificates](#10-static-vs-dynamic-linking-and-ca-certificates)
-   [11. How to choose the final base
    image](#11-how-to-choose-the-final-base-image)
-   [12. Security benefits and
    limitations](#12-security-benefits-and-limitations)
-   [13. Troubleshooting minimal
    images](#13-troubleshooting-minimal-images)
-   [14. Practical lab and challenge
    tasks](#14-practical-lab-and-challenge-tasks)
-   [15. Interview questions and
    answers](#15-interview-questions-and-answers)
-   [16. What belongs in later notes](#16-what-belongs-in-later-notes)
-   [17. References](#17-references)

------------------------------------------------------------------------

## 1. Learning objectives

After completing this guide, you should be able to:

1.  Explain why compilers, source code, and build tools usually do not
    belong in a production runtime image.
2.  Write a Dockerfile with named build and runtime stages.
3.  Copy only the required compiled artifact from one stage to another
    using `COPY --from`.
4.  Build a Go executable suitable for a minimal Linux runtime.
5.  Compare a single-stage image with a multi-stage `scratch` or
    distroless image.
6.  Understand the operational trade-offs of images without a shell or
    package manager.
7.  Use image-size and inspection commands to verify results rather than
    assume a particular size.
8.  Explain why smaller images can reduce attack surface but do not
    automatically guarantee security.

## 2. Why optimize container images?

A development environment may contain much more than the application
needs to run:

-   Compiler and language toolchain
-   Source code and build scripts
-   Package manager and package indexes
-   Test tools and debugging utilities
-   Development libraries and headers
-   Temporary build artifacts

If all of these are retained in the final image, the image may be much
larger than the actual runtime needs.

### Why image size matters

Smaller, appropriately constructed images can:

-   Reduce download and distribution time.
-   Reduce registry storage and transfer costs.
-   Shorten some deployment and scaling operations.
-   Reduce the number of installed packages that need patching.
-   Make vulnerability scan results easier to review.
-   Limit the tools available to an attacker if an application is
    compromised.

**Size is not the only goal.** Runtime compatibility, patchability,
reproducibility, observability, and security matter too. A tiny image
that cannot run reliably or cannot be updated safely is not a good
production image.

### The main principle

> Build with everything needed to compile and test; run with only what
> is required to execute the application.

Docker recommends multi-stage builds to separate build-time dependencies
from the final runtime image. See [Docker's multi-stage build
documentation](https://docs.docker.com/build/building/multi-stage/).

## 3. What is a multi-stage build?

A multi-stage Dockerfile contains multiple `FROM` instructions. Each
starts a new build stage. Stages can use different base images and serve
different purposes.

``` text
Source code
    |
    v
┌────────────────────────────┐
│ Build stage                │
│ Compiler + source + tools  │
│ go build                   │
└─────────────┬──────────────┘
              |
              | COPY --from=builder
              v
┌────────────────────────────┐
│ Final runtime stage        │
│ Only runtime artifact      │
│ + required runtime files   │
└─────────────┬──────────────┘
              |
              v
        Production container
```

### Key Dockerfile syntax

``` dockerfile
FROM golang:1.24 AS builder
# build instructions

FROM scratch AS runtime
COPY --from=builder /path/to/app /app
ENTRYPOINT ["/app"]
```

-   `FROM ... AS builder` names the build stage.
-   A later `FROM` starts a fresh stage.
-   `COPY --from=builder` copies selected files from the named stage.
-   By default, Docker builds the last stage as the final image.
-   `--target builder` can be used when you intentionally want to build
    an intermediate stage.

The specific Go image tag in examples should be checked against the
version supported by your project and official image publisher.

### What multi-stage builds do not do

They do not automatically make every application tiny. The final image
still needs its runtime, shared libraries, certificates, locale data,
application assets, and other required files. The amount saved depends
on the build toolchain, application, base image, and runtime
requirements.

## 4. What are distroless images?

Distroless images contain an application and its required runtime
dependencies without the usual collection of tools included in a
general-purpose Linux distribution. Google's distroless project
describes its images as omitting package managers, shells, and other
standard distribution utilities.

### Common properties

-   No package manager for installing tools at container startup.
-   Usually no shell such as `/bin/sh`.
-   Minimal set of runtime libraries and files.
-   Often designed around a language/runtime family or application type.
-   Can support a non-root user, depending on the selected image.

### Why teams use them

A reduced runtime environment can lower the number of packages and
utilities included in production. This may reduce the attack surface and
improve the signal-to-noise ratio of vulnerability scans.

### Important limitations

-   You cannot assume `sh`, `bash`, `curl`, `find`, or `ls` exists.
-   Debugging generally requires application logs, metrics, process
    inspection from the host/runtime, or a separate debug image.
-   Native binaries may need shared libraries not included in the chosen
    image.
-   Certificates, timezone data, or other files may be needed depending
    on the application's behavior.
-   A minimal image still needs to be updated and scanned.
-   A vulnerability in the application or a bundled runtime dependency
    can still be exploitable.

### `scratch` vs distroless

  -----------------------------------------------------------------------
  Feature                 `scratch`               Distroless runtime
                                                  image
  ----------------------- ----------------------- -----------------------
  Base contents           Empty starting point    Selected runtime files
                                                  and dependencies

  Shell/package manager   None by default         Usually none

  Shared libraries        Must be supplied if     Selected libraries may
                          required                be included

  Best fit                Suitable self-contained Applications that need
                          binaries, commonly      a minimal but curated
                          static Go binaries      runtime environment

  Setup effort            Higher; author must     Often easier when an
                          identify every required appropriate
                          file                    language/runtime image
                                                  exists

  Debugging               Very limited inside the Also intentionally
                          image                   limited
  -----------------------------------------------------------------------

Do not call `scratch` a distroless distribution: it is an empty base
image. Both can be used for minimal runtime images, but the file
contents and assumptions differ.

## 5. Go calculator project

This lab uses a tiny Go calculator CLI application. It reads two numbers
and an operator from environment variables, calculates the result, and
prints it. This avoids interactive input so the container can be tested
with simple repeatable commands.

### Step 1 --- Create the project directory

``` bash
mkdir -p go-calculator
cd go-calculator
```

### Step 2 --- Create `go.mod`

``` go
module example.com/go-calculator

go 1.24
```

The Go version declaration should be compatible with the installed
compiler and the selected builder image. If you choose a newer supported
Go toolchain, update both consistently.

### Step 3 --- Create `main.go`

``` go
package main

import (
    "fmt"
    "os"
    "strconv"
)

func main() {
    aText := os.Getenv("NUM_A")
    bText := os.Getenv("NUM_B")
    op := os.Getenv("OP")

    if aText == "" || bText == "" || op == "" {
        fmt.Fprintln(os.Stderr, "Set NUM_A, NUM_B, and OP (+, -, *, /)")
        os.Exit(2)
    }

    a, err := strconv.ParseFloat(aText, 64)
    if err != nil {
        fmt.Fprintln(os.Stderr, "NUM_A must be a number")
        os.Exit(2)
    }

    b, err := strconv.ParseFloat(bText, 64)
    if err != nil {
        fmt.Fprintln(os.Stderr, "NUM_B must be a number")
        os.Exit(2)
    }

    var result float64
    switch op {
    case "+":
        result = a + b
    case "-":
        result = a - b
    case "*":
        result = a * b
    case "/":
        if b == 0 {
            fmt.Fprintln(os.Stderr, "division by zero")
            os.Exit(2)
        }
        result = a / b
    default:
        fmt.Fprintln(os.Stderr, "OP must be one of +, -, *, /")
        os.Exit(2)
    }

    fmt.Printf("%.4g %s %.4g = %.4g\n", a, op, b, result)
}
```

### Step 4 --- Test locally, if Go is installed

``` bash
NUM_A=12 NUM_B=3 OP=/ go run .
```

Expected output:

``` text
12 / 3 = 4
```

Other examples:

``` bash
NUM_A=8 NUM_B=5 OP=+ go run .
NUM_A=8 NUM_B=5 OP=- go run .
NUM_A=8 NUM_B=5 OP='*' go run .
```

## 6. Baseline: single-stage Dockerfile

Create `Dockerfile.single`:

``` dockerfile
FROM golang:1.24

WORKDIR /src

COPY go.mod ./
COPY main.go ./

RUN go build -o /usr/local/bin/calculator .

ENTRYPOINT ["/usr/local/bin/calculator"]
```

This builds the app but uses the full Go image as the runtime image. The
compiler and other tools remain in the image even though the calculator
does not need them to execute.

Build and run:

``` bash
docker build -f Dockerfile.single -t go-calculator:single .
docker run --rm -e NUM_A=12 -e NUM_B=3 -e OP=/ go-calculator:single
```

Inspect the image size:

``` bash
docker image ls go-calculator
docker image inspect go-calculator:single
```

The size will vary with the selected Go image version, architecture,
platform, and Docker build environment. Do not expect the exact image
size quoted in a video.

## 7. Optimized: multi-stage build using scratch

Create `Dockerfile.scratch`:

``` dockerfile
# syntax=docker/dockerfile:1

FROM golang:1.24 AS builder

WORKDIR /src

COPY go.mod ./
COPY main.go ./

# Build a Linux executable with no CGO dependency for this example.
RUN CGO_ENABLED=0 GOOS=linux go build \
    -trimpath \
    -ldflags="-s -w" \
    -o /out/calculator .

FROM scratch AS runtime

COPY --from=builder /out/calculator /calculator

USER 65532:65532

ENTRYPOINT ["/calculator"]
```

### Why this works

-   The builder image includes the Go compiler and build tools.
-   `CGO_ENABLED=0` disables CGO for this example, making a
    self-contained static-style executable feasible.
-   `GOOS=linux` targets Linux.
-   `-trimpath` removes local filesystem paths from build metadata where
    applicable.
-   `-ldflags="-s -w"` strips symbol/debug information, which can reduce
    binary size but makes some debugging less convenient.
-   The final stage starts from `scratch`, an empty base image.
-   Only the compiled binary is copied from the builder.
-   `USER 65532:65532` configures a non-root numeric UID/GID, provided
    the application does not need files or privileges it cannot access.
-   `ENTRYPOINT` runs the binary directly without requiring a shell.

Build and run:

``` bash
docker build -f Dockerfile.scratch -t go-calculator:scratch .
docker run --rm -e NUM_A=12 -e NUM_B=3 -e OP=/ go-calculator:scratch
```

Test error handling:

``` bash
docker run --rm -e NUM_A=5 -e NUM_B=0 -e OP=/ go-calculator:scratch
```

The division-by-zero case should print an error and exit with a non-zero
status.

### Why `scratch` is not right for every application

This example deliberately avoids CGO and external runtime files. A Go
program that uses CGO, requires shared libraries, loads
templates/certificates from the filesystem, or depends on other runtime
assets may fail in `scratch` unless those dependencies are supplied
correctly.

For multi-architecture builds, ensure the builder target and output
architecture match the intended runtime platform.

## 8. Alternative: use a distroless runtime image

An alternative final stage uses a curated minimal runtime image instead
of an empty filesystem.

Create `Dockerfile.distroless`:

``` dockerfile
# syntax=docker/dockerfile:1

FROM golang:1.24 AS builder

WORKDIR /src

COPY go.mod ./
COPY main.go ./

RUN CGO_ENABLED=0 GOOS=linux go build \
    -trimpath \
    -ldflags="-s -w" \
    -o /out/calculator .

FROM gcr.io/distroless/static-debian12:nonroot AS runtime

COPY --from=builder /out/calculator /calculator

ENTRYPOINT ["/calculator"]
```

This example uses Google's `static-debian12:nonroot` image. Check the
project's current supported tags and recommendations before using it in
a real pipeline. Image availability and naming may change over time.

Build and run:

``` bash
docker build -f Dockerfile.distroless -t go-calculator:distroless .
docker run --rm -e NUM_A=12 -e NUM_B=3 -e OP=/ go-calculator:distroless
```

The chosen distroless image supplies a curated minimal runtime base and
a non-root user configuration. The binary is still built separately and
copied into the runtime stage.

### Which one should you choose?

-   Choose `scratch` when you can verify the executable is
    self-contained and you are prepared to include any required files
    manually.
-   Choose a suitable distroless image when you want a curated minimal
    runtime environment with relevant runtime components already
    included.
-   Choose a slim general-purpose runtime image when operational
    tooling, shared libraries, or compatibility needs justify the
    additional contents.

Never choose solely by image size. Verify runtime behavior and
vulnerability/maintenance requirements.

## 9. Build and compare image sizes

Build all three variants:

``` bash
docker build -f Dockerfile.single -t go-calculator:single .
docker build -f Dockerfile.scratch -t go-calculator:scratch .
docker build -f Dockerfile.distroless -t go-calculator:distroless .
```

List the sizes:

``` bash
docker image ls go-calculator
```

Or inspect each image's reported size:

``` bash
docker image inspect go-calculator:single \
  --format='{{.RepoTags}} {{.Size}} bytes'

docker image inspect go-calculator:scratch \
  --format='{{.RepoTags}} {{.Size}} bytes'

docker image inspect go-calculator:distroless \
  --format='{{.RepoTags}} {{.Size}} bytes'
```

### How to interpret the results

The single-stage image should generally be much larger because it
retains the Go toolchain. The `scratch` and distroless variants should
generally be much smaller for this simple binary, but exact results
vary.

The video reports an example reduction from roughly 861 MB to 1.83 MB.
Treat those figures as results from that particular build and
environment, not universal guarantees.

### Calculate percentage reduction

If you record image sizes (S\_{`\text{before}`{=tex}}) and
(S\_{`\text{after}`{=tex}}), the percentage reduction is:

\[ `\text{Reduction (\%)}`{=tex} =
`\frac{S_{\text{before}} - S_{\text{after}}}{S_{\text{before}}}`{=tex}
`\times 100`{=tex} \]

Example only: if an image drops from 800 MB to 20 MB, the reduction is
97.5%. Use your own measured values for the actual lab report.

### Image size is not the same as disk usage

Docker image listings show image size in a particular representation.
Images may share layers, and actual disk use can differ from the sum of
displayed image sizes. Registry transfer size can also differ because
layers may be compressed.

For a fair comparison: - Use the same source code and build target. -
Record the platform and base-image versions. - Compare the image
IDs/tags and image sizes. - Run the same functional tests against every
variant. - Record build time separately from final image size.

## 10. Static vs dynamic linking and CA certificates

### Static and dynamic linking

A dynamically linked binary expects certain shared libraries to be
present at runtime. A statically linked or self-contained binary carries
more of what it needs within the executable, depending on the language
and build configuration.

For Go: - `CGO_ENABLED=0` can produce a self-contained binary for many
pure-Go applications. - CGO-dependent programs may require a C toolchain
during build and compatible shared libraries at runtime. - Static
compilation is not automatically possible or appropriate for every
dependency and target.

Check the output file on a suitable Linux environment:

``` bash
file ./calculator
```

This command requires the `file` utility on the machine where you run
it; it is not available inside a `scratch` container.

### Certificates and other files

An empty `scratch` image has no CA certificate bundle by default. If
your application makes outbound HTTPS requests, it may need a trusted CA
certificate bundle copied into the image. Other applications may require
timezone data, templates, locale files, or configuration.

Do not copy arbitrary files blindly. Identify runtime requirements and
include only what the application actually needs.

## 11. How to choose the final base image

  -----------------------------------------------------------------------
  Runtime base            Advantages              Trade-offs
  ----------------------- ----------------------- -----------------------
  Full language image     Convenient, familiar,   Larger, more packages,
                          includes toolchain and  larger maintenance
                          utilities               surface

  Slim runtime image      Smaller than full image Still contains
                          while retaining common  distribution packages
                          OS runtime features     and may need patching

  Alpine-based image      Often small; useful in  Musl vs glibc
                          compatible environments compatibility and
                                                  package/runtime
                                                  differences can require
                                                  care

  Distroless              Minimal curated         Debugging and
                          runtime, no general     operational tasks
                          shell/package manager   require external tools;
                                                  runtime compatibility
                                                  must be verified

  `scratch`               Empty base, excellent   You must provide every
                          for appropriate         needed runtime file; no
                          self-contained binaries shell, certificates, or
                                                  OS utilities by default
  -----------------------------------------------------------------------

A minimal image is an outcome of good dependency analysis, not just a
Dockerfile trick. A smaller base can also reduce vulnerability exposure,
but you must continue updating the base image and application.

## 12. Security benefits and limitations

### Potential benefits

-   Fewer packages and binaries in the runtime image.
-   Smaller attack surface when unnecessary tools and libraries are
    absent.
-   Less image content to scan and maintain.
-   Clear separation between build-time tools and runtime artifacts.
-   Easier inspection of exactly what is copied into the final stage.

### What it does not guarantee

-   The application itself may still contain vulnerabilities.
-   The final binary may include vulnerable dependencies.
-   The builder can still be compromised or pull malicious dependencies.
-   Incorrect permissions, secrets, capabilities, or network exposure
    remain risks.
-   An old minimal base image can still contain vulnerable components.
-   A small image can be harder to debug if the operational process is
    not designed for it.

### Practical hardening checklist

-   [ ] Use a trusted and maintained builder and runtime image.
-   [ ] Keep the build and runtime stages separate.
-   [ ] Copy only required artifacts into the final stage.
-   [ ] Run as non-root where practical.
-   [ ] Do not embed credentials or tokens in the image.
-   [ ] Pin and review dependencies; record image digests for releases.
-   [ ] Scan the image and dependencies.
-   [ ] Rebuild periodically to receive base-image and dependency
    updates.
-   [ ] Test the actual runtime image, not only the builder stage.
-   [ ] Capture logs and metrics externally rather than relying on a
    shell in the container.
-   [ ] Keep a documented debugging workflow or separate debug build.
-   [ ] Verify required certificates, libraries, assets, and
    permissions.

## 13. Troubleshooting minimal images

  -----------------------------------------------------------------------------
  Symptom                       Likely cause            Suggested check
  ----------------------------- ----------------------- -----------------------
  `exec format error`           Binary built for the    Check target platform
                                wrong OS or CPU         and build settings;
                                architecture            inspect the binary on a
                                                        compatible host.

  `no such file or directory`   Missing dynamic loader  Check linkage with
  when executing a binary that  or incompatible runtime host-side tools such as
  appears present               dependencies            `file` and `ldd` where
                                                        appropriate; inspect
                                                        the chosen base image.

  HTTPS requests fail in        No CA certificate       Identify the app's
  `scratch`                     bundle or missing trust certificate
                                configuration           requirements and copy a
                                                        trusted bundle
                                                        deliberately.

  Cannot run `sh` or `ls`       Expected behavior for   Use application logs
  inside the container          `scratch`/distroless    and host/runtime
                                                        inspection; do not
                                                        assume a shell exists.

  Container exits immediately   The calculator is a     Check `docker ps -a`
                                one-shot CLI process    and `docker logs`; an
                                                        exited state is normal
                                                        after output.

  Binary reports permission     Incorrect executable    Check the artifact mode
  denied                        permissions or runtime  during build and the
                                restrictions            configured user.

  Binary needs a shared library CGO/dynamic dependency  Use a compatible
                                not included in final   runtime base or provide
                                stage                   the required library
                                                        deliberately.

  Final image is still large    Build stage             Check the last stage,
                                accidentally selected,  `--target`, image
                                large runtime           history, and `COPY`
                                dependencies, or extra  statements.
                                files copied            

  Unexpected vulnerability      Application dependency  Review scanner output,
  findings                      or base-image issues    update
                                                        dependencies/base
                                                        image, and rebuild.
  -----------------------------------------------------------------------------

### Useful host-side commands

``` bash
docker ps -a
docker logs CONTAINER_NAME
docker inspect IMAGE_OR_CONTAINER
docker image history go-calculator:scratch
docker image ls go-calculator
```

Minimal runtime images often lack tools required to diagnose themselves.
Use the Docker host, orchestrator, application telemetry, or a separate
debug image to inspect the process.

## 14. Practical lab and challenge tasks

### Task A --- Build and compare

-   [ ] Create the calculator source and module file.
-   [ ] Build the single-stage image.
-   [ ] Build the `scratch` multi-stage image.
-   [ ] Build the distroless multi-stage image.
-   [ ] Record each image size, build duration, and successful test
    output.
-   [ ] Explain why the compiler is absent from the final stage.

### Task B --- Test correctness

For each image, run:

``` bash
docker run --rm -e NUM_A=10 -e NUM_B=2 -e OP=+ go-calculator:scratch
docker run --rm -e NUM_A=10 -e NUM_B=2 -e OP=- go-calculator:scratch
docker run --rm -e NUM_A=10 -e NUM_B=2 -e OP='*' go-calculator:scratch
docker run --rm -e NUM_A=10 -e NUM_B=2 -e OP=/ go-calculator:scratch
```

Repeat using the `single` and `distroless` tags.

### Task C --- Failure scenarios

-   [ ] Run without required environment variables.
-   [ ] Test an invalid number.
-   [ ] Test division by zero.
-   [ ] Attempt to open a shell in the `scratch` container and explain
    why it fails.
-   [ ] Describe how you would investigate a missing shared library
    without adding tools to the production image.

### Task D --- Experiment with build flags

Build with and without `-ldflags="-s -w"`. Compare the binary and image
sizes, then explain the debugging trade-off. Do not assume symbol
stripping always produces a large reduction.

### Task E --- Write a short lab report

Include: 1. Purpose and architecture diagram. 2. Source code and the
three Dockerfiles. 3. Build commands and image-size measurements. 4.
Functional test outputs. 5. Security and operational trade-offs. 6.
Conclusion on which runtime base you would choose and why.

## 15. Interview questions and answers

**1. What is a multi-stage Docker build?**\
A Dockerfile pattern using multiple `FROM` stages so the build
environment can be separated from the final runtime image.

**2. Why are multi-stage builds useful?**\
They let the final image contain only the application artifacts and
runtime dependencies needed to execute the app, rather than the complete
build toolchain.

**3. What does `COPY --from=builder` do?**\
It copies files from a named earlier build stage into the current stage.

**4. What is `scratch`?**\
Docker's special empty base image. It has no normal Linux distribution
files, shell, package manager, or certificate bundle by default.

**5. Are `scratch` and distroless the same?**\
No. `scratch` is empty; distroless images contain a curated minimal set
of runtime files and dependencies.

**6. What is a distroless image?**\
A minimal runtime image that excludes general-purpose package managers,
shells, and many utilities not required to run the application.

**7. Why does a Go application often work well with `scratch`?**\
Many pure-Go applications can be built as self-contained Linux
executables, so the runtime may need little beyond the binary itself.

**8. Does every Go application work in `scratch`?**\
No. CGO, dynamic libraries, CA certificates, timezone data, external
assets, and other runtime requirements may need to be included.

**9. Why is image size important?**\
It affects distribution, storage, deployment efficiency, and can
correlate with the amount of software that must be maintained and
scanned.

**10. Does a smaller image guarantee greater security?**\
No. It can reduce unnecessary components and attack surface, but the
application, dependencies, build pipeline, permissions, and base image
still require security controls.

**11. What is the difference between build-time and runtime
dependencies?**\
Build-time dependencies compile, test, or package the application.
Runtime dependencies are needed when the final application executes.

**12. Why use a non-root user in the final image?**\
It reduces privileges available to the application if it is compromised,
assuming the application does not require root and file permissions are
configured correctly.

**13. Why might `docker exec -it container sh` fail in a distroless
image?**\
There may be no shell installed. Use logs, host/runtime inspection, or a
separate debug image.

**14. What is the purpose of `CGO_ENABLED=0` in the Go example?**\
It disables CGO so a pure-Go program can often be built without relying
on C shared libraries at runtime.

**15. Why might an HTTPS request fail in a `scratch` image?**\
The empty image has no CA certificate bundle by default, so certificate
verification may not have the trust roots required.

**16. What does `-ldflags="-s -w"` do?**\
It strips symbol-table and DWARF debug information from a Go binary,
which can reduce size but may make debugging harder.

**17. Does Docker build every stage into the final image?**\
No. The final image is based on the selected target stage, normally the
last stage. Artifacts must be copied into it explicitly.

**18. How can you compare image sizes?**\
Use `docker image ls` or `docker image inspect`, and compare builds made
from the same source and platform.

**19. Why should the final image be tested independently?**\
The final runtime environment may be missing libraries, certificates,
files, or permissions that existed in the builder.

**20. What is the trade-off of distroless images?**\
They can reduce runtime contents and attack surface, but make
interactive debugging and on-container maintenance harder; operations
should rely on observability and reproducible rebuilds.

## 16. What belongs in later notes

Keep related subjects separate to preserve the playlist's structure:

  -----------------------------------------------------------------------------
  Future note                               Focus
  ----------------------------------------- -----------------------------------
  `05-docker-storage/README.md`             Volumes, bind mounts, persistence
                                            and backups

  `06-docker-networking/README.md`          Networks, DNS, port publishing and
                                            connectivity

  `07-docker-compose/README.md`             Multi-container application
                                            configuration

  `08-container-security/README.md`         Image scanning, SBOMs, signing,
                                            provenance, secrets and runtime
                                            hardening

  `09-ci-cd-container-pipeline/README.md`   Build/test/scan/publish stages,
                                            artifact promotion, versioning and
                                            rollback
  -----------------------------------------------------------------------------

The multi-stage build technique should be referenced in later Dockerfile
notes rather than fully repeated. In future language-specific examples,
compare the runtime requirements of the application instead of assuming
every language can use `scratch`.

## 17. References

### Video and playlist

-   [Abhishek Veeramalla --- Multi-Stage Docker Builds and Distroless
    Images](https://www.youtube.com/watch?v=yyJrZgoNal0)
-   [DevOps Zero to Hero
    playlist](https://www.youtube.com/playlist?list=PLdpzxOOAlwvIc1TjTwopNSjRJkzES2ZXk)
-   [Previous note: Docker
    fundamentals](../02-docker-fundamentals/README.md)

### Official documentation and projects

-   [Docker: Multi-stage
    builds](https://docs.docker.com/build/building/multi-stage/)
-   [Docker: Multi-stage builds --- getting
    started](https://docs.docker.com/get-started/docker-concepts/building-images/multi-stage-builds/)
-   [Docker: Build best
    practices](https://docs.docker.com/build/building/best-practices/)
-   [Docker: Go language guide](https://docs.docker.com/guides/golang/)
-   [GoogleContainerTools/distroless](https://github.com/GoogleContainerTools/distroless)
-   [Go documentation](https://go.dev/doc/)
-   [Go compiler command reference](https://pkg.go.dev/cmd/compile)
-   [Dockerfile
    reference](https://docs.docker.com/reference/dockerfile/)

------------------------------------------------------------------------

## Attribution and update note

These are original study notes based on the video's subject and
supplementary official documentation, not a verbatim transcript. Image
tags, Go versions, and runtime recommendations change; check the
official documentation and test the final image on the target
architecture before deployment.

**Suggested commit message:**
`docs: add multi-stage and distroless Docker build notes`
