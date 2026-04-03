#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
"""Generate versions1.json and optionally project.json from git tags.

Tags must follow the format v<semver> (e.g. v3.1.0). The script sorts all
matching tags in descending semver order, marks the newest as preferred, and
writes docs/versions1.json relative to the current working directory.

Usage:
    generate-versions-json [--limit N] [--output PATH] [--name NAME] [--project-output PATH]

    --limit N      Maximum number of older versions to include after the preferred
                   (latest) entry. "latest" does not count toward this limit.
                   Defaults to no limit (all tags included).
    --output DIR   Directory to write output files (default: docs).
                   Writes versions1.json always, and project.json when --name is provided.
    --name NAME    Project name. When provided, also writes project.json.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

SEMVER_RE = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")
DEFAULT_OUTPUT_DIR = Path("docs")


def get_tags() -> list[str]:
    result = subprocess.run(
        ["git", "tag", "--list", "v*"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.splitlines()


def semver_key(tag: str) -> tuple[int, int, int]:
    m = SEMVER_RE.match(tag)
    if not m:
        return (-1, -1, -1)
    return (int(m.group(1)), int(m.group(2)), int(m.group(3)))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        metavar="N",
        help="Number of older versions to include after the preferred (latest) entry.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        metavar="DIR",
        help="Directory to write output files (default: docs).",
    )
    parser.add_argument(
        "--name",
        default=None,
        metavar="NAME",
        help="Project name. When provided, also writes project.json.",
    )
    args = parser.parse_args()

    tags = get_tags()
    valid_tags = [t for t in tags if SEMVER_RE.match(t)]

    if not valid_tags:
        print("No semver tags found (expected format: v<major>.<minor>.<patch>)", file=sys.stderr)
        sys.exit(1)

    valid_tags.sort(key=semver_key, reverse=True)

    # The preferred (latest) tag is always included; the limit applies to the rest.
    preferred, *older = valid_tags
    if args.limit is not None:
        older = older[: args.limit]

    entries = []
    for i, tag in enumerate([preferred] + older):
        version = tag.lstrip("v")
        entry = {"version": version, "url": f"../{version}"}
        if i == 0:
            entry = {"preferred": True, **entry}
        entries.append(entry)

    versions_file = args.output / "versions1.json"
    versions_file.write_text(json.dumps(entries, indent=4) + "\n")
    print(f"Wrote {len(entries)} entries to {versions_file}")

    if args.name is not None:
        project = {"name": args.name, "version": preferred.lstrip("v")}
        project_file = args.output / "project.json"
        project_file.write_text(json.dumps(project, indent=4) + "\n")
        print(f"Wrote project.json to {project_file}")


if __name__ == "__main__":
    main()
