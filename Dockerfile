FROM python:3.12-alpine

LABEL maintainer="Himangshu Pan <researchersheru@gmail.com>"
LABEL description="Loggen - SOC analyst training log generator"

# Install build dependencies (needed for pydantic-core and other compiled packages)
RUN apk add --no-cache --virtual .build-deps \
        gcc \
        musl-dev \
        libffi-dev \
        cargo \
        rust \
    && apk add --no-cache bash

WORKDIR /app

# Copy project files
COPY pyproject.toml README.md ./
COPY loggen ./loggen

# Install loggen, then remove build dependencies to keep image small
RUN pip install --no-cache-dir -e . \
    && apk del .build-deps \
    && rm -rf /root/.cargo /root/.cache

# Create non-root user (UID/GID 1000 matches most host users by default)
RUN addgroup -g 1000 loggen \
    && adduser -u 1000 -G loggen -s /bin/bash -D loggen

# Create directory for generated logs (volume mount point) owned by loggen user
RUN mkdir -p /logs && chown -R loggen:loggen /logs

# Switch to non-root user
USER loggen

# Switch to logs directory so relative outputs land in the mounted volume
WORKDIR /logs

# Default to interactive bash so users can run loggen commands
CMD ["/bin/bash"]
