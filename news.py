import feedparser

import requests
from io import BytesIO


def get_news_from_source(url: str) -> list:
    news = []
    response = requests.get(url, verify=False)  # ignore SSL
    feed = feedparser.parse(BytesIO(response.content))

    for entry in feed.entries:
        title, link, published_date = entry.title, entry.link, entry.published
        news.append(
            {
                'title': title,
                'link': link,
                'published_date': published_date,
            }
        )
    return news
