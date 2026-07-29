<!--
  SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
  SPDX-License-Identifier: Apache-2.0
-->
# Product Documentation Builder

Use the images from this project to build HTML for NVIDIA product documentation.

## Autobuild

To use sphinx-autobuild, perform the following actions:

- Update your `Makefile`, or other build tool, to run the `sphinx-autobuild` command, like the example in this repository.
- When you start the container to build your documentation project, add the `-p 8000:8000` command-line argument.

## Swagger

```{swagger-plugin} _static/openapi.yaml
:id: some-id
```
