# SPDX-FileCopyrightText: Copyright (c) 2025 Broadsage <opensource@broadsage.com>
#
# SPDX-License-Identifier: Apache-2.0

# syntax=docker/dockerfile:1

FROM alpine:3.23@sha256:865b95f46d98cf867a156fe4a135ad3fe50d2056aa3f25ed31662dff6da4eb62

LABEL org.opencontainers.image.authors="Broadsage <opensource@broadsage.com>" \
  org.opencontainers.image.url="https://github.com/broadsage/docker-scaffold" \
  org.opencontainers.image.source="https://github.com/broadsage/docker-scaffold" \
  org.opencontainers.image.vendor="Broadsage Corporation Limited" \
  org.opencontainers.image.title="docker-scaffold" \
  org.opencontainers.image.description="Ansible-powered scaffolding tool for Docker image repositories" \
  org.opencontainers.image.licenses="Apache-2.0"

RUN \
  echo "**** Install packages ****" && \
  YQ_VERSION=v4.45.1 && \
  wget -q https://github.com/mikefarah/yq/releases/download/"${YQ_VERSION}"/yq_linux_amd64 -O /usr/bin/yq && \
  chmod +x /usr/bin/yq && \
  apk add --no-cache --upgrade \
  ansible \
  catatonit \
  bash \
  shadow && \
  apk del alpine-release && \
  rm -rf /var/cache/apk/* && \
  echo "**** Create non-root user ****" && \
  addgroup -g 1001 nonroot && \
  adduser -u 1001 -G nonroot -h /app -D nonroot

COPY --chown=1001:1001 ansible /app
COPY --chown=1001:1001 scripts /app/scripts
COPY --chown=1001:1001 VERSION /app/VERSION
COPY --chown=1001:1001 entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

WORKDIR /app

# Health check for container orchestrators
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD ["/bin/true"]

# Run as non-root user by default (UID 1001 - Docker convention)
# Using numeric UID for OpenShift/Kubernetes compatibility
USER 1001

ENTRYPOINT ["/usr/bin/catatonit", "--", "/entrypoint.sh"]