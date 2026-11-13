"""TW7 brand and no-patrol acceptance tests."""
from __future__ import annotations

import json
from pathlib import Path

from scout.schema import DEFAULT_SETTINGS

ROOT = Path(__file__).resolve().parents[1]


def test_tw7_is_the_default_brand_and_patrols_are_disabled():
    assert DEFAULT_SETTINGS["unit_name_zh"] == "香港童軍總會荃灣第7旅"
    assert DEFAULT_SETTINGS["unit_name_en"] == "7th Tsuen Wan Scout Group"
    assert DEFAULT_SETTINGS["patrols"] == []
    assert DEFAULT_SETTINGS["feature_flags"]["gacha"] is True


def test_sign_in_lists_member_names_directly(client, store):
    store.save_setting("patrols", [])
    page = client.get("/login").get_data(as_text=True)
    assert "選擇你的姓名登入" in page
    assert "王小明" in page and "李美儀" in page
    assert "選擇你的小隊" not in page
    assert "Tiger" not in page and "Otter" not in page and "Seagull" not in page
    assert "TW7" in page and "香港童軍總會荃灣第7旅" in page


def test_leader_can_create_and_edit_a_member_without_a_patrol(leader_client, store):
    store.save_setting("patrols", [])
    response = leader_client.post("/leader/accounts", data={
        "display_name_zh": "新成員", "display_name_en": "New Member",
        "email": "member@example.com", "scout_no": "TW7-001",
    })
    assert response.status_code in (200, 302)
    member = next(u for u in store.list("users") if u.get("display_name_zh") == "新成員")
    assert member["patrol"] == ""

    page = leader_client.get("/leader/accounts").get_data(as_text=True)
    assert "新成員" in page
    assert 'name="patrol"' not in page

    leader_client.post(f"/leader/accounts/{member['id']}", data={
        "display_name_en": "Edited Member", "patrol": "Tiger",
    })
    assert store.get("users", member["id"])["patrol"] == ""


def test_profile_lists_all_members_without_patrol_branding(new_scout, store):
    store.save_setting("patrols", [])
    page = new_scout.get("/profile").get_data(as_text=True)
    assert "所有成員" in page and "成員名單" in page
    assert "各小隊成員" not in page
    assert "港島第八十二旅" not in page


def test_committed_local_database_is_an_empty_scaffold():
    for path in (ROOT / "data" / "db").glob("*.json"):
        assert json.loads(path.read_text()) == [], path.name


def test_no_legacy_brand_text_or_logo_is_shipped():
    needles = ("82hkg", "第八十二", "港島第82旅", "82nd Hong Kong", "筲箕灣區")
    # The existing common badge/game curriculum is intentionally retained unchanged.
    roots = [ROOT / "app.py", ROOT / "api", ROOT / "scout", ROOT / "templates"]
    for target in roots:
        paths = [target] if target.is_file() else list(target.rglob("*"))
        for path in paths:
            if not path.is_file() or path.suffix not in {".py", ".html", ".json", ".md", ".js", ".css"}:
                continue
            text = path.read_text(errors="ignore").casefold()
            assert all(needle.casefold() not in text for needle in needles), path
