"""Map color support for the Roborock custom component."""

from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import cast

from vacuum_map_parser_base.config.color import Color, ColorsPalette, SupportedColor
from vacuum_map_parser_base.config.drawable import Drawable
from vacuum_map_parser_base.config.image_config import ImageConfig
from vacuum_map_parser_base.config.size import Size, Sizes
from vacuum_map_parser_roborock.map_data_parser import RoborockMapDataParser

from roborock.map import map_parser as roborock_map_parser

_HEX_COLOR_RE = re.compile(r"^#[0-9a-fA-F]{6}$")


@dataclass
class MapParserConfig(roborock_map_parser.MapParserConfig):
    """Roborock map parser config with optional palette overrides."""

    colors: dict[SupportedColor, Color] = field(default_factory=dict)
    """Map element color overrides."""

    room_colors: dict[str, Color] = field(default_factory=dict)
    """Room color overrides keyed by Roborock room id."""


def normalize_hex_color(value: str | None) -> str:
    """Normalize an optional #rrggbb color for storage."""
    if value is None:
        return ""
    value = value.strip()
    if not value:
        return ""
    if _HEX_COLOR_RE.fullmatch(value) is None:
        raise ValueError(f"Invalid hex color: {value}")
    return value.lower()


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    """Convert a normalized #rrggbb color to an RGB tuple."""
    value = normalize_hex_color(value)
    if not value:
        raise ValueError("Empty hex color cannot be converted to RGB")
    return cast(
        tuple[int, int, int],
        tuple(int(value[index : index + 2], 16) for index in (1, 3, 5)),
    )


def apply_map_parser_palette_patch() -> None:
    """Patch python-roborock's parser factory to honor color overrides."""
    roborock_map_parser.MapParserConfig = MapParserConfig
    roborock_map_parser._create_map_data_parser = _create_map_data_parser


def _create_map_data_parser(config: MapParserConfig) -> RoborockMapDataParser:
    """Create a RoborockMapDataParser based on the config entry."""
    color_dicts = dict(getattr(config, "colors", {}) or {})
    room_colors = dict(getattr(config, "room_colors", {}) or {})

    if not config.show_background:
        color_dicts[SupportedColor.MAP_OUTSIDE] = (0, 0, 0, 0)

    if not config.show_walls:
        color_dicts[SupportedColor.GREY_WALL] = (0, 0, 0, 0)
        color_dicts[SupportedColor.MAP_WALL] = (0, 0, 0, 0)
        color_dicts[SupportedColor.MAP_WALL_V2] = (0, 0, 0, 0)

    if not config.show_rooms:
        room_colors.update(
            {str(room_id): (0, 0, 0, 0) for room_id in range(1, 32)}
        )

    return RoborockMapDataParser(
        ColorsPalette(color_dicts, room_colors),
        Sizes(
            {
                size: value * config.map_scale
                for size, value in Sizes.SIZES.items()
                if size != Size.MOP_PATH_WIDTH
            }
        ),
        cast(list[Drawable], config.drawables),
        ImageConfig(scale=config.map_scale),
        [],
    )
