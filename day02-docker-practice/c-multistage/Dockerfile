# ==========================================
# STAGE 1: Compilation Environment (Heavy)
# ==========================================
FROM alpine:3.19 AS builder

# Install C compiler and standard build tools
RUN apk add --no-cache gcc musl-dev

WORKDIR /build

# Copy source code and compile statically
COPY hello.c .
RUN gcc -O2 -static -o hello hello.c

# ==========================================
# STAGE 2: Production Runtime (Ultra-Light)
# ==========================================
FROM alpine:3.19

LABEL maintainer="student@cdac.in"
LABEL type="optimized-c-binary"

WORKDIR /app

# Copy ONLY the compiled binary from Stage 1
COPY --from=builder /build/hello /app/hello

# Execute the binary
CMD ["/app/hello"]
