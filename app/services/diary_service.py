from datetime import datetime

from sqlalchemy import or_

from ..models import Diary


def normalize_tags(raw_tags: str) -> str:
    if not raw_tags:
        return ""

    normalized = raw_tags.replace("、", ",")
    tag_list = [tag.strip() for tag in normalized.split(",") if tag.strip()]

    # 重複を除去しつつ順序を維持
    unique_tags = list(dict.fromkeys(tag_list))
    return ", ".join(unique_tags)


def parse_entry_date(raw_date: str):
    return datetime.strptime(raw_date, "%Y-%m-%d").date()


def validate_diary_form(form) -> tuple[dict, list[str]]:
    errors: list[str] = []

    title = form.get("title", "").strip()
    content = form.get("content", "").strip()
    entry_date_raw = form.get("entry_date", "").strip()
    mood = form.get("mood", "").strip()
    tags = normalize_tags(form.get("tags", "").strip())

    if not title:
        errors.append("タイトルは必須です。")

    if not content:
        errors.append("本文は必須です。")

    entry_date = None
    if not entry_date_raw:
        errors.append("日付は必須です。")
    else:
        try:
            entry_date = parse_entry_date(entry_date_raw)
        except ValueError:
            errors.append("日付の形式が正しくありません。")

    data = {
        "title": title,
        "content": content,
        "entry_date": entry_date,
        "mood": mood,
        "tags": tags,
    }
    return data, errors


def apply_diary_data(diary: Diary, data: dict) -> Diary:
    diary.title = data["title"]
    diary.content = data["content"]
    diary.entry_date = data["entry_date"]
    diary.mood = data["mood"]
    diary.tags = data["tags"]
    return diary


def build_diary_query(search_text: str = "", entry_date: str = "", tag: str = ""):
    query = Diary.query

    if search_text:
        pattern = f"%{search_text}%"
        query = query.filter(
            or_(
                Diary.title.ilike(pattern),
                Diary.content.ilike(pattern),
                Diary.tags.ilike(pattern),
            )
        )

    if entry_date:
        try:
            parsed_date = parse_entry_date(entry_date)
            query = query.filter(Diary.entry_date == parsed_date)
        except ValueError:
            pass

    if tag:
        query = query.filter(Diary.tags.ilike(f"%{tag}%"))

    return query.order_by(Diary.entry_date.desc(), Diary.created_at.desc())