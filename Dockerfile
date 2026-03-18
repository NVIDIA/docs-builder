# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

FROM hashicorp/vault AS v
FROM python:3.13

ARG UID=1000
ARG FERN_API_VERSION=4.31.1
ARG NODE_VERSION=22.12.0

RUN apt-get update && DEBIAN_FRONTEND=noninteractive \
 && apt-get install --no-install-recommends -y \
      make \
      rsync \
      openssh-client \
      wget \
      jq \
      curl \
      ca-certificates \
      xz-utils

COPY --from=v /bin/vault /bin/vault
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

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
