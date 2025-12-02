# syntax=docker/dockerfile:1

FROM alpine:3.22

# set version label
ARG BUILD_DATE
ARG VERSION
LABEL build_version="Version:- ${VERSION} Build-date:- ${BUILD_DATE}"
LABEL maintainer="roxedus, thelamer"

RUN \
  echo "**** Install build packages ****" && \
  YQ_VERSION=v4.45.1 &&\
  wget https://github.com/mikefarah/yq/releases/download/${YQ_VERSION}/yq_linux_amd64 -O /usr/bin/yq &&\
  chmod +x /usr/bin/yq && \
  apk add --no-cache --upgrade \
    ansible && \
  printf "Version: ${VERSION}\nBuild-date: ${BUILD_DATE}\n" > /build_version && \
  apk del \
    alpine-release

COPY /ansible /app
COPY entrypoint.sh entrypoint.sh

WORKDIR /app

ENTRYPOINT ["catatonit", "--", "/entrypoint.sh"]