from datetime import date, datetime

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Diary(db.Model):
    __tablename__ = "diaries"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    entry_date = db.Column(db.Date, nullable=False, default=date.today)
    mood = db.Column(db.String(50), nullable=True, default="")
    tags = db.Column(db.String(255), nullable=True, default="")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    @property
    def tag_list(self) -> list[str]:
        if not self.tags:
            return []
        return [tag.strip() for tag in self.tags.split(",") if tag.strip()]

    def __repr__(self) -> str:
        return f"<Diary id={self.id} title={self.title!r}>"