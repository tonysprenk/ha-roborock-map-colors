#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


def fail(message: str) -> None:
    print(f"hacs package validation failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    hacs_path = ROOT / "hacs.json"
    readme_path = ROOT / "README.md"
    if not hacs_path.is_file():
        fail("hacs.json is missing")
    if not readme_path.is_file():
        fail("README.md is missing")

    hacs = json.loads(hacs_path.read_text(encoding="utf-8"))
    if hacs.get("name") != "Roborock Map Colors":
        fail("hacs.json name must be Roborock Map Colors")
    if hacs.get("domains") != ["roborock"]:
        fail("hacs.json domains must be ['roborock']")
    if hacs.get("homeassistant") != "2026.6.1":
        fail("hacs.json must pin Home Assistant compatibility to 2026.6.1")

    readme = readme_path.read_text(encoding="utf-8")
    required = [
        "Home Assistant Core 2026.6.1",
        "#ff2d55",
        "Settings > Devices & services > Roborock > Configure",
        "Rollback",
        "custom_components/roborock",
    ]
    for snippet in required:
        if snippet not in readme:
            fail(f"README.md must contain {snippet!r}")

    print("hacs package validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
