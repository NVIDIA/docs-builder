# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Integration tests for all extensions working together."""

import pytest
from pathlib import Path
from sphinx.testing.util import SphinxTestApp


class TestAllExtensions:

    @pytest.mark.sphinx('html', testroot='all-extensions')
    def test_build(self, app: SphinxTestApp) -> None:
        app.build(force_all=True)
        assert app.statuscode == 0

        index_html = Path(app.outdir) / 'index.html'
        with open(index_html, 'r', encoding='utf-8') as f:
            html_content = f.read()

            assert '::::{tab-set}' not in html_content
            assert '<div class="sd-tab-set' in html_content

            assert '::::{grid}' not in html_content
            assert '<div class="sd-card-body' in html_content

            assert 'id="combined-test-api">' in html_content

            assert '<a class="reference external" href="https://docs.python.org/' in html_content

            assert '>Is this page helpful?<' in html_content
            assert 'src="https://assets.adobedtm.com/' in html_content

            assert 'substitute_me' not in html_content
            assert 'substitution_done' in html_content