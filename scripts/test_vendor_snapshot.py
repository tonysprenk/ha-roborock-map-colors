#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
COMPONENT = ROOT / "custom_components" / "roborock"

EXPECTED_FILES = {
    "__init__.py",
    "binary_sensor.py",
    "button.py",
    "config_flow.py",
    "const.py",
    "coordinator.py",
    "diagnostics.py",
    "entity.py",
    "icons.json",
    "image.py",
    "manifest.json",
    "models.py",
    "number.py",
    "quality_scale.yaml",
    "roborock_storage.py",
    "select.py",
    "sensor.py",
    "services.py",
    "services.yaml",
    "strings.json",
    "switch.py",
    "time.py",
    "vacuum.py",
}


def fail(message: str) -> None:
    print(f"vendor snapshot validation failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    if not COMPONENT.is_dir():
        fail("custom_components/roborock is missing")

    actual_files = {path.name for path in COMPONENT.iterdir() if path.is_file()}
    missing = sorted(EXPECTED_FILES - actual_files)
    if missing:
        fail(f"missing vendored files: {missing}")

    manifest = json.loads((COMPONENT / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("domain") != "roborock":
        fail("manifest domain must be roborock")
    if manifest.get("version") != "0.1.0":
        fail("custom component manifest version must be 0.1.0")

    requirements = set(manifest.get("requirements", []))
    required = {
        "python-roborock==5.12.0",
        "vacuum-map-parser-roborock==0.1.4",
    }
    if not required.issubset(requirements):
        fail(f"manifest requirements must include {sorted(required)}")

    init_text = (COMPONENT / "__init__.py").read_text(encoding="utf-8")
    if "map_parser_config=MapParserConfig(" not in init_text:
        fail("__init__.py must still configure MapParserConfig")

    print("vendor snapshot validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
