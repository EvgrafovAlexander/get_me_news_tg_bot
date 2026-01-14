from news.http_client import RSSHttpClient
from news.parser import RSSParser


class NewsReader:
    def __init__(self, http_client: RSSHttpClient, parser: RSSParser):
        self.http_client = http_client
        self.parser = parser

    def read(self, source_url: str) -> list[dict]:
        """
        Загружает RSS и возвращает статьи.
        """
        response = self.http_client.fetch(source_url)
        return self.parser.parse(response.content, source_url)
