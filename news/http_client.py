import requests
from requests import Response


class RSSHttpClient:
    def __init__(self, timeout: int = 20):
        self.timeout = timeout

    def fetch(self, url: str) -> Response:
        response = requests.get(
            url,
            timeout=self.timeout,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/120.0.0.0 Safari/537.36",
                "Accept": "application/rss+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8",
            },
        )
        response.raise_for_status()
        return response
