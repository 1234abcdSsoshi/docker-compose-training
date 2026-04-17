from datetime import date

import pytest

from app import create_app
from app.models import Diary, db


@pytest.fixture
def app():
    app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test-secret",
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )

    with app.app_context():
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def create_sample_diary(title: str = "テスト日記") -> int:
    diary = Diary(
        title=title,
        content="これはテスト本文です。",
        entry_date=date(2026, 4, 17),
        mood="嬉しい",
        tags="テスト, Python",
    )
    db.session.add(diary)
    db.session.commit()
    return diary.id


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "日記アプリへようこそ".encode("utf-8") in response.data


def test_create_diary(client):
    response = client.post(
        "/diaries/new",
        data={
            "title": "新しい日記",
            "content": "今日は良い一日でした。",
            "entry_date": "2026-04-17",
            "mood": "嬉しい",
            "tags": "日常, 学習",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "新しい日記".encode("utf-8") in response.data

    diaries = Diary.query.all()
    assert len(diaries) == 1


def test_list_diaries(client, app):
    with app.app_context():
        create_sample_diary()

    response = client.get("/diaries")
    assert response.status_code == 200
    assert "テスト日記".encode("utf-8") in response.data


def test_delete_diary(client, app):
    with app.app_context():
        diary_id = create_sample_diary()

    response = client.post(f"/diaries/{diary_id}/delete", follow_redirects=True)
    assert response.status_code == 200
    assert "日記を削除しました。".encode("utf-8") in response.data

    with app.app_context():
        assert Diary.query.count() == 0