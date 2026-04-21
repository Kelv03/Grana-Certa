from abc import ABC, abstractmethod
from typing import Optional
import requests
from bs4 import BeautifulSoup

from .models import ProductOffer


DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
}


class BaseStore(ABC):
    store_name: str = "Loja"
    base_url: str = ""

    def __init__(self, timeout: int = 20):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)

    def get_soup(self, url: str) -> BeautifulSoup:
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        return BeautifulSoup(response.text, "lxml")

    @abstractmethod
    def search(self, query: str) -> Optional[ProductOffer]:
        raise NotImplementedError