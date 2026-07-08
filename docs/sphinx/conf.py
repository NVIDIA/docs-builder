# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
project = 'NVIDIA Product Documentation Builder'
copyright = '2025, NVIDIA Corporation'
author = 'NVIDIA Corporation'
release = '0.1.0'

extensions = [
    'myst_parser',
    'sphinx.ext.intersphinx',
    'sphinx_copybutton',
    'sphinx_design',
    'swagger_plugin_for_sphinx',
    'sphinx_substitution_extensions',
]

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'nvidia_sphinx_theme'
html_theme_options = {
    'public_docs_features': True,
}
html_static_path = ['_static']
# html_base_url = 'https://docs.nvidia.com/.../latest/'
html_copy_source = False
html_show_sphinx = False
html_show_sourcelink = False
html_domain_indices = False
html_use_index = False
