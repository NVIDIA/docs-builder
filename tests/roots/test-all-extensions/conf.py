# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
"""Test configuration with common extensions enabled."""

extensions = [
    'myst_parser',
    'sphinx.ext.intersphinx',
    'sphinx_copybutton',
    'sphinx_design',
    'swagger_plugin_for_sphinx',
    'sphinx_substitution_extensions',
]

exclude_patterns = ['_build']
html_theme = 'nvidia_sphinx_theme'
html_static_path = ['_static']

html_theme_options = {
    'public_docs_features': True,
}

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

# Copybutton config
copybutton_exclude = '.linenos, .gp, .go'

myst_enable_extensions = [
    'dollarmath',
    'colon_fence',
    'substitution',
]

substitutions_default_enabled = True

myst_substitutions = {
    "substitute_me": "substitution_done",
}