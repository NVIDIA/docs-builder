# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

import json
import sys
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent.parent / "scripts"))
import generate_versions_json as gvj


# ---------------------------------------------------------------------------
# semver_key — pure function, no mocking needed
# ---------------------------------------------------------------------------


def test_semver_key_valid():
    assert gvj.semver_key("v3.1.0") == (3, 1, 0)


def test_semver_key_zero_components():
    assert gvj.semver_key("v0.0.1") == (0, 0, 1)


def test_semver_key_invalid_returns_sentinel():
    assert gvj.semver_key("not-a-tag") == (-1, -1, -1)
    assert gvj.semver_key("v1.2") == (-1, -1, -1)
    assert gvj.semver_key("1.2.3") == (-1, -1, -1)


def test_semver_key_sort_order():
    tags = ["v1.10.0", "v1.9.0", "v2.0.0", "v1.10.1"]
    assert sorted(tags, key=gvj.semver_key, reverse=True) == [
        "v2.0.0",
        "v1.10.1",
        "v1.10.0",
        "v1.9.0",
    ]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def fake_tags(*tags):
    """Return a mock for subprocess.run that yields the given tag strings."""
    result = MagicMock()
    result.stdout = "\n".join(tags) + "\n"
    return result


def run_main(tmp_path, tags, extra_args=None):
    """Patch dependencies and call main(), returning the parsed JSON output."""
    argv = ["generate-versions-json", "--output", str(tmp_path)] + (extra_args or [])

    with (
        patch("subprocess.run", return_value=fake_tags(*tags)),
        patch.object(sys, "argv", argv),
    ):
        gvj.main()

    return json.loads((tmp_path / "versions1.json").read_text())


# ---------------------------------------------------------------------------
# main() — normal cases
# ---------------------------------------------------------------------------


def test_newest_tag_is_preferred(tmp_path):
    entries = run_main(tmp_path, ["v1.0.0", "v2.0.0", "v1.5.0"])
    assert entries[0]["preferred"] is True
    assert entries[0]["version"] == "2.0.0"


def test_older_tags_have_no_preferred_key(tmp_path):
    entries = run_main(tmp_path, ["v1.0.0", "v2.0.0", "v1.5.0"])
    for entry in entries[1:]:
        assert "preferred" not in entry


def test_tags_sorted_descending(tmp_path):
    entries = run_main(tmp_path, ["v1.0.0", "v3.0.0", "v2.0.0"])
    assert [e["version"] for e in entries] == ["3.0.0", "2.0.0", "1.0.0"]


def test_url_format(tmp_path):
    entries = run_main(tmp_path, ["v1.0.0", "v2.0.0"])
    for entry in entries:
        assert entry["url"] == f"../{entry['version']}"


def test_v_prefix_stripped_from_version(tmp_path):
    entries = run_main(tmp_path, ["v3.1.0"])
    assert entries[0]["version"] == "3.1.0"


def test_single_tag(tmp_path):
    entries = run_main(tmp_path, ["v1.0.0"])
    assert len(entries) == 1
    assert entries[0]["preferred"] is True
    assert entries[0]["version"] == "1.0.0"


def test_non_semver_tags_skipped(tmp_path):
    entries = run_main(tmp_path, ["v2.0.0", "nightly", "v1.0.0", "rc1"])
    assert [e["version"] for e in entries] == ["2.0.0", "1.0.0"]


# ---------------------------------------------------------------------------
# main() — --limit flag
# ---------------------------------------------------------------------------


def test_limit_restricts_older_entries(tmp_path):
    tags = ["v1.0.0", "v2.0.0", "v3.0.0", "v4.0.0", "v5.0.0"]
    entries = run_main(tmp_path, tags, extra_args=["--limit", "2"])
    assert len(entries) == 3  # preferred + 2 older
    assert entries[0]["version"] == "5.0.0"
    assert entries[1]["version"] == "4.0.0"
    assert entries[2]["version"] == "3.0.0"


def test_limit_does_not_exclude_preferred(tmp_path):
    entries = run_main(tmp_path, ["v1.0.0", "v2.0.0"], extra_args=["--limit", "0"])
    assert len(entries) == 1
    assert entries[0]["preferred"] is True


def test_limit_larger_than_available_tags(tmp_path):
    tags = ["v1.0.0", "v2.0.0"]
    entries = run_main(tmp_path, tags, extra_args=["--limit", "99"])
    assert len(entries) == 2


def test_no_limit_includes_all_tags(tmp_path):
    tags = [f"v1.0.{i}" for i in range(10)]
    entries = run_main(tmp_path, tags)
    assert len(entries) == 10


# ---------------------------------------------------------------------------
# main() — --output flag
# ---------------------------------------------------------------------------


def test_custom_output_dir(tmp_path):
    output_dir = tmp_path / "custom"
    output_dir.mkdir()
    argv = ["generate-versions-json", "--output", str(output_dir)]

    with (
        patch("subprocess.run", return_value=fake_tags("v1.0.0", "v2.0.0")),
        patch.object(sys, "argv", argv),
    ):
        gvj.main()

    entries = json.loads((output_dir / "versions1.json").read_text())
    assert len(entries) == 2
    assert entries[0]["version"] == "2.0.0"


# ---------------------------------------------------------------------------
# main() — --name / project.json
# ---------------------------------------------------------------------------


def test_name_writes_project_json(tmp_path):
    run_main(tmp_path, ["v1.0.0", "v3.1.0", "v2.0.0"], extra_args=["--name", "nim-operator"])
    project = json.loads((tmp_path / "project.json").read_text())
    assert project == {"name": "nim-operator", "version": "3.1.0"}


def test_project_version_matches_preferred(tmp_path):
    entries = run_main(tmp_path, ["v1.0.0", "v2.0.0"], extra_args=["--name", "my-project"])
    project = json.loads((tmp_path / "project.json").read_text())
    preferred = next(e for e in entries if e.get("preferred"))
    assert project["version"] == preferred["version"]


def test_no_name_skips_project_json(tmp_path):
    run_main(tmp_path, ["v1.0.0", "v2.0.0"])
    assert not (tmp_path / "project.json").exists()


# ---------------------------------------------------------------------------
# main() — error cases
# ---------------------------------------------------------------------------


def test_no_valid_tags_exits_nonzero(tmp_path):
    with pytest.raises(SystemExit) as exc_info:
        run_main(tmp_path, ["nightly", "rc1"])
    assert exc_info.value.code != 0


def test_empty_tag_list_exits_nonzero(tmp_path):
    with pytest.raises(SystemExit) as exc_info:
        run_main(tmp_path, [])
    assert exc_info.value.code != 0
