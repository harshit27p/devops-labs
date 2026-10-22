FROM alpine:3.19

# 1. Create a dedicated non-root group and user (appuser with UID 10001)
RUN addgroup -g 10001 appgroup && \
    adduser -u 10001 -G appgroup -s /bin/sh -D appuser

# 2. Set working directory and grant ownership to appuser
WORKDIR /home/appuser/app
RUN chown -R appuser:appgroup /home/appuser/app

# 3. Switch to non-root user
USER appuser

# 4. Command to inspect running user identity
CMD ["whoami"]
