import sqlite3
import time
from contextlib import closing
from datetime import datetime, timedelta

DB_PATH = "db.sqlite"  # путь к БД внутри контейнера

def init_db():
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                link TEXT PRIMARY KEY,
                name TEXT,
                date_published DATE
            )
            """)


def is_article_new(link, published_date, days=7):
    """
    Проверяет, что статья не старше `days` дней и не присутствует среди ранее учтённых.
    published_date должна быть time.struct_time
    """
    published_dt = datetime.fromtimestamp(time.mktime(published_date))
    if not (published_dt >= datetime.now() - timedelta(days=days)):
        return False

    with closing(sqlite3.connect(DB_PATH)) as conn:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM articles WHERE link = ?", (link,))
        return cur.fetchone() is None


def mark_article_as_checked(link, title, published_date):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            conn.execute(
                "INSERT OR IGNORE INTO articles (link, name, date_published) VALUES (?, ?, ?)",
                (link, title, published_date)
            )
