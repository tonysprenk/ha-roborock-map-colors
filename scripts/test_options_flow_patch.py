#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
COMPONENT = ROOT / "custom_components" / "roborock"


def fail(message: str) -> None:
    print(f"options flow validation failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def require_contains(path: Path, needle: str) -> None:
    if needle not in path.read_text(encoding="utf-8"):
        fail(f"{path} must contain {needle!r}")


def main() -> int:
    const = COMPONENT / "const.py"
    config_flow = COMPONENT / "config_flow.py"
    strings = COMPONENT / "strings.json"

    require_contains(const, 'CONF_MAP_COLORS = "map_colors"')
    require_contains(const, 'CONF_PATH_COLOR = "path_color"')
    require_contains(const, 'DEFAULT_PATH_COLOR = ""')

    require_contains(config_flow, "CONF_MAP_COLORS,")
    require_contains(config_flow, "CONF_PATH_COLOR,")
    require_contains(config_flow, "DEFAULT_PATH_COLOR,")
    require_contains(config_flow, "from .map_colors import normalize_hex_color")
    require_contains(config_flow, 'errors[CONF_PATH_COLOR] = "invalid_hex_color"')
    require_contains(config_flow, "self.options.setdefault(CONF_MAP_COLORS, {})[")
    require_contains(config_flow, "] = path_color")
    require_contains(config_flow, "self.options.pop(CONF_MAP_COLORS, None)")
    require_contains(config_flow, "vol.Optional(")
    require_contains(config_flow, "CONF_PATH_COLOR,")

    strings_data = json.loads(strings.read_text(encoding="utf-8"))
    options = strings_data["options"]["step"]["drawables"]
    if options["data"].get("path_color") != "Path color":
        fail("strings.json must label path_color")
    if "Hex color" not in options["data_description"].get("path_color", ""):
        fail("strings.json must describe path_color as a hex color")
    if (
        strings_data["config"]["error"].get("invalid_hex_color")
        != "Enter a color in #rrggbb format."
    ):
        fail("strings.json must define invalid_hex_color")

    print("options flow validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
