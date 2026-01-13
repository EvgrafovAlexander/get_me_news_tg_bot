import feedparser
import requests

from io import BytesIO

from config.settings import settings
from db import is_article_new, mark_article_as_checked
from logger import logger


def get_news_from_source(url: str) -> list:
    """
    Получает перечень статей из источника.

    :param url: RSS-адрес источника
    :return: перечень статей
    """
    news = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/rss+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8",
    }

    response = requests.get(url, headers=headers, verify=False, timeout=20)  # ignore SSL
    feed = feedparser.parse(BytesIO(response.content))

    for entry in feed.entries:
        try:
            title, link = entry.title, entry.link
            published_date, parsed_published_date = entry.published, entry.published_parsed
            if is_article_new(link, parsed_published_date, settings.rss_last_days):
                news.append(
                    {
                        'title': title,
                        'link': link,
                        'published_date': published_date,
                    }
                )
                mark_article_as_checked(link, title, published_date)
        except Exception:
            logger.exception(
                f"Failed to process RSS entry | source={url} | "
                f"title={getattr(entry, 'title', None)} | "
                f"link={getattr(entry, 'link', None)}"
            )
    return news
