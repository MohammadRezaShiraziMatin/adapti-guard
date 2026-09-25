import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts" / "notion"))
from academic_os_client import parse_notion_id


def test_parse_notion_id_from_uuid():
    assert (
        parse_notion_id("248104cd-477e-80af-bc30-000bd28de8f9")
        == "248104cd-477e-80af-bc30-000bd28de8f9"
    )


def test_parse_notion_id_from_url():
    url = "https://www.notion.so/myworkspace/Page-Title-248104cd477e80afbc30000bd28de8f9"
    assert parse_notion_id(url) == "248104cd-477e-80af-bc30-000bd28de8f9"
