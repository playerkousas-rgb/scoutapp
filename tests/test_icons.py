"""G11 app-icon contract for the TW7 temporary brand."""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ICONS = ROOT / "static" / "icons"

EXPECTED = {
    "favicon-16.png": (16, 16),
    "favicon-32.png": (32, 32),
    "apple-touch-icon.png": (180, 180),
    "icon-192.png": (192, 192),
    "icon-512.png": (512, 512),
    "icon-maskable-192.png": (192, 192),
    "icon-maskable-512.png": (512, 512),
    "og-image.png": (1200, 630),
}


def test_all_nine_g11_icon_files_exist_at_the_right_sizes():
    files = {p.name for p in ICONS.iterdir() if p.is_file()}
    assert files == {*EXPECTED, "favicon.ico"}
    for name, size in EXPECTED.items():
        with Image.open(ICONS / name) as image:
            assert image.size == size, name
            assert image.format == "PNG", name
    with Image.open(ICONS / "favicon.ico") as image:
        sizes = set(image.info.get("sizes") or [])
    assert sizes == {(16, 16), (32, 32), (48, 48)}


def test_icons_stay_under_the_g11_budget_and_are_full_bleed():
    assert sum(path.stat().st_size for path in ICONS.iterdir() if path.is_file()) <= 260 * 1024
    for name in ("icon-192.png", "icon-512.png", "icon-maskable-192.png", "icon-maskable-512.png"):
        with Image.open(ICONS / name) as image:
            rgb = image.convert("RGB")
            corners = [rgb.getpixel((0, 0)), rgb.getpixel((rgb.width - 1, 0)),
                       rgb.getpixel((0, rgb.height - 1)), rgb.getpixel((rgb.width - 1, rgb.height - 1))]
            assert all(pixel != (255, 255, 255) for pixel in corners), name
            assert len(rgb.getcolors(maxcolors=1_000_000) or []) >= 4, name


def test_manifest_and_head_reference_the_g11_files(client):
    manifest = json.loads((ROOT / "static" / "manifest.webmanifest").read_text())
    assert manifest["theme_color"] == "#24533F"
    assert manifest["background_color"] == "#79C9C3"
    assert {(i["src"], i["sizes"], i["purpose"]) for i in manifest["icons"]} == {
        ("/icons/icon-192.png", "192x192", "any"),
        ("/icons/icon-512.png", "512x512", "any"),
        ("/icons/icon-maskable-192.png", "192x192", "maskable"),
        ("/icons/icon-maskable-512.png", "512x512", "maskable"),
    }
    page = client.get("/login").get_data(as_text=True)
    for required in ("/icons/favicon.ico", "/icons/favicon-16.png", "/icons/favicon-32.png",
                     "/icons/apple-touch-icon.png", "/manifest.webmanifest", "/icons/og-image.png"):
        assert required in page
    response = client.get("/icons/icon-192.png")
    assert response.status_code == 200
    assert "immutable" in response.headers["Cache-Control"]
