# SPDX-FileCopyrightText: Copyright (c) 2025 Broadsage <opensource@broadsage.com>
#
# SPDX-License-Identifier: Apache-2.0

# syntax=docker/dockerfile:1

FROM alpine:3.22

LABEL org.opencontainers.image.authors="Broadsage Opensource <opensource@broadsage.com>" \
      org.opencontainers.image.url="https://github.com/broadsage/docker-scaffold" \
      org.opencontainers.image.source="https://github.com/broadsage/docker-scaffold" \
      org.opencontainers.image.vendor="Broadsage Corporation Limited" \
      org.opencontainers.image.title="docker-scaffold" \
      org.opencontainers.image.description="Ansible-powered scaffolding tool for Docker image repositories" \
      org.opencontainers.image.licenses="Apache-2.0"

RUN \
  echo "**** Install packages ****" && \
  YQ_VERSION=v4.45.1 && \
  wget -q https://github.com/mikefarah/yq/releases/download/${YQ_VERSION}/yq_linux_amd64 -O /usr/bin/yq && \
  chmod +x /usr/bin/yq && \
  apk add --no-cache --upgrade \
    ansible \
    catatonit \
    bash \
    shadow && \
  apk del alpine-release && \
  rm -rf /var/cache/apk/*

COPY ansible /app
COPY scripts /app/scripts
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

WORKDIR /app

ENTRYPOINT ["/usr/bin/catatonit", "--", "/entrypoint.sh"]