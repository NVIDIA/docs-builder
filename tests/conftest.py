# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Pytest configuration and fixtures for Sphinx documentation tests."""

import pytest
from pathlib import Path
from sphinx.testing.util import SphinxTestApp

# Get the directory containing the test roots
pytest_plugins = 'sphinx.testing.fixtures'

# Root directory for all test fixtures
TEST_ROOTS_DIR = Path(__file__).parent / 'roots'


@pytest.fixture(scope='session')
def rootdir() -> Path:
    """Return the path to the test roots directory for Sphinx testing fixtures."""
    return TEST_ROOTS_DIR


def make_app(testroot: str, **kwargs) -> SphinxTestApp:
    """
    Create a SphinxTestApp for testing.

    Args:
        testroot: Name of the test root directory (e.g., 'test-sphinx-design')
        **kwargs: Additional arguments to pass to SphinxTestApp

    Returns:
        Configured SphinxTestApp instance
    """
    srcdir = (TEST_ROOTS_DIR / testroot).resolve()

    # Set default kwargs
    kwargs.setdefault('buildername', 'html')
    kwargs.setdefault('freshenv', True)
    kwargs.setdefault('warningiserror', True)

    # Create the app
    app = SphinxTestApp(srcdir=srcdir, **kwargs)

    return app
