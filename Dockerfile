# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

FROM hashicorp/vault AS v
FROM python:3.13

ARG UID=1000

RUN apt-get update && DEBIAN_FRONTEND=noninteractive \
 && apt-get install --no-install-recommends -y \
      make \
      rsync \
      openssh-client \
      wget \
      jq

COPY --from=v /bin/vault /bin/vault

ENV HOME=/home/nvidia
RUN useradd -u "${UID}" -ms /bin/bash nvidia && chmod 777 "${HOME}"
USER nvidia
ENV PATH="/home/nvidia/.local/bin:${PATH}"

RUN --mount=type=bind,source=.,destination=/x,rw python3 -m pip install \
        --requirement=/x/requirements.txt