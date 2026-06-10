#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import shutil
import tempfile
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
CORE_TAG = "2026.6.1"
ARCHIVE_URL = f"https://github.com/home-assistant/core/archive/refs/tags/{CORE_TAG}.zip"
SOURCE_IN_ARCHIVE = (
    Path(f"core-{CORE_TAG}") / "homeassistant" / "components" / "roborock"
)
DESTINATION = ROOT / "custom_components" / "roborock"
CUSTOM_VERSION = "0.1.0"


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="roborock-core-") as temp_dir:
        temp_path = Path(temp_dir)
        archive_path = temp_path / f"core-{CORE_TAG}.zip"
        print(f"Downloading {ARCHIVE_URL}")
        urllib.request.urlretrieve(ARCHIVE_URL, archive_path)

        with zipfile.ZipFile(archive_path) as archive:
            archive.extractall(temp_path)

        source = temp_path / SOURCE_IN_ARCHIVE
        if not source.is_dir():
            raise FileNotFoundError(f"Could not find {source}")

        if DESTINATION.exists():
            shutil.rmtree(DESTINATION)
        DESTINATION.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, DESTINATION)

    manifest_path = DESTINATION / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["version"] = CUSTOM_VERSION
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(
        f"Vendored Home Assistant Core {CORE_TAG} Roborock component "
        f"into {DESTINATION}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
