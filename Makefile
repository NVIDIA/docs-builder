# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = docs
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help docs-html docs-live test

docs-html:
	sphinx-build -W -b html -d /tmp "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(0)

docs-live:
	@echo "Starting sphinx-autobuild..."
	sphinx-autobuild --host 0.0.0.0 -W -b html -d /tmp "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(0)

# Install development dependencies
install-dev:
	pip install -r requirements-dev.txt

# Run tests with pytest
test:
	pytest tests/ -vv -s

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -b $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
