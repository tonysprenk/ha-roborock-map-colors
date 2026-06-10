#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
COMPONENT = ROOT / "custom_components" / "roborock"


def require_contains(path: Path, needle: str) -> None:
    text = path.read_text(encoding="utf-8")
    if needle not in text:
        print(f"{path} must contain {needle!r}", file=sys.stderr)
        raise SystemExit(1)


def require_order(path: Path, before: str, after: str) -> None:
    text = path.read_text(encoding="utf-8")
    before_index = text.find(before)
    after_index = text.find(after)
    if before_index == -1 or after_index == -1 or before_index >= after_index:
        print(f"{path} must place {before!r} before {after!r}", file=sys.stderr)
        raise SystemExit(1)


def main() -> int:
    map_colors = COMPONENT / "map_colors.py"
    init_file = COMPONENT / "__init__.py"

    if not map_colors.is_file():
        print("map_colors.py is missing", file=sys.stderr)
        return 1

    require_contains(
        map_colors, "class MapParserConfig(roborock_map_parser.MapParserConfig):"
    )
    require_contains(
        map_colors,
        "colors: dict[SupportedColor, Color] = field(default_factory=dict)",
    )
    require_contains(
        map_colors, "room_colors: dict[str, Color] = field(default_factory=dict)"
    )
    require_contains(map_colors, "def normalize_hex_color(value: str | None) -> str:")
    require_contains(map_colors, "def hex_to_rgb(value: str) -> tuple[int, int, int]:")
    require_contains(map_colors, "def apply_map_parser_palette_patch() -> None:")
    require_contains(
        map_colors,
        "roborock_map_parser._create_map_data_parser = _create_map_data_parser",
    )
    require_contains(map_colors, "ColorsPalette(color_dicts, room_colors)")

    const_file = COMPONENT / "const.py"
    require_contains(const_file, 'CONF_MAP_COLORS = "map_colors"')
    require_contains(const_file, 'CONF_PATH_COLOR = "path_color"')
    require_contains(const_file, 'DEFAULT_PATH_COLOR = ""')

    require_contains(
        init_file, "from vacuum_map_parser_base.config.color import SupportedColor"
    )
    require_contains(
        init_file,
        "from .map_colors import MapParserConfig, apply_map_parser_palette_patch, hex_to_rgb",
    )
    require_contains(init_file, "apply_map_parser_palette_patch()")
    require_contains(init_file, "colors=_map_parser_colors_from_options(entry.options),")
    require_contains(init_file, "def _map_parser_colors_from_options(")
    require_contains(init_file, "path_color = options.get(CONF_PATH_COLOR)")
    require_contains(init_file, "map_colors = options.get(CONF_MAP_COLORS, {})")
    require_order(init_file, "apply_map_parser_palette_patch()", "async def async_setup(")

    print("map color parser patch validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
