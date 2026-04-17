import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DB_PATH = BASE_DIR / "db" / "diary.sqlite3"


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{DEFAULT_DB_PATH.as_posix()}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"
    TESTING = False