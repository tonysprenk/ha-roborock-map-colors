# Roborock Map Colors

Custom Home Assistant `roborock` component override for Home Assistant Core 2026.6.1.

This keeps the built-in Roborock integration behavior from Core 2026.6.1 and adds one map rendering option: a configurable robot path color. The intended color for this installation is `#ff2d55`, which makes the traveled path visible over blue room backgrounds.

## Compatibility

- Home Assistant Core 2026.6.1
- `python-roborock==5.12.0`
- `vacuum-map-parser-roborock==0.1.4`

Review this override before using it on a newer Home Assistant Core release.

## Install

Install this repository as a HACS custom integration repository. After installing, restart Home Assistant so `custom_components/roborock` overrides the built-in integration.

Configure the color at:

Settings > Devices & services > Roborock > Configure

Set `Path color` to `#ff2d55`. Leave it empty to use the Roborock default color.

## Rollback

Remove this custom repository from HACS or delete `/config/custom_components/roborock`, then restart Home Assistant. The built-in Roborock integration will load again with the default map palette.
