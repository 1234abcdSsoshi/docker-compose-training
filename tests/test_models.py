from datetime import date

from app.models import Diary


def test_tag_list_property():
    diary = Diary(
        title="タグ確認",
        content="本文",
        entry_date=date(2026, 4, 17),
        tags="Python, Flask, 日記",
    )

    assert diary.tag_list == ["Python", "Flask", "日記"]


def test_empty_tags():
    diary = Diary(
        title="空タグ",
        content="本文",
        entry_date=date(2026, 4, 17),
        tags="",
    )

    assert diary.tag_list == []