import datetime
import sqlite3
import time
from contextlib import closing


DB_PATH = "/app/data/db.sqlite"  # путь к БД внутри контейнера

def init_db():
    """
    Инициализация базы данных sqlite3, создание таблиц:
    - articles (ранее отправленные статьи)
    - subscribers (подписчики бота)
    """
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                link TEXT PRIMARY KEY,
                name TEXT,
                date_published DATE
            )
            """)
            conn.execute("""
            CREATE TABLE IF NOT EXISTS subscribers (
                chat_id TEXT PRIMARY KEY
            )
            """)


def is_article_new(link, published_date, days=7) -> bool:
    """
    Проверяет, что статья не старше `days` дней и не присутствует среди ранее учтённых.
    published_date должна быть time.struct_time
    """
    published_dt = datetime.datetime.fromtimestamp(time.mktime(published_date))
    if not (published_dt >= datetime.datetime.now() - datetime.timedelta(days=days)):
        return False

    with closing(sqlite3.connect(DB_PATH)) as conn:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM articles WHERE link = ?", (link,))
        return cur.fetchone() is None


def mark_article_as_checked(link, title, published_date):
    """
    Добавляет статью в список ранее отправленных.

    :param link: ссылка на статью
    :param title: заголовок статьи
    :param published_date: дата публикации
    """
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            conn.execute(
                "INSERT OR IGNORE INTO articles (link, name, date_published) VALUES (?, ?, ?)",
                (link, title, published_date)
            )


def add_subscriber(chat_id: str):
    """
    Добавляет нового подписчика.

    :param chat_id: идентификатор подписчика
    """
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            conn.execute(
                "INSERT OR IGNORE INTO subscribers (chat_id) VALUES (?)",
                (chat_id,)
            )


def remove_subscriber(chat_id: str):
    """
    Удаляет ранее добавленного подписчика.

    :param chat_id: идентификатор подписчика
    """
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            conn.execute(
                "DELETE FROM subscribers WHERE chat_id = ?",
                (chat_id,)
            )


def get_all_subscribers() -> list:
    """
    Получает список всех подписчиков.

    :return: перечень идентификаторов действующих подписчиков
    """
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT chat_id FROM subscribers")
        return [row[0] for row in cursor.fetchall()]


def cleanup_old_articles(last_days_articles: int = None) -> datetime.date:
    """
    Удаляет статьи старше чем LAST_DAYS_ARTICLES + 7 дней.

    :param last_days_articles: заданное число дней, за которые получаем статьи
    :return: дата, ранее которой статьи были удалены
    """
    from news import LAST_DAYS_ARTICLES
    if not last_days_articles:
        last_days_articles = LAST_DAYS_ARTICLES

    extra_days = 7
    cutoff_date = datetime.datetime.now(datetime. UTC).date() - datetime.timedelta(days=last_days_articles + extra_days)

    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            conn.execute(
                "DELETE FROM articles WHERE date_published < ?",
                (cutoff_date.isoformat(),)
            )

    return cutoff_date
