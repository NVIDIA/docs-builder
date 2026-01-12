<!--
  SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
  SPDX-License-Identifier: Apache-2.0
-->
# NVIDIA Product Documentation Builder

## Why

Use the images from this project to build HTML for NVIDIA product documentation using Sphinx.

The goal of putting common Sphinx packages in a container is to standardize on the tooling
and avoid repo-by-repo customizations.
If a customization is useful to one project, put the customization in this project so everyone can benefit.

## Getting the Container

1. Pull the container:

   ```console
   $ docker pull ghcr.io/nvidia/docs-builder:0.1.0
   ```

   The tag changes periodically.
   Refer to the [container registry](https://github.com/NVIDIA/docs-builder/pkgs/container/docs-builder)
   for newer tags.

## Update Your Project

If this is the first time you use the container with your project or you pulled a newer container, update the project dependencies.

1. Update the image in your GitHub workflow file:

   ```yaml
   variables:
     IMAGE: ghcr.io/nvidia/docs-builder:0.1.0
   ```

   There is more than one way to specify the image.
   Your repo might specify the image in some other way.

1. Commit and push the updates to your repo.

## Build the Documentation

1. Start the docs-builder container, referencing the repo as the `/work` directory:

   ```console
   $ docker run --rm -it -v $(pwd):/work -w /work ghcr.io/nvidia/docs-builder:0.1.0 bash
   ```

1. Inside the container, build the docs:

   ```console
   $ make <possible-arguments>

   # Or with sphinx-build.
   $ sphinx-build -m html <docs/source> <docs/_build>
   ```

## Troubleshooting Permissions Errors

If your UNIX user ID is not `1000`, you can experience permissions issues.
You can determine your ID by running `id -u` in a terminal, outside the container.
If your ID is not `1000`, the clone the docs-builder-sphinx repo and build your own container with a command like the following example:

```console
$ docker build \
    -t ghcr.io/nvidia/docs-builder:0.1.0 \
    --build-arg UID=$(id -u) .
```
