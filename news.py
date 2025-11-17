import feedparser
import requests

from io import BytesIO

from db import is_article_new, mark_article_as_checked


def get_news_from_source(url: str) -> list:
    news = []
    response = requests.get(url, verify=False)  # ignore SSL
    feed = feedparser.parse(BytesIO(response.content))

    for entry in feed.entries:
        title, link = entry.title, entry.link
        published_date, parsed_published_date = entry.published, entry.published_parsed
        if is_article_new(link, parsed_published_date):
            news.append(
                {
                    'title': title,
                    'link': link,
                    'published_date': published_date,
                }
            )
            mark_article_as_checked(link, title, published_date)
    return news
