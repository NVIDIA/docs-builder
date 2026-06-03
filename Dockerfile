# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

ARG AWS_CLI_VERSION=2.35.16
ARG PYTHON_VERSION=3.13.14
ARG UV_VERSION=0.11.27
ARG VAULT_VERSION=2.0.3
ARG YQ_VERSION=4.53.3

FROM public.ecr.aws/aws-cli/aws-cli:${AWS_CLI_VERSION}@sha256:6614ba94b6ca40af5eb5cd7b97229950c171e38ad8d30f4fd764ef17cd9e39b7 AS aws
FROM mikefarah/yq:${YQ_VERSION}@sha256:11a1f0b604b13dbbdc662260d8db6f644b22d8553122a25c1b5b2e8713ca6977 AS yq
FROM hashicorp/vault:${VAULT_VERSION}@sha256:a296a888b118615dc01d5f1a6846e6d4a7277946caaed5b447008fff5fe06b54 AS vault
FROM ghcr.io/astral-sh/uv:${UV_VERSION}@sha256:4d01caf3b22dfd11003455e2e68153da08c4ee1fa54fdbd166c6282d22693419 AS uv
FROM python:${PYTHON_VERSION}@sha256:4c822f0fadfeba9ea973d81fb5bbd5c2106f12ae02d0a5cdd48907909395310b

ARG UID=1000
ARG FERN_API_VERSION=5.56.3
ARG NODE_VERSION=22.12.0
ARG GH_VERSION=2.93.0

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

RUN apt-get update && DEBIAN_FRONTEND=noninteractive \
 && apt-get install --no-install-recommends -y \
      git \
      unzip \
      less \
      make \
      rsync \
      openssh-client \
      wget \
      jq \
      curl \
      ca-certificates \
      xz-utils \
 && rm -rf /var/lib/apt/lists/*

COPY --from=aws /usr/local/aws-cli /usr/local/aws-cli
COPY --from=yq /usr/bin/yq /usr/local/bin/yq
COPY --from=vault /bin/vault /bin/vault
COPY --from=uv /uv /uvx /bin/

RUN ln -s /usr/local/aws-cli/v2/current/bin/aws /usr/local/bin/aws \
 && aws --version \
 && yq --version \
 && vault version \
 && uv --version

ENV HOME=/home/nvidia
RUN useradd -u "${UID}" -ms /bin/bash nvidia && chmod 777 "${HOME}"
USER nvidia
ENV PATH="/home/nvidia/.venv/bin:/home/nvidia/.local/node/bin:/home/nvidia/.local/bin:${PATH}"

RUN uv venv /home/nvidia/.venv
RUN --mount=type=bind,source=.,destination=/x,rw uv pip install --python /home/nvidia/.venv/bin/python --requirement /x/requirements.txt

RUN curl -fsSL "https://nodejs.org/dist/v${NODE_VERSION}/node-v${NODE_VERSION}-linux-x64.tar.xz" -o /tmp/node.tar.xz \
 && mkdir -p /home/nvidia/.local/node \
 && tar -xJf /tmp/node.tar.xz -C /home/nvidia/.local/node --strip-components=1 \
 && /home/nvidia/.local/node/bin/npm config set prefix /home/nvidia/.local \
 && /home/nvidia/.local/node/bin/npm install -g "fern-api@${FERN_API_VERSION}" \
 && rm /tmp/node.tar.xz

# Prime ~/.fern/app-preview/ with the docs preview bundle.
RUN --mount=type=bind,source=docs/fern,destination=/x/fern,rw set -eux; \
    cd /x/fern; \
    ( fern docs dev >/tmp/fern-warm.log 2>&1 & echo $! > /tmp/fern-warm.pid ); \
    for i in $(seq 1 60); do \
      if [ -d /home/nvidia/.fern/app-preview/.next ] \
         && [ -f /home/nvidia/.fern/app-preview/etag ]; then \
        break; \
      fi; \
      sleep 2; \
    done; \
    kill "$(cat /tmp/fern-warm.pid)" 2>/dev/null || true; \
    sleep 1; \
    kill -9 "$(cat /tmp/fern-warm.pid)" 2>/dev/null || true; \
    rm -f /tmp/fern-warm.log /tmp/fern-warm.pid; \
    test -d /home/nvidia/.fern/app-preview/.next; \
    test -f /home/nvidia/.fern/app-preview/etag; \
    echo "Primed Fern docs preview bundle:"; \
    ls -la /home/nvidia/.fern/app-preview/
