<!--
  SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
  SPDX-License-Identifier: Apache-2.0
-->
# All Extensions Test

This page tests multiple extensions working together.

## Sphinx-Design Tabs with Code (Copybutton)

::::{tab-set}

:::{tab-item} Python Example
```python
>>> import requests
>>> response = requests.get("https://api.example.com")
>>> print(response.status_code)
200
```
:::

:::{tab-item} Shell Example
```bash
$ curl https://api.example.com
$ python script.py
```
:::

::::

## Grid with Cards

::::{grid} 2
:gutter: 1

:::{grid-item-card} API Documentation
:link: api-reference
:link-type: ref

Complete API reference with examples
:::

:::{grid-item-card} Getting Started
Quick start guide for beginners
:::

::::

(api-reference)=
## API Reference

```{swagger-plugin} _static/openapi.yaml
:id: combined-test-api
```

## Intersphinx Test

Link to Python docs: {external+python:py:class}`dict`

## Substitutions

<https://github.com/adamtheturtle/sphinx-substitution-extensions?tab=readme-ov-file#using-substitutions-in-myst-markdown>

```{code-block} console

$ bash {{substitute_me}}
```

And inline code: {substitution-code}`run bash {{substitute_me}}`.

In plain text, you can add spaces: {{ substitute_me }}.
