from pathlib import Path

from dotenv import load_dotenv
from flask import Flask

from .config import Config
from .models import db

# ルートの .env を読み込む
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__)

    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    # SQLite 保存先ディレクトリを作成
    db_dir = Path(app.root_path) / "db"
    db_dir.mkdir(parents=True, exist_ok=True)

    db.init_app(app)

    from .routes.diary import diary_bp

    app.register_blueprint(diary_bp)

    with app.app_context():
        db.create_all()

    return app